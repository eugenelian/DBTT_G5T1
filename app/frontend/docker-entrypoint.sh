#!/bin/sh
# Default value if not provided
: "${VITE_API_URL:=http://dbttg5t1backend-production:8000}"

# Export so envsubst can access it as a child process
export VITE_API_URL

# Replace environment variables in the nginx template
envsubst '$VITE_API_URL' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'
