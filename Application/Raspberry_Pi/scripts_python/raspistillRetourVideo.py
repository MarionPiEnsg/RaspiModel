#! /usr/bin/python
# -*- coding:utf-8 -*-
import time
import Image
from os import popen
arret = False
time.sleep(5)
i = 1
while arret == False:
    sortie=popen("cd /home/pi/Videos/ && ls")
    print("boucle : "+str(i))
    for line in sortie.read().splitlines():
        if("arret.txt" == line):
            arret = True
    if(arret):
        break
    images = popen("cd /home/pi/Videos/donnees_acqui/ && ls")
    for Limage in images.read().splitlines():
        t1 = time.time()
        image = Image.open("/home/pi/Videos/donnees_acqui/"+Limage , "r")
        image.thumbnail([300,225], Image.ANTIALIAS) 
        image.save("/tmp/stream/pic.jpg", "JPEG")
        print(Limage)
        t2 = time.time()
        t3 = 3 - (t2 - t1)
        print(t3)
        time.sleep(t3)
    i = i+1
print("fin")
