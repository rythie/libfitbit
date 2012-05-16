#!/bin/bash

# A script to start libfitbit when the device is connected and restart it if it crashes

LIBFITBITPATH="/root/libfitbit";
 
while [ true ]
do
	lsusb -d 10c4:84c4
	if [ $? == 0 ] # wait for device to be connected
	then
		echo "Starting..."
		$LIBFITBITPATH/python/fitbit_client.py
	fi

	sleep 10;
done
