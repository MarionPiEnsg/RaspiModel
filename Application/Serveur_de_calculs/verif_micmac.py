#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import popen, listdir
import sys
import subprocess
import time


dossier = str(sys.argv[1])
print(dossier)
chaine = "FATAL ERROR" # Texte à rechercher
erreur = False
Tapioca = "Tapioca.txt"
Tapas = "Tapas.txt"
C3DC="C3DC.txt"
fichierErreur = dossier+"/Erreur.txt"
fichierFin = dossier+"/fin.txt"
while (erreur == False):
    dossierTravail = listdir(dossier+'/donnees_acqui')
    time.sleep(10)
    for line in dossierTravail:
        if Tapioca in line :
            fichierTapioca = dossier+"/donnees_acqui/Tapioca.txt"
            print(fichierTapioca)
            fTapioca = open(fichierTapioca,"r").readlines()
            for ligneTapioca in fTapioca:
                if chaine in ligneTapioca:
                    erreur = True
                    open(fichierErreur, "w")
                    open(fichierFin, "w")
                    subprocess.call(['pkill', '-f', 'mm3d'])
                    break
        if Tapas in line:
            fichierTapas = dossier+"/donnees_acqui/Tapas.txt"
            print(fichierTapas)
            fTapas = open(fichierTapas,"r").readlines()
            for ligneTapas in fTapas:
                if chaine in ligneTapas:
                    erreur = True
                    open(fichierErreur, "w")
                    open(fichierFin, "w")
                    subprocess.call(['pkill', '-f', 'mm3d'])
                    break
        if C3DC in line:
            fichierC3DC = dossier+"/donnees_acqui/C3DC.txt"
            fC3DC = open(fichierC3DC,"r").readlines()
            for ligneC3DC in fC3DC:
                if chaine in ligneC3DC:
                    erreur = True
                    open(fichierErreur, "w")
                    open(fichierFin, "w")
                    subprocess.call(['pkill', '-f', 'mm3d'])
                    break
print(erreur)
