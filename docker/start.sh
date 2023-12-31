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

# Initialize Log Collector
if [ "$FRAG" -ne "0" ]; then
   ./logCollector.py $LOGS/ $LOCATION $EXPERIMENT &
fi

# Remove exiting logs
rm -Rf $LOGS/

./ngscope > /dev/null
if [ "$TIMEOUT" -ne "0" ]; then
    timeout $TIMEOUT ./ngscope -c config.cfg -s $LOGS/sibs/ -o $LOGS/dci_output/
else
    ./ngscope -c config.cfg -s $LOGS/sibs/ -o $LOGS/dci_output/
fi

# If logs are not fragmented, upload the resulting log
if [ "$FRAG" -eq "0" ]; then
    echo "Please wait until the logs get pushed to the central registry"
    UPLOAD_ALL=1 ./logCollector.py $LOGS/ $LOCATION $EXPERIMENT 
fi
