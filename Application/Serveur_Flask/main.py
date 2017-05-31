#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
import paramiko
import time

#Recherche du chemin du fichier main (sans le nom)
path = __file__
nomFichierCourant = "main.py"
taille = len(nomFichierCourant)
cheminMain = path[0:-taille]

#Chemins de travail des machines distantes
valeursDicoDist = dict()
filename = cheminMain+"config.txt"
with open(filename, "r") as file:
    for line in file:
        try:
            name, valeurDicoDist = line.split(":")
            valeursDicoDist[name.strip()] = valeurDicoDist.strip()
        except: #permet de gerer ce qui n'est pas des renseignements, comme des explication ou les titres
            pass
cheminTravailPi=valeursDicoDist["cheminTravailPi"]
cheminTravailServeurCalculs=valeursDicoDist["cheminTravailServeurCalculs"]
    

# initialisation des chaines de caractères à remplir dans le html via Jinja
titre = "RaspiModel"
ConnectRasp = "NO"
ConnectServ = "NO"
# connection a la raspberry pi et au serveur de calculs    
sshRasp = paramiko.SSHClient()
sshServ = paramiko.SSHClient()
sshRasp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshServ.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#-------------- Retour video --------  
def functionInitDossierPhotoRasp():
    """
       Fonction qui va appeler un script python sur la raspberry pi afin de supprimer 
       le dossier d'acquisition puis va le recreer. Ceci dans le but de ne pas provoquer
       d'erreurs lors de l'ecrasement des images. Puis va vider la corbeille.
       La fonction retourne "Initiation rasp" dans le terminal si les deux étapes se sont 
       bien déroulées, sinon "bug Initiation rasp" s'affiche.
    """
    try:
        sshRasp.exec_command('python '+cheminTravailPi+'/scripts_python/initialisation.py')
        sshRasp.exec_command('cd / && trash-empty')
        print("Initiation rasp")
    except:
        print("bug Initiation rasp")
  
@app.route('/retourVideoAcquiServeur')
def functionRetourVideoAcquiServeur():
    """
        Fonction qui active le serveur de streming sur la rasberry pi
        Il va lire l'image pic.jpg qui se situe dans le dossier temporaire créé avec la fonction "functionRetourVideoAcqui"
        Retourne dans le terminal Python l'état de la commande avec "Serveur video" ou "bug Serveur video"
    """
    try:
        sshRasp.exec_command('mjpg_streamer -i "/usr/local/lib/input_file.so -f /tmp/stream -n pic.jpg" -o "/usr/local/lib/output_http.so -w /usr/local/www"')
        print("Serveur video")
    except:
        print("bug serveur video")
    return jsonify("");    
    
@app.route('/retourVideoAcqui')
def functionRetourVideoAcqui():
    """
        Fonction de lancement de la camera de la rapsberry pi
        Crée un dossier temporire pour stocker l'image courante
        Puis lance la commande d'activation de la camera qui stocke ses images dans le dossier précedement créé, chaque image porte le nom de pic.jpg, cette image sera crée > stockée > lue par le serveur de streaming > écrasée par l'image suivante
        Retourne dans le terminal Python l'état de la commande avec "video" ou "bug video"
    """
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = sshRasp.exec_command('mkdir /tmp/stream')
        ssh_stdin1, ssh_stdout1, ssh_stderr1 = sshRasp.exec_command('raspistill -vf -hf --nopreview -w 266 -h 200 -q 5 -o /tmp/stream/pic.jpg -tl 500 -t 9999999')  
    except:
        print("bug video")
    functionRetourVideoAcquiServeur()
    return jsonify("")

@app.route('/FinRetourVideoAcqui')
def functionFinRetourVideoAcqui():
    """
        Fonction qui éteint la camera de la raspberry pi via la commande 'pkill raspistill'
        Retourne dans le terminal Python l'état de la commande avec "fin video" ou "bug fin video"
    """
    try:
        sshRasp.exec_command('pkill raspistill')
        print("fin video")
    except:
        print("bug fin video")
    return jsonify("")

        
#-------------- Fonctions de mouvement du robot --------
#paramètres pour les servo moteurs
min_bas = 2.5
centre_bas = 6.5
max_bas = 11.5
decalage_bas=0.1
min_haut = 3.5
centre_haut = 5
max_haut = 5.5
decalage_haut=0.1
coefVitesseBas = 5
coefVitesseHaut = 3
#Activation du robot
def functionActivRobot():
    """
        Cette fonction a pour but d'initialiser les servo moteur afin de les placer à leur position de départ.
        Si les commandes ssh échoues "Activation robot échouée" s'affiche sinon c'est "activation robot OK".
        La fonction retourne au JS via jsonify "Activ ok".
    """
    try:
        commandeBas='python '+cheminTravailPi+'/scripts_python/1-activeRobotBas.py '+str(centre_bas)
        commandeHaut='python '+cheminTravailPi+'/scripts_python/1-activeRobotHaut.py '+str(centre_haut)
        sshRasp.exec_command(commandeBas)
        sshRasp.exec_command(commandeHaut)
        print ("activation robot OK")
    except:
        print("Activation robot échouée")
    return jsonify("Activ ok")

#Fonction rapidité de mouvements du robot (coefficients multiplicateurs)
@app.route('/vitesseCameraLent')
def functionVitesseCameraLent():
    """
       Fonction qui gère la vitesse de rotation des servo moteur, ici elle passe en vitesse lente.
       La vitesse de déplacement est miltipliée par 1 pour le servo supérieur comme pour le servo 
       inférieur.
    """
    print("vitesse lent")
    global coefVitesseBas
    global coefVitesseHaut
    coefVitesseBas=1
    coefVitesseHaut=1
    return jsonify("")

@app.route('/vitesseCameraNormal')
def functionVitesseCameraNormal():
    """
       Fonction qui gère la vitesse de rotation des servo moteur, ici elle passe en vitesse normale.
       La vitesse de déplacement est miltipliée par 3 pour le servo supérieur et par 5 pour le servo 
       inférieur.
    """
    print("vitesse normal")
    global coefVitesseBas
    global coefVitesseHaut
    coefVitesseBas=5
    coefVitesseHaut=3
    return jsonify("")

@app.route('/vitesseCameraRapide')
def functionVitesseCameraRapide():
    """
       Fonction qui gère la vitesse de rotation des servo moteur, ici elle passe en vitesse rapide.
       La vitesse de déplacement est miltipliée par 6 pour le servo supérieur et par 10 pour le servo 
       inférieur.
    """
    print("vitesse rapide")
    global coefVitesseBas
    global coefVitesseHaut
    coefVitesseBas=10
    coefVitesseHaut=6
    return jsonify("")
    
#Fait tourner le robot vers le haut
@app.route('/moveRobotHautHaut')
def functionMoveRobotHautHaut():
    """
       Cette fonction a pour but de faire pivoter le servo supérieur vers le haut, la vitesse de deplacement
       va dependre si l'utilisateur la modifie, sinon c'est la vitesse "normale" qui est utilisee.
       Si le servo est en butee, alors la fonction ne va pas continuer de se déplacer dans ce sens et va en 
       informer le javascript.
    """
    try:
        global centre_haut
        global coefVitesseHaut
        if not((centre_haut-(decalage_haut*coefVitesseHaut)) <= min_haut):
            centre_haut -= decalage_haut*coefVitesseHaut
            commande1 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotHaut.py '+str(centre_haut)
            sshRasp.exec_command(commande1)
            print(centre_haut)
            print("vers le haut")
            move_haut_haut = "ok"
        
        else:
            centre_haut = min_haut
            commande1 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotHaut.py '+str(centre_haut)
            sshRasp.exec_command(commande1)
            print(centre_haut)
            print("butté en haut")
            move_haut_haut = "no"
    except:
        print("vers le haut échoué")
    return jsonify(move_haut_haut)

#Fait tourner le robot vers le bas
@app.route('/moveRobotHautBas')
def functionMoveRobotHautBas():
    """
       Cette fonction a pour but de faire pivoter le servo supérieur vers le bas, la vitesse de deplacement
       va dependre si l'utilisateur la modifie, sinon c'est la vitesse "normale" qui est utilisee.
       Si le servo est en butee, alors la fonction ne va pas continuer de se déplacer dans ce sens et va en 
       informer le javascript.
    """
    try:
        global centre_haut
        global coefVitesseHaut
        if not((centre_haut+(decalage_haut*coefVitesseHaut)) >= max_haut):
            centre_haut += decalage_haut*coefVitesseHaut
            commande2 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotHaut.py '+str(centre_haut)
            sshRasp.exec_command(commande2)
            print(centre_haut)
            print("vers le bas")
            move_haut_bas = "ok"
        else:
            centre_haut = max_haut
            commande2 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotHaut.py '+str(centre_haut)
            sshRasp.exec_command(commande2)
            print(centre_haut)
            print("butté en bas")
            move_haut_bas = "no"
    except:
        print("vers le bas échoué")
    return jsonify(move_haut_bas)    
 
#Fait tourner le robot vers la droite 
@app.route('/moveRobotBasDroite')
def functionMoveRobotBasDroite():
    """
       Cette fonction a pour but de faire pivoter le servo inferieur vers la droite, la vitesse de deplacement
       va dependre si l'utilisateur la modifie, sinon c'est la vitesse "normale" qui est utilisee.
       Si le servo est en butee, alors la fonction ne va pas continuer de se déplacer dans ce sens et va en 
       informer le javascript.
    """
    try:
        global centre_bas
        global coefVitesseBas
        if not((centre_bas-(decalage_bas*coefVitesseBas)) <= min_bas):
            centre_bas -= decalage_bas*coefVitesseBas
            commande3 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotBas.py '+str(centre_bas)
            sshRasp.exec_command(commande3)
            print(centre_bas)
            print("tourne à droite")
            move_bas_droite = "ok"
        else:
            centre_bas = min_bas
            commande3 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotBas.py '+str(centre_bas)
            sshRasp.exec_command(commande3)
            print(centre_bas)
            print("butté à droite")
            move_bas_droite = "no"
    except:
        print("tourne à droite échoué")
    return jsonify(move_bas_droite);

#Fait tourner le robot vers la gauche    
@app.route('/moveRobotBasGauche')
def functionMoveRobotBasGauche():
    """
       Cette fonction a pour but de faire pivoter le servo inferieur vers la gauche, la vitesse de deplacement
       va dependre si l'utilisateur la modifie, sinon c'est la vitesse "normale" qui est utilisee.
       Si le servo est en butee, alors la fonction ne va pas continuer de se déplacer dans ce sens et va en 
       informer le javascript.
    """
    try:
        global centre_bas
        global coefVitesseBas
        if not((centre_bas+(decalage_bas*coefVitesseBas)) >= max_bas):
            centre_bas += decalage_bas*coefVitesseBas
            commande4 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotBas.py '+str(centre_bas)
            sshRasp.exec_command(commande4)
            print(centre_bas)
            print("tourne à gauche")
            move_bas_gauche = "ok"
        else:
            centre_bas = max_bas
            commande4 = 'python '+cheminTravailPi+'/scripts_python/1-activeRobotBas.py '+str(centre_bas)
            sshRasp.exec_command(commande4)
            print(centre_bas)
            print("butté à gauche")
            move_bas_gauche = "no"
    except:
        print("tourne à gauche échoué")
    return jsonify(move_bas_gauche)

#-------------- Fonctions automatiquement lancee au chargement du navigateur --------
@app.route('/')
def connectionSsh():
    """
        Fonction qui se lance automatiquement lors du chargement du navigateur
        Se connecte à la raspebrry pi et au serveur de calculs, lance l'activation du robot et le retour video
        Retourne l'état de connection ssh de la raspberry pi et le serveur de calculs dans la génération du fichier html via Flask (Ok ou NO )
        Retourne dans le terminal Python les états de connection des ssh
    """
    # Informations de connection aux ssh
    global cheminMain
    valeursDico = dict()
    filename = cheminMain+"config.txt"
    with open(filename, "r") as file:
        for line in file:
            try:
                name, valeurDico = line.split(":")
                valeursDico[name.strip()] = valeurDico.strip()
            except: #permet de gerer ce qui n'est pas des renseignements, comme des explication ou les titres
                pass
    ipRasp=valeursDico["ipRasp"]
    usernameRasp=valeursDico["userNameRasp"]
    passeRasp=valeursDico["passeRasp"]
    ipServeur=valeursDico["ipServeur"]
    usernameServeur=valeursDico["userNameServeur"]
    passeServeur=valeursDico["passeServeur"]
    # Si la connection à la raspberry pi fonctionne on fait ...
    try:
        sshRasp.connect(ipRasp, username=usernameRasp, password=passeRasp)
        ConnectRasp = "OK"
        functionInitDossierPhotoRasp()
        functionRetourVideoAcqui()
        functionActivRobot()
        print("Connection SSH rasp OK")
        # Si la connection au serveur fonctionne on fait ...
        try:
            sshServ.connect(ipServeur, username=usernameServeur, password=passeServeur)
            ConnectServ = "OK" 
            print("Connection SSH serveur OK")
            return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)
        # Si la connection au serveur NE fonctionne PAS on fait ...
        except:
            ConnectServ = "NO" 
            print("Connection SSH serveur Failed")
            return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)
    # Si la connection à la raspberry pi NE fonctionne PAS on fait ...
    except (paramiko.SSHException, TimeoutError):
        # Si la connection au serveur fonctionne on fait ...
        try: 
          sshServ.connect(ipServeur, username=usernameServeur, password=passeServeur)
          ConnectServ = "OK"
          ConnectRasp = "NO" 
          print("Connection SSH rasp Failed mais serveur OK")
          return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)
        # Si la connection au serveur NE fonctionne PAS on fait ...
        except: 
            ConnectServ = "NO"
            ConnectRasp = "NO"
            print("Connection SSH rasp et serveur Failed")
            return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)
        # on renvoie le résultat des connections à la page html (qui est crée au même moment)
        return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)
        quit()
    return render_template('accueil.html', titre="RaspiModel", ConnectRasp = ConnectRasp, ConnectServ = ConnectServ)

#-------------- Acquisition --------  
def functionAcquisition(temps):
    """
       Fonction permetant de lancer le script d'acquisition de la raspberry via ssh.
       Le temps qui est passé en paramètre est envoyé à la raspberry pi pour acquerir
       le bon nombre de secondes.
    """
    functionFinRetourVideoAcqui()
    photos = "bash "+cheminTravailPi+"/scripts_python/raspistillAcqui.bash "+ str(temps)
    sshRasp.exec_command(photos)
    
@app.route('/acquisition5')
def time5():
    """
        Cette fonction sert d'intermédiaire entre le javascript et la fonction ssh 
        envoyee a la raspberry pi. La fonction en elle meme est un paramètre pour la 
        fonction "functionAcquisition()" en envoyant le paramètre 5 pour une acquisition
        de 5 secondes.
    """
    functionAcquisition(5)
    return jsonify("")
    
@app.route('/acquisition10')
def time10():
    """
        Cette fonction sert d'intermédiaire entre le javascript et la fonction ssh 
        envoyee a la raspberry pi. La fonction en elle meme est un paramètre pour la 
        fonction "functionAcquisition()" en envoyant le paramètre 10 pour une acquisition
        de 10 secondes.
    """
    functionAcquisition(10)
    return jsonify("")
    
@app.route('/acquisition15')
def time15():
    """
        Cette fonction sert d'intermédiaire entre le javascript et la fonction ssh 
        envoyee a la raspberry pi. La fonction en elle meme est un paramètre pour la 
        fonction "functionAcquisition()" en envoyant le paramètre 15 pour une acquisition
        de 15 secondes.
    """
    functionAcquisition(15)
    return jsonify("")

#-------------- Calculs --------  
def finCalculs():
    """
        La fonction va tester toutes les 5 secondes si le calculs micmac est terminé en "regardant"
        dans le dossier de travail sur le serveur de calculs si le fichier fin.txt ou Erreur.txt existe.
        Si c'est le cas le fichier arret.txt est créé dans le dossier de travail de la raspberry pi et la fonction
        retourne un bouleen si une erreur est survenue. Sinon le script attend 5 secondes et boucle.
    """
    time.sleep(15)
    fini = False
    erreurMicmac = False
    motFin = "'fin.txt'"
    motErreur= "'Erreur.txt'"
    while (fini == False):
        print("verif en cours")
        ssh_stdin, ssh_stdout, ssh_stderr = sshServ.exec_command("cd "+cheminTravailServeurCalculs+"/ && ls")
        for line in ssh_stdout.read().splitlines():
            mot = str(line)[1:]
            if (motFin == mot):
                fini = True
                print('fin calculs')
            if (motErreur == mot):
                erreurMicmac = True
                fini = True
                print("erreur avec micmac")
        print(erreurMicmac)
        if (fini == False):
            print("en attente")
            time.sleep(5)
    sshRasp.exec_command('echo "arret" > '+cheminTravailPi+'/arret.txt')
    return (erreurMicmac)
    
@app.route('/calculs')
def functionCalculs():
    """
        Cette fonction lance le calcul micmac, la verification des erreur, et le retour video 
        pendant les calculs le tout en SSH.
        Elle va aussi lancer la fonction "finCalculs()" pour verifier si une erreur est survenue 
        et renvoye la réponse de la fonction (un bouleen) au javascript via jsonify.
    """
    micmac = "sh "+cheminTravailServeurCalculs+"/micmac_rasp.sh "+cheminTravailServeurCalculs+" "+cheminTravailPi
    print(micmac)
    verif = "python "+cheminTravailServeurCalculs+"/verif_micmac.py "+cheminTravailServeurCalculs
    ssh_stdinR, ssh_stdoutR, ssh_stderrR = sshRasp.exec_command("python "+cheminTravailPi+"/scripts_python/raspistillRetourVideo.py")
    functionRetourVideoAcquiServeur()
    ssh_stdin, ssh_stdout, ssh_stderr = sshServ.exec_command(micmac)
    ssh_stdinV, ssh_stdoutV, ssh_stderrV = sshServ.exec_command(verif)
    reponse = finCalculs()
    # print("erreur et out micmac")
    # for lineErr in ssh_stderr.read().splitlines():
        # print(lineErr)
    # for lineOut in ssh_stdout.read().splitlines():
        # print(lineOut)
    # print("erreur et out verif")
    # for lineErrV in ssh_stderrV.read().splitlines():
        # print(lineErrV)
    # for lineOutV in ssh_stdoutV.read().splitlines():
        # print(lineOutV)
    # print("erreur et out retourVideo")
    # for lineErrR in ssh_stderrR.read().splitlines():
        # print(lineErrR)
    # for lineOutR in ssh_stdoutR.read().splitlines():
        # print(lineOutR)
    
    return jsonify(reponse);

#-------------- Activation d'un element html --------  
@app.route('/reactiv_element')
def reactiv_element_function():
    """
        Fonction renvoyant un string vide
        Est utilisé pour activer un element html en remplacant la classe pas rien et donc retirer
        l'element hide lorsqu'il est le seul paramètre dans "classe"
    """
    result = ""
    return jsonify(result=result)  

#-------------- Extinction de la rasberry pi --------      
@app.route('/eteindreRasp')
def functionDesactiveRasp():
    """
        Cette fonction envoie une commade ssh a la raspberry pi pour l'eteindre. Elle va retourner au javascript
        le rapport "rasberry eteinte".
    """
    eteindre = "sudo shutdown now"
    sshRasp.exec_command(eteindre)
    print("Raspberry pi Eteinte")
    return jsonify("raspberry eteinte");
 
 
#if __name__ == '__main__':
app.run(debug=True)