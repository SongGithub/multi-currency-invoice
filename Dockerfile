FROM ubuntu:xenial
# DO NOT EDIT the line above - your final image must be based on ubuntu:xenial

RUN \
    apt update && \
    apt install -y python3-pip && \
    rm -rf /var/lib/apt/lists

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip3 freeze