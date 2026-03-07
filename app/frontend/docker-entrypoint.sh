#!/bin/sh
# Default value if not provided
: "${VITE_API_URL:=http://ai-clinical-assistant-backend:8000}"

# Replace environment variables in the nginx template
envsubst '$VITE_API_URL' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'
