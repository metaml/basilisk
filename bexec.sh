#!/bin/bash

PYTHONPATH="/"
for i in $(find /nix/store -name site-packages -type d | grep python); do
    PYTHONPATH=$PYTHONPATH:$i
done

export LD_LIBRARY_PATH=/Basilisk:$LD_LIBRARY_PATH
export PYTHONPATH

exec python3 $1
