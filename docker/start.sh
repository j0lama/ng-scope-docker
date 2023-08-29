#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "USE: $0 <EARFCN list>"
    exit 1
fi

./tools/genConfig.py config.cfg ${@:1}
RET=$?
if [ $RET != 0 ]; then
    echo "Error generating NG-Scope config file"
    exit 1
fi

cat config.cfg

./ngscope > /dev/null
./ngscope -c config.cfg -s logs/sibs.dump -o logs/dci_output/
