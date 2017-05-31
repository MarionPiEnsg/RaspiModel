#!/bin/sh
#dossier de travail pour micmac en entree
dossier=$1

#dossier de travail dela Raspberry Pi en entree
dossierPi=$2

#fonction permettant de verifier si le fichier Erreur.txt existe grace a "-e"
testErreur()
{ if [ -e $dossier+"/Erreur.txt" ]
	then
		exit #s'il existe alors on arree le script
	fi
}

#Recueration des informations de connexion au FTP hebergeant le visualisateur Potree 
loginFTP=$(grep loginFTP $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)
passeFTP=$(grep passeFTP $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)
hoteFTP=$(grep hoteFTP $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)

#Recueration des informations de connexion au SSH de la Raspberry Pi
loginRasp=$(grep loginRasp $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)
passeRasp=$(grep passeRasp $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)
ipRasp=$(grep ipRasp $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)

#Emplacement de Micmac sur la machine
micmac=$(grep micmac $dossier/config.txt | cut -d":" -f2 | cut -d" " -f2)


#On vide le dossier des images et des calculs micmac
rm -rf $dossier/donnees_acqui/*
# On supprime le dossier de Potree qui sera recréé automatiquement plus tard
rm -r $dossier/nuage/
#Suppression des deux fichiers de fin : fin.txt et Erreur.txt s'ils existent, sinon le script continu et ne prend pas compte de l'erreur
rm $dossier/fin.txt
rm $dossier/Erreur.txt

#les images de l'acquisition on recuperees par ssh depuis la raspberry pi et copiees dans le dossier des images sur cette machine
sshpass -p $passeRasp scp -rp $loginRasp@$ipRasp:$dossierPi/donnees_acqui/*.jpg $dossier/donnees_acqui/
#on se place dans le dossier de images (qui est aussi de dossiers des calculs micmac)
cd $dossier/donnees_acqui/
ls

#Calculs micmac
#Recherche des points de liaison
$micmac/mm3d Tapioca All ".*jpg" -1 Detect=Digeo > Tapioca.txt # le rapport est ecrit dans le fichier texte
testErreur
#Mise en place des images
$micmac/mm3d Tapas RadialBasic ".*jpg" Out=MEP > Tapas.txt # le rapport est ecrit dans le fichier texte
testErreur
#Generation du nuage de points
$micmac/mm3d C3DC QuickMac ".*jpg" MEP ZoomF=4 > C3DC.txt # le rapport est ecrit dans le fichier texte
testErreur
cd ..

#Creation du viewer du nuage de points precedement cree avec PotreeConverter
PotreeConverter $dossier/donnees_acqui/C3DC_QuickMac.ply -o $dossier/nuage -p nuage --overwrite

#Envoi des donnees crees sur le serveur FTP de visualisation et de partage de fichier
wput $dossier/nuage/nuage.html ftp://$loginFTP:$passeFTP@$hoteFTP/wwwR/nuage/nuage.html -u
wput /nuage/pointclouds/ ftp://$loginFTP:$passeFTP@$hoteFTP/wwwR/nuage/pointclouds/ -u
wput /donnees_acqui/C3DC_QuickMac.ply ftp://$loginFTP:$passeFTP@$hoteFTP/wwwR/nuage.ply.xyz -u

#lorsque le script est terminé, on cree le fichier fin.txt (utile dans d'autres scripts)
echo "fin" > fin.txt

exit # securite pour que le script s'arrete bien

#Pour plus d'information sur les commandes micmac, se referer a sa documentation sur http://micmac.ensg.eu
