#!/bin/bash
pkill raspistill
rm /home/pi/Videos/arret.txt
temps=$(($1*1000))
raspistill -vf -hf --nopreview -q 5 -o /home/pi/Videos/donnees_acqui/img_%1d.jpg -tl 500 -t $temps
