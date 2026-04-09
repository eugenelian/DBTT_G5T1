#!/bin/sh
set -e

# Default value if not provided
: "${VITE_API_URL:=http://ai-clinical-assistant-backend:8000}"

echo "[entrypoint] VITE_API_URL is set to: '${VITE_API_URL}'"

# Replace environment variables in the nginx template.
# Use sed as a robust fallback in addition to envsubst so the literal
# placeholder is always replaced even if envsubst has scope issues.
if envsubst '$VITE_API_URL' \
      < /etc/nginx/conf.d/nginx.conf.template \
      > /etc/nginx/conf.d/default.conf 2>/tmp/envsubst.err; then
    echo "[entrypoint] envsubst succeeded"
else
    echo "[entrypoint] envsubst failed (exit $?), stderr:" >&2
    cat /tmp/envsubst.err >&2
    echo "[entrypoint] falling back to sed substitution" >&2
    sed "s|\${VITE_API_URL}|${VITE_API_URL}|g" \
        /etc/nginx/conf.d/nginx.conf.template \
        > /etc/nginx/conf.d/default.conf
fi

# If envsubst left the placeholder unreplaced (e.g. variable was empty or
# envsubst silently did nothing), force-replace it with sed.
if grep -q '\${VITE_API_URL}' /etc/nginx/conf.d/default.conf; then
    echo "[entrypoint] WARNING: placeholder still present after envsubst, applying sed fix" >&2
    sed -i "s|\${VITE_API_URL}|${VITE_API_URL}|g" /etc/nginx/conf.d/default.conf
fi

echo "[entrypoint] Generated nginx config (/etc/nginx/conf.d/default.conf):"
cat /etc/nginx/conf.d/default.conf

# Start nginx
exec nginx -g 'daemon off;'
