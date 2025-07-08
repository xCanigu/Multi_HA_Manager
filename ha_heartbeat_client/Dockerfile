FROM ghcr.io/hassio-addons/base:latest

COPY run.sh /run.sh
COPY heartbeat_client.py /heartbeat_client.py

# Install Python + package
RUN apk add --no-cache python3 py3-pip
RUN pip3 install requests websockets

# Add permission to start script
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]