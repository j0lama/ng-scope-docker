#!/usr/bin/env bash

sudo docker pull princetonpaws/ng-scope:22.04
sudo ln -s $(pwd)/ng-scope.sh /usr/local/bin/ngscope-docker