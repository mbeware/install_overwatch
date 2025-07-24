sudo mv /usr/bin/curl /usr/bin/curl.original
sudo tee /usr/bin/curl > /dev/null <<'EOF'
#!/bin/bash
echo "$(date) CURL command: curl $*" >> /var/log/curl_downloads.log
exec /usr/bin/curl.original "$@"
EOF

sudo chmod +x /usr/bin/curl
# look into LD_PRELOAD for curl comme remplacement. 