#!/bin/bash

STORAGEPATH=/data/pcap
STORAGEPART=/dev/md0
MAXSPACE=95
USEDSPACE=`df $STORAGEPART | tail -n1 | tr -s ' ' ' ' | cut -f 5 -d ' ' | sed 's/%//'`

while [[ $MAXSPACE -le $USEDSPACE ]]
do
	logger -t "ROLLINGCAPTURE" "Removing files to regain storage space"
	DELETE=`ls -1t $STORAGEPATH/*.capture | tail -n 1` 
	logger -t "ROLLINGCAPTURE" "Deleting $DELETE"
	#rm $DELETE
done

logger -t "ROLLINGCAPTURE" "$USEDSPACE% of $STORAGEPART used for packet capture. Limit is $MAXSPACE%"

#now check the directories have been created for tomorrow's capture
test -d $STORAGEPATH/`date -d tomorrow +%Y%m%d` || mkdir $STORAGEPATH/`date -d tomorrow +%Y%m%d`
