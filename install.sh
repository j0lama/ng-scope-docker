#!/usr/bin/env bash
cd docker || exit
sudo docker build -t ngscope .
cd ..
sudo ln -s $(pwd)/ngscope.sh /usr/local/bin/ngscope-docker