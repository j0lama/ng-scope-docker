#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "USE: $0 <Number of USRPs> <EARFCN>"
    exit 1
fi

./tools/genConfig.py $1 $2 config.cfg
RET=$?
if [ $RET != 0 ]; then
    echo "Error generating NG-Scope config file"
    exit 1
fi

./ngscope > /dev/null
./ngscope -c config.cfg -s logs/sibs.dump -o logs/dci_output/