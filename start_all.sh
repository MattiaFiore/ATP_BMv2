#!/bin/bash

'
This script will send from each host the packet that you need to aggregate 
'
HOSTS=("h0" "h1" "h2" "h3")



# Iterate through the list and echo each item
for HOST in "${HOSTS[@]}"; do

  echo "STARTING WORKER $HOST"
  #Finding the PID of heach host 
  PID=$(ps aux | grep $HOST | grep 'bash' | awk '{print $2}')
  echo "$PID"
  #Execute the worker code 
  sudo mnexec -a $PID python3 worker.py -id 1 -sn 1 -agg 10 & 

done

wait