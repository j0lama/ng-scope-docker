#!/bin/bash

LOGS=./logs/logs

if [ "$#" -lt 2 ]; then
    echo "USE: $0 <Fragmentation (yes/no)> <EARFCN list>"
    exit 1
fi

./genConfig.py $1 config.cfg ${@:2}
RET=$?
if [ $RET != 0 ]; then
    echo "Error generating NG-Scope config file"
    exit 1
fi

# Initialize Log Collector
EXPERIMENT=$(./utils/formatText.py "$HOST_HOSTNAME")
./logCollector.py $LOGS/ $LOCATION $EXPERIMENT

# Remove exiting logs
rm -Rf $LOGS/

./ngscope > /dev/null
./ngscope -c config.cfg -s $LOGS/sibs/ -o $LOGS/dci_output/
