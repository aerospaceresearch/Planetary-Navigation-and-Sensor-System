#!/bin/bash
lsusb -d 0bda:2838 > /dev/null
directory="data/"
separator="_"
fileending=".dat"
while [ $? == 0 ]
do
    timed=$(date +%s)
    hostn=$(hostname)
    rtl_sdr -f 446000000 -g 30 -n 122880000 "$directory$hostn$separator$timed$fileending"
    echo "Recorded" 
    lsusb -d 0bda:2838 > /dev/null
done
