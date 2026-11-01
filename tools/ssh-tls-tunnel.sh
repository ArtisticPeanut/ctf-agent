#!/usr/bin/env bash
# SSH-over-TLS + reverse SOCKS tunnel.
#
# Topology:
#   laptop (venue LAN) --TLS:443--> EC2 stunnel --> EC2 sshd
#   EC2 127.0.0.1:$PORT --> SSH reverse forward --> laptop microsocks
#
# Usage:
#   ./ssh-tls-tunnel.sh [port]        # default 1080
#
# Override with env vars: EC2, SSH_USER, KEY, SNI, LOCAL_TLS_PORT.
set -euo pipefail

PORT="${1:-1080}"
EC2="${EC2:-44.193.44.44}"
SSH_USER="${SSH_USER:-ubuntu}"
KEY="${KEY:-$HOME/.ssh/ctf_ed25519}"
SNI="${SNI:-cdn-edge.local}"
LOCAL_TLS_PORT="${LOCAL_TLS_PORT:-2222}"

for bin in microsocks stunnel autossh ssh; do
    command -v "$bin" >/dev/null 2>&1 || {
        echo "missing dependency: $bin" >&2
        echo "sudo apt update && sudo apt install -y stunnel4 autossh microsocks" >&2
        exit 1
    }
done

if [[ ! -r "$KEY" ]]; then
    echo "key not readable: $KEY" >&2
    exit 1
fi

# Stop previous instances of this tunnel.
pkill -f "microsocks .* -p ${PORT}( |$)" 2>/dev/null || true
pkill -f "stunnel /tmp/ssh-cli-${PORT}.conf" 2>/dev/null || true
sleep 0.3

# SOCKS proxy bound to loopback only. Do not expose it on the LAN.
microsocks -q -i 127.0.0.1 -p "$PORT" &
MICROSOCKS_PID=$!

CONF="/tmp/ssh-cli-${PORT}.conf"
cat >"$CONF" <<EOF
foreground = yes
debug = 2

[ssh-tls]
client = yes
accept = 127.0.0.1:${LOCAL_TLS_PORT}
connect = ${EC2}:443
sni = ${SNI}
verifyChain = no
EOF

stunnel "$CONF" &
STUNNEL_PID=$!

cleanup() {
    kill "$MICROSOCKS_PID" "$STUNNEL_PID" 2>/dev/null || true
    wait "$MICROSOCKS_PID" "$STUNNEL_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

sleep 1
if ! kill -0 "$STUNNEL_PID" 2>/dev/null; then
    echo "stunnel failed to start; check the TLS endpoint ${EC2}:443" >&2
    exit 1
fi

echo "TLS   ${EC2}:443 (SNI ${SNI}) -> 127.0.0.1:${LOCAL_TLS_PORT}"
echo "SOCKS EC2 127.0.0.1:${PORT} -> laptop 127.0.0.1:${PORT}"
echo "Press Ctrl-C to stop."

# No exec: keep the trap alive so both helper processes are cleaned up.
autossh -M 0 -N \
    -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes -o ConnectTimeout=10 \
    -o StrictHostKeyChecking=accept-new \
    -o UserKnownHostsFile="$HOME/.ssh/known_hosts_tunnel" \
    -o IdentitiesOnly=yes -i "$KEY" \
    -p "$LOCAL_TLS_PORT" \
    -R "127.0.0.1:${PORT}:127.0.0.1:${PORT}" \
    "${SSH_USER}@127.0.0.1"
