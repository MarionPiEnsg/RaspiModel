#! /usr/bin/python
# -*- coding:utf-8 -*-
import shutil
import os
#création d'un dossier pour y mettre les images
nom="/home/pi/Videos/donnees_acqui"
# si le dossier des images existe deja on le supprime
if os.path.exists(nom):
    shutil.rmtree(nom)
#on cree un dossier pour y mettre les images et on s'y place
os.mkdir(nom)
#os.chdir(nom)
