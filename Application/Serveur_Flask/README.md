Placer le dossier "Serveur_Flask" dans le localhost de la machine qui sert de serveur pour Flask.
Par exemple :
- EasyPhp/
  - www/
    - Serveur_Flask/
      - static/
      - templates/
      - config.txt
      - main.py

-------
Avant lancer l'application, veuillez à modifier le fichier **config.txt** pour remplacer les valeurs par les votres.
Attention les entetes de doivent pas être modifiées et la structure doit rester intacte comme suit:

### exempleConfig.txt
  
     Description de la section 1
     nomPremiereVariable: maPremiereValeur
    
     Description de la section 12
     nomSecondeVariable: maSecondeValeur

 
 Seules les valeurs comme "maPremiereValeur" et "maSecondeValeur" doivent être modifiées.
 
-------
Programmes nécessaires :
- Python 3.6 :
  - Flask
  - paramiko
  - time
