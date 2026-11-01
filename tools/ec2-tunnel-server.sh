#!/usr/bin/env bash
# Run on the EC2 host (Ubuntu/Debian) with sudo.
# Terminates TLS on :443 and forwards it to the local sshd on :22.
set -euo pipefail

TLS_PORT="${TLS_PORT:-443}"
SSH_PORT="${SSH_PORT:-22}"
SNI="${SNI:-cdn-edge.local}"

if ! command -v stunnel >/dev/null 2>&1; then
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get install -y stunnel4 openssl
fi

install -d -m 755 /etc/stunnel
if [[ ! -s /etc/stunnel/stunnel.pem ]]; then
    openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
        -keyout /etc/stunnel/stunnel.key \
        -out /etc/stunnel/stunnel.crt \
        -subj "/CN=${SNI}"
    cat /etc/stunnel/stunnel.key /etc/stunnel/stunnel.crt >/etc/stunnel/stunnel.pem
    chmod 600 /etc/stunnel/stunnel.key /etc/stunnel/stunnel.pem
fi

cat >/etc/stunnel/stunnel.conf <<EOF
pid = /var/run/stunnel4/stunnel.pid
output = /var/log/stunnel4/stunnel.log
debug = 4

[ssh-tls]
accept = 0.0.0.0:${TLS_PORT}
connect = 127.0.0.1:${SSH_PORT}
cert = /etc/stunnel/stunnel.pem
sslVersion = TLSv1.2
EOF

mkdir -p /var/run/stunnel4 /var/log/stunnel4
chown stunnel4:stunnel4 /var/run/stunnel4 /var/log/stunnel4 2>/dev/null || true
sed -i 's/^ENABLED=.*/ENABLED=1/' /etc/default/stunnel4 2>/dev/null || true

systemctl enable stunnel4 >/dev/null 2>&1 || true
systemctl restart stunnel4 2>/dev/null || stunnel /etc/stunnel/stunnel.conf

sleep 1
if ss -ltn | grep -q ":${TLS_PORT} "; then
    echo "stunnel listening on :${TLS_PORT} -> 127.0.0.1:${SSH_PORT}"
else
    echo "stunnel did not bind :${TLS_PORT}; check /var/log/stunnel4/stunnel.log" >&2
    exit 1
fi
