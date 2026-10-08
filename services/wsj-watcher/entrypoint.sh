#!/bin/bash
set -euo pipefail
umask 077
: "${ADMIN_PASSWORD:?Set ADMIN_PASSWORD to a random password of at least 24 characters}"
if [ "${#ADMIN_PASSWORD}" -lt 24 ]; then echo 'ADMIN_PASSWORD too short' >&2; exit 1; fi
case "${PORT:-8080}" in ''|*[!0-9]*) exit 1;; esac
case "${MODE:-login}" in login|watch|once) ;; *) exit 1;; esac
mkdir -p /data /tmp/nginx /tmp/nginx/body /tmp/nginx/proxy
chown -R pwuser:pwuser /data /tmp/nginx
printf '%s\n' "$ADMIN_PASSWORD" | htpasswd -i -c /tmp/admin.htpasswd admin >/dev/null
chmod 644 /tmp/admin.htpasswd
unset ADMIN_PASSWORD
Xvfb :99 -screen 0 1440x1000x24 -nolisten tcp &
pids=("$!")
for attempt in {1..50}; do
  if xdpyinfo -display :99 >/dev/null 2>&1; then break; fi
  sleep 0.1
done
xdpyinfo -display :99 >/dev/null 2>&1 || { echo 'Display startup failed' >&2; exit 1; }
login_location='location / { return 404; }'
if [ "${MODE:-login}" = login ]; then
  # Reachable only behind nginx authentication, never published as raw VNC.
  su -s /bin/bash pwuser -c 'exec x11vnc -display :99 -noshm -localhost -nopw -forever -shared -rfbport 5900' &
  pids+=("$!")
  /usr/bin/websockify --web=/usr/share/novnc 127.0.0.1:6080 127.0.0.1:5900 &
  pids+=("$!")
  login_location='location / { auth_basic "WSJ private browser"; auth_basic_user_file /tmp/admin.htpasswd; proxy_pass http://127.0.0.1:6080; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_read_timeout 3600s; }'
fi
cat >/tmp/nginx.conf <<EOF
worker_processes 1;
pid /tmp/nginx/nginx.pid;
error_log /dev/stderr warn;
events { worker_connections 128; }
http {
  access_log off;
  client_body_temp_path /tmp/nginx/body;
  proxy_temp_path /tmp/nginx/proxy;
  server {
    listen ${PORT:-8080};
    add_header Cache-Control "no-store" always;
    add_header X-Content-Type-Options nosniff always;
    location = /health { proxy_pass http://127.0.0.1:8081/health; }
    location = /status { auth_basic "WSJ status"; auth_basic_user_file /tmp/admin.htpasswd; proxy_pass http://127.0.0.1:8081/status; }
    $login_location
  }
}
EOF
nginx -c /tmp/nginx.conf -g 'daemon off;' &
pids+=("$!")
su -s /bin/bash pwuser -c 'cd /app && exec python watcher.py' &
pids+=("$!")
trap 'kill "${pids[@]}" 2>/dev/null || true; wait || true' EXIT
trap 'exit 0' TERM INT
set +e
wait -n -p exited_pid "${pids[@]}"
exit_status=$?
echo "Required process exited: pid=${exited_pid:-unknown}, status=$exit_status" >&2
exit 1
