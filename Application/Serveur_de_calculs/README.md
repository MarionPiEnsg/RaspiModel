Placer le dossier "Serveur_de_calculs" à l'emplacement souhaité sur la machine qui est équipée de Micmac.

Avant lancer l'application, veuillez à modifier le fichier **config.txt** pour remplacer les valeurs par les votres.
Attention les entetes de doivent pas être modifiées et la structure doit rester intacte comme suit:

### exempleConfig.txt
  
     Description de la section 1
     nomPremiereVariable: maPremiereValeur
    
     Description de la section 12
     nomSecondeVariable: maSecondeValeur

 
 Seules les valeurs comme "maPremiereValeur" et "maSecondeValeur" doivent être modifiées.
 
 ----------
Programmes nécessaires:
- MicMac
- PotreeConverter
- sshpass
- scp
- wput
- Python 2.7 :
  - os
  - sys
  - subprocess
  - time
