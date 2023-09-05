#!/bin/bash

Help() {
    echo "Usage:   $0 <NG-Scope Image name> <EARFCN List>"
    echo "Example: $0 j0lama/ng-scope:latest 700"
    echo "Example: $0 j0lama/ng-scope:latest 700 300"
    echo
    exit 1
}

# Cheking arguments
if [ "$#" -lt 2 ]; then
    Help
fi

docker run --name ng-scope -ti --privileged --rm -v $(pwd):/ng-scope/build/ngscope/src/logs/ $1 ./start.sh ${@:2}
