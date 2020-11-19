#!/bin/bash -e

#######################
## !!!!!!!!!!!!!!!!! ##
## !! DO NOT EDIT !! ##
## !!!!!!!!!!!!!!!!! ##
#######################

# This script must NOT be edited. It is used to run our other shell scripts inside a Docker container.

IMAGETAG="xero-code-test:latest"

if [ ! -x "$(command -v docker)" ]; then
    echo "Please install Docker and ensure the 'docker' command executes successfully."
    exit 1
fi

# Validate Dockerfile
grep -Fxq "FROM ubuntu:xenial" Dockerfile || (echo "Dockerfile be based on ubuntu:xenial" && exit 1)

# Build image
if [ "$CACHE" != "true" ]; then
    CACHE="false"
    if [[ "$(docker images -q $IMAGETAG 2> /dev/null)" != "" ]]; then
        echo "Removing cached Docker image. Use CACHE=true to leverage caching."
        CMD="docker rmi $IMAGETAG"
        echo "$CMD"
        eval "$CMD"
    fi
fi
CMD="docker build -t $IMAGETAG ."
echo "$CMD"
eval "$CMD"

# Run image
CMD="docker run --rm -v $PWD:/app -w /app $IMAGETAG $@"
echo "$CMD"
eval "$CMD"
