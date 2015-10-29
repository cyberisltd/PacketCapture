#!/bin/bash
#Author Geoff Jones (nop@0x90.co.uk)

BASELOCATION=/data/pcap
STORAGELOCATION=$BASELOCATION/%Y%m%d
FILENAME=%Y%m%d%H%M-$1.pcap
LOG=/var/log/tcpdump/`date +%F`-$$-$1.log
INTERFACE=$1
PCAPMAXSIZE=250
ROLLOVER=300
TCPDUMP=/usr/sbin/tcpdump
BUFFERSIZE=52428
SNAPLENGTH=0
FILTER=""

#Starting process and logging

if ! test -d $BASELOCATION/`date +%Y%m%d`
then
	echo "Storage location doesn't exist. Cron daemon running to create dirs? Creating now...but ensure the crontab is running correctly"
	if ! mkdir $BASELOCATION/`date +%Y%m%d` 
	then
		echo "Cannot create storage dir, exiting"
		exit 1
	fi
fi

$TCPDUMP -B $BUFFERSIZE -i $INTERFACE -C $PCAPMAXSIZE -G $ROLLOVER -s $SNAPLENGTH -w $STORAGELOCATION/$FILENAME $FILTER 2>> $LOG &

echo "Check $LOG for information"

exit 0

