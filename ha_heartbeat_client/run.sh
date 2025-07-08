#!/usr/bin/with-contenv bashio

SERVER_URL=$(bashio::config 'server_url')
TOKEN=$(bashio::config 'token')

python3 /heartbeat_client.py "$SERVER_URL" "$TOKEN"
        