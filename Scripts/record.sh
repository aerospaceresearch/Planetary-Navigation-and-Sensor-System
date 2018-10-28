#!/bin/bash
lsusb -d 0bda:2838 > /dev/null																#DVBT-device connected
directory="data/"																			#Path of data
separator="_"
fileending=".dat"
while [ $? == 0 ]																			#while device is connected
do
    timed=$(date +%s)																		#set time stemp
    hostn=$(hostname)                                                                       #get hostname
    rtl_sdr -f 446000000 -g 30 -n 122880000 "$directory$hostn$separator$timed$fileending"	#record
    echo "Recorded" 
    lsusb -d 0bda:2838 > /dev/null
done
