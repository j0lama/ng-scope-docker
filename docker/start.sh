#!/bin/bash

if [ "$#" -lt 4 ]; then
    echo "USE: $0 <Fragmentation> <Timeout> <Experiment> <EARFCN list>"
    exit 1
fi

LOGS=./logs/logs
LOCATION=$(./formatText.py "$HOST_HOSTNAME")
FRAG=$1
TIMEOUT=$2
EXPERIMENT=$3

./genConfig.py $FRAG config.cfg ${@:4}
RET=$?
if [ $RET != 0 ]; then
    echo "Error generating NG-Scope config file"
    exit 1
fi

# Remove exiting logs
rm -Rf $LOGS/

./ngscope > /dev/null
if [ "$TIMEOUT" -ne "0" ]; then
    timeout $TIMEOUT ./ngscope -c config.cfg -s $LOGS/sibs/ -o $LOGS/dci_output/
else
    ./ngscope -c config.cfg -s $LOGS/sibs/ -o $LOGS/dci_output/
fi
