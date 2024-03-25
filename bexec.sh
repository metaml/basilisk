#!/bin/bash

PYTHONPATH="/Basilisk"
for i in $(find /nix/store -name site-packages -type d | grep python); do
    PYTHONPATH=$PYTHONPATH:$i
done
echo exec python3 $1
