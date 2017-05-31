// Initialisation des variables
var paragrapheConnectionRasp = document.getElementById("ConnectRasp");
var paragrapheConnectionServ = document.getElementById("ConnectServ");
var btnCommencer = document.getElementById("btnCommencer");
var valeurParagrapheConnectionRasp = paragrapheConnectionRasp.innerText;
var valeurParagrapheConnectionServ = paragrapheConnectionServ.innerText;
var valeurConnectionRasp = valeurParagrapheConnectionRasp.substring(valeurParagrapheConnectionRasp.length-2,valeurParagrapheConnectionRasp.length);
var valeurConnectionServ = valeurParagrapheConnectionServ.substring(valeurParagrapheConnectionServ.length-2,valeurParagrapheConnectionServ.length);
var couleurConnectRasp = document.getElementById("couleurConnectRasp");
var couleurConnectServ = document.getElementById("couleurConnectServ");
var SecAvantAcquisition = document.getElementById("SecAvantAcquisition");
var paragrapheDebutAcqui = document.getElementById('paragrapheDebutAcqui');
var boiteCommencer = document.getElementById("boiteCommencer");
var acquisition = document.getElementById('acquisition');
var SecFinAcquisition = document.getElementById('SecFinAcquisition');
var calculs = document.getElementById('calculs');
var loader = document.getElementById('loader');
var enjoy = document.getElementById('enjoy');
var webcam = document.getElementById('webcam');
var flecheHaut = document.getElementById('flecheHaut');
var flechebas = document.getElementById('flecheBas');
var flecheDroite = document.getElementById('flecheDroite');
var flecheGauche = document.getElementById('flecheGauche');
var btnGauche = document.getElementById("btnGauche");
var btnDroite = document.getElementById("btnDroite");
var btnHaut = document.getElementById("btnHaut");
var btnBas = document.getElementById("btnBas");
var blocChoixVitesse = document.getElementById('blocChoixVitesse');
var btnShutRasp = document.getElementById('btnShutRasp');
var delai = document.getElementById('delai');
var texteCalculs = document.getElementById('texteCalculs');
var loader = document.getElementById('loader');

// ------ JS MATERIALIZE ------
(function($){
  $(function(){

    $('.button-collapse').sideNav();

  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function() {
    $('select').material_select();
  });
// ------ FIN JS MATERIALIZE ------

//Fonction qui permet d'initialiser les boutons en fonction du statut des connexions ssh
function activPage(){
    if (valeurConnectionRasp !== "OK"){
        btnCommencer.className = "waves-effect waves-light btn valign disabled btnCommencer";
	btnShutRasp.className = "waves-effect waves-light btn disabled";
        couleurConnectRasp.className = "connexionNO";
        console.log("connexion SSH Raspberry échouée");
    }
    else if (valeurConnectionRasp == "OK"){
        couleurConnectRasp.className = "connexionOK";
        console.log("connexion SSH Raspberry ok");
    }
    if (valeurConnectionServ !== "OK"){
        btnCommencer.className = "waves-effect waves-light btn valign disabled btnCommencer";
        couleurConnectServ.className = "connexionNO";
        console.log("connexion SSH Serveur de calculs échouée");
    }
    else if (valeurConnectionServ == "OK"){
        couleurConnectServ.className = "connexionOK";
        console.log("connexion SSH Serveur de calculs ok");
    }
    
}


//lance les calculs micmac sur le serveur de calculs à partir de python et initialise l'affichage des div html
function CalculsMicmac(){
    console.log("calculs micmac");

    $(function(){
          $.getJSON($SCRIPT_ROOT + '/calculs', {
          }, function(data) {
			  if(data == true){
				// s'il y a un problème dans micmac, le bloc suivant s'affiche dans le html
				texteCalculs.innerHTML = '<i class="material-icons left">report_problem</i> Une erreur est survenue lors des calculs, veulliez recommencer <a onclick="location.reload()" id="btnReload"><i class="material-icons lienLogo">autorenew</i></a>';
				loader.className = "hide";
				webcam.className = "hide";
				btnShutRasp.className ="waves-effect waves-light btn";
			  }
			  else{
				// on affiche le bloc enjoy et le bouton pour eteindre la raspberry
				enjoy.className="";
				btnShutRasp.className ="waves-effect waves-light btn";
				// on cache le bloc calculs
				calculs.className="hide";
			  }
          });
    });
}

//Eteint la camera via python
function finCamera(){
    console.log('fin acqui');
    $(function(){
          $.getJSON($SCRIPT_ROOT + '/FinRetourVideoAcqui', {
          }, function(data) {
          });
    });
}

// lance les calculs micmac et initialise l'affichage des div html
function fonctionCalculs(){
    CalculsMicmac();
    //on affiche le bloc calculs
    calculs.className="";
    //on masque le bloc titreCapture
    titreCapture.className="hide titre-boite";
    //on masque le bloc acquisition et le retour video
    acquisition.className="hide";
    webcam.className = "center";
}

//comptes a rebours avant la fin de l'acquisition et lancement de la fonction des calculs
function attenteFin(valeur){
    if(valeur == 5){
        $("#SecFinAcquisition").text("5");
        setTimeout(function(){$("#SecFinAcquisition").text("4");}, 1000);
        setTimeout(function(){$("#SecFinAcquisition").text("3");}, 2000);
        setTimeout(function(){$("#SecFinAcquisition").text("2");}, 3000);
        setTimeout(function(){$("#SecFinAcquisition").text("1");}, 4000);
        setTimeout(function(){$("#SecFinAcquisition").text("0");}, 5000);
        setTimeout(function(){fonctionCalculs()}, 6000);
    } 
    else if(valeur == 10){
        $("#SecFinAcquisition").text("10");
        setTimeout(function(){$("#SecFinAcquisition").text("9");}, 1000);
        setTimeout(function(){$("#SecFinAcquisition").text("8");}, 2000);
        setTimeout(function(){$("#SecFinAcquisition").text("7");}, 3000);
        setTimeout(function(){$("#SecFinAcquisition").text("6");}, 4000);
        setTimeout(function(){$("#SecFinAcquisition").text("5");}, 5000);
        setTimeout(function(){$("#SecFinAcquisition").text("4");}, 6000);
        setTimeout(function(){$("#SecFinAcquisition").text("3");}, 7000);
        setTimeout(function(){$("#SecFinAcquisition").text("2");}, 8000);
        setTimeout(function(){$("#SecFinAcquisition").text("1");}, 9000);
        setTimeout(function(){$("#SecFinAcquisition").text("0");}, 10000);
        setTimeout(function(){fonctionCalculs()}, 11000);
    } 
    else if(valeur == 15){
        $("#SecFinAcquisition").text("15");
        setTimeout(function(){$("#SecFinAcquisition").text("14");}, 1000);
        setTimeout(function(){$("#SecFinAcquisition").text("13");}, 2000);
        setTimeout(function(){$("#SecFinAcquisition").text("12");}, 3000);
        setTimeout(function(){$("#SecFinAcquisition").text("11");}, 4000);
        setTimeout(function(){$("#SecFinAcquisition").text("10");}, 5000);
        setTimeout(function(){$("#SecFinAcquisition").text("9");}, 6000);
        setTimeout(function(){$("#SecFinAcquisition").text("8");}, 7000);
        setTimeout(function(){$("#SecFinAcquisition").text("7");}, 8000);
        setTimeout(function(){$("#SecFinAcquisition").text("6");}, 9000);
        setTimeout(function(){$("#SecFinAcquisition").text("5");}, 10000);
        setTimeout(function(){$("#SecFinAcquisition").text("4");}, 11000);
        setTimeout(function(){$("#SecFinAcquisition").text("3");}, 12000);
        setTimeout(function(){$("#SecFinAcquisition").text("2");}, 13000);
        setTimeout(function(){$("#SecFinAcquisition").text("1");}, 14000);
        setTimeout(function(){$("#SecFinAcquisition").text("0");}, 15000);
        setTimeout(function(){fonctionCalculs()}, 16000);
    } 
}

//Récupère la valeur du temps d'acquisition, initialise l'affichage des division html,
//eteint le retour video et le compte a rebours avant la fin de l'acquisition
function debutAcqui(){
    //on affiche le bloc début Acquisition et le retour video
    acquisition.className="";
    //on cache le paragraphe d'attente avant acquisition
    paragrapheDebutAcqui.className = "hide";
	webcam.className = "hide";
	finCamera();
    var selection = document.getElementById('choix');
    var valeur = selection.options[selection.selectedIndex].value;
    if(valeur == 5){
      $.getJSON($SCRIPT_ROOT + '/acquisition5', {
      }, function(data) {
			console.log(data);
	  });
	  attenteFin(valeur);
    }
	
    else if(valeur == 10){
        $.getJSON($SCRIPT_ROOT + '/acquisition10', {
      }, function(data) {
			console.log(data);
      });
	  attenteFin(valeur);
    }
    else if(valeur == 15){
        $.getJSON($SCRIPT_ROOT + '/acquisition15', {
      }, function(data) {
			console.log(data);
      });
	  attenteFin(valeur);
    }    
}

//compte a rebours avant le debut de l'acquisition
function attente(){
	if(document.getElementById('filled-in-box').checked == true){
		$("#SecAvantAcquisition").text("10");
		setTimeout(function(){$("#SecAvantAcquisition").text("9");}, 1000);
		setTimeout(function(){$("#SecAvantAcquisition").text("8");}, 2000);
		setTimeout(function(){$("#SecAvantAcquisition").text("7");}, 3000);
		setTimeout(function(){$("#SecAvantAcquisition").text("6");}, 4000);
		setTimeout(function(){$("#SecAvantAcquisition").text("5");}, 5000);
		setTimeout(function(){$("#SecAvantAcquisition").text("4");}, 6000);
		setTimeout(function(){$("#SecAvantAcquisition").text("3");}, 7000);
		setTimeout(function(){$("#SecAvantAcquisition").text("2");}, 8000);
		setTimeout(function(){$("#SecAvantAcquisition").text("1");}, 9000);
		setTimeout(function(){$("#SecAvantAcquisition").text("0");}, 10000);
		setTimeout(function(){debutAcqui();}, 11000);
	}
	else{
		debutAcqui();
};}
    
//le déclanche lorsque le bouton "commencer" est cliqué, initialise l'affichage des div hmtl 
//et lance le compte a rebours avec le début de l'acquisition 
function commencer(){
    //affichage du paragraphe d'attente avant acquisition
    paragrapheDebutAcqui.className = "";
    //on cache le bloc de "commencer" et le retour video
    boiteCommencer.className = "hide row sousBoite";
    webcam.className = "center";
    flecheBas.className = "hide";
    flecheHaut.className = "hide";
    flecheDroite.className = "hide";
    flecheGauche.className = "hide";
	blocChoixVitesse.className = "hide";
	//on cache le bouton pour eteindre la raspberry
	btnShutRasp.className = "hide";
	//on cache la checkbox
	delai.className="hide";
    //compte à rebours
    attente();
    
}

//lorsque le bouton "commencer" est cliqué la conftion commencer() est lancée
$(function() {
    $('a#btnCommencer').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/reactiv_element', {
      }, function(data) {
        commencer();
      });
      
      return false;
    });
  });
//Fonctions d'appel de fonctions python pour les boutons du robot 
//vitesse de déplacement de la camera

function vitesse(){
    var selection = document.getElementById('choixVitesse');
    var valeur = selection.options[selection.selectedIndex].value;
    if(valeur == 1){
        $.getJSON($SCRIPT_ROOT + '/vitesseCameraLent', {
      }, function(data) {
        console.log("vitesse Lent");
      });
    }
    else if(valeur == 2){
        $.getJSON($SCRIPT_ROOT + '/vitesseCameraNormal', {
      }, function(data) {
        console.log("vitesse Normal");
      });
    }
    else if(valeur == 3){
        $.getJSON($SCRIPT_ROOT + '/vitesseCameraRapide', {
      }, function(data) {
        console.log("vitesse Rapide");
      });
    }
    
}

//Tourner a gauche 
$(function() {
    $('a#btnGauche').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/moveRobotBasGauche', {
      }, function(data) {
            if (data == "no"){
                btnGauche.className = "disabled btnDroiteGauche btn waves-effect waves-light";
            }
            else if(data == "ok"){
                btnGauche.className = "btnDroiteGauche btn waves-effect waves-light";
                btnDroite.className = "btnDroiteGauche btn waves-effect waves-light";
            }
      });
      
      return false;
    });
  });

//Tourner a droite  
$(function() {
    $('a#btnDroite').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/moveRobotBasDroite', {
      }, function(data) {
            if (data == "no"){
                btnDroite.className = "disabled btnDroiteGauche btn waves-effect waves-light";
            }
            else if(data == "ok"){
                btnDroite.className = "btnDroiteGauche btn waves-effect waves-light";
                btnGauche.className = "btnDroiteGauche btn waves-effect waves-light";
            }
      });
      return false;
    });
  });
//Vers le haut
$(function() {
    $('a#btnHaut').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/moveRobotHautHaut', {
      }, function(data) {
            if (data == "no"){
                btnHaut.className = "disabled btn waves-effect waves-light"
            }
            else if(data == "ok"){
                btnHaut.className = "btn waves-effect waves-light"
                btnBas.className = "btn waves-effect waves-light"
            }
      });
      return false;
    });
  });
//Vers le bas
$(function() {
    $('a#btnBas').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/moveRobotHautBas', {
      }, function(data) {
            if (data == "no"){
                btnBas.className = "disabled btn waves-effect waves-light"
            }
            else if(data == "ok"){
                btnBas.className = "btn waves-effect waves-light"
                btnHaut.className = "btn waves-effect waves-light"
            }
      });
      return false;
    });
  });

//Evenement : eteindre la raspberry pi
$(function() {
    $('a#btnShutRasp').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/eteindreRasp', {
      }, function(data) {
		  paragrapheConnectionRasp.innerHTML = 'Connexion à la Raspberry Pi : <b id ="couleurConnectRasp" class="connexionNO">NO</b>';
		  btnCommencer.className = "waves-effect waves-light btn valign disabled btnCommencer";
		  btnShutRasp.className = "btn waves-effect waves-light disabled";

      });
	  
	  console.log("rasp en cours d'extinction")
	 return false;
    });
  });


//Lancement de la fonction au chargement du navigateur  
activPage();
