#!/usr/bin/with-contenv bashio

# Citește configurările din UI
SERVER_URL=$(bashio::config 'server_url')
TOKEN=$(bashio::config 'token')

# Rulează scriptul Python
python3 /heartbeat_client.py "$SERVER_URL" "$TOKEN"
