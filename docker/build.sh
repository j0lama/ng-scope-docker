#!/bin/bash

Help() {
    echo "Usage: $0 [Options...]" >&2
    echo "  -n, --name <Image name>     Name of the Docker image (e.g. j0lama/ng-scope:latest)"
    echo "  -s, --scratch               Build Docker image from scrach"
    echo "  -h, --help                  Show help menu"
    echo
    exit 1
}

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -n|--name)
      NAME="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--scratch)
      SCRATCH="--no-cache"
      shift # past argument
      ;;
    -h|--help)
      Help
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

# Cheking arguments
if [[ -z "$NAME" ]]; then
    echo "Error: Image name argument missing"
    echo "Execute '$0 --help' for more help"
    exit 1
fi

docker build $SCRATCH -t $NAME .