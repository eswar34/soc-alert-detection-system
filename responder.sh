#!/bin/bash

IP=$1
ACTION=$2

LOG_FILE="response.log"

echo "----------------------------------" >> $LOG_FILE
echo "Time: $(date)" >> $LOG_FILE
echo "IP: $IP" >> $LOG_FILE
echo "Action Taken: $ACTION" >> $LOG_FILE

if [ "$ACTION" == "BLOCK IP" ]; then
    echo "Simulating IP block for $IP" >> $LOG_FILE
    echo "Result: IP $IP blocked (simulation)" >> $LOG_FILE
else
    echo "Monitoring IP $IP" >> $LOG_FILE
    echo "Result: No blocking performed" >> $LOG_FILE
fi

echo "----------------------------------" >> $LOG_FILE
