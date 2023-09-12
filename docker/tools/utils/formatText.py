#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
    exit(1)

print("_".join(sys.argv[1].split()).lower())