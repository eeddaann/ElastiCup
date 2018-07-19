FROM docker.elastic.co/kibana/kibana:6.3.1
ARG NODE_OPTIONS="--max-old-space-size=4096"
RUN ["/usr/share/kibana/bin/kibana-plugin","install","https://download.elastic.co/kibana/canvas/kibana-canvas-0.1.2055.zip"]
