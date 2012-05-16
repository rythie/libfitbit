#!/bin/bash
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
