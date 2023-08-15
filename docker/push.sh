#!/bin/bash

Help() {
    echo "Push image to Docker Hub (https://hub.docker.com)" >&2
    echo "Usage: $0 <Image name> (e.g. j0lama/ng-scope:latest)"
    echo
    exit 1
}

# Cheking arguments
if [ "$#" -ne 1 ]; then
    Help
fi

docker image push $1