#!/bin/bash

while true; do
    ./dnd.py 2>&1 | tee -a log
    sleep 1
done
