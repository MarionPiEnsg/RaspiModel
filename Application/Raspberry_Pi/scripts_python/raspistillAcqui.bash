#!/bin/bash
#on arrete raspistill s'il est deja en cours (s'il ne l'est pas, le script va comptinuer) 
pkill raspistill

#on supprime le fichier de rapport "arret.txt" laissé par un calcul precedent
rm /home/pi/Videos/arret.txt

#on recupere le nombre de secondes souhaitees pour l'acquisition qu'on multiplie par 1000 pour avoir des milisecondes
temps=$(($1*1000))
#lancement de l'acquisition pour $temps secondes avec une image toutes les 1/2 secondes (-tl 500)
#les images sont retournees car la camera est positionnee a l'envers sur son support (-vf -hf)
# -q 5 correspond à la qualite des images a acquerir, valeurs de 0 à 100
# les images ont un nom qui s'incremente au fur et a mesure de l'acquisition
raspistill -vf -hf --nopreview -q 5 -o /home/pi/Videos/donnees_acqui/img_%1d.jpg -tl 500 -t $temps
