#!/bin/bash

while true; do
    ./dnd.py | tee -a log
    sleep 1
done

