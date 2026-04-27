//le code javascript qui sera à chaque fois qu'un nouveau visiteur arrive dans le site web
//--on commence par récuperer les informations qui seront envoyés à la base de donnée
//--on créé une session storage qui va contenir l'id du visitor dans la base de donnée

function initialize(){//cette fonction d'initialiser va se charger d'initialiser
    if(window.XMLHttpRequest){
        var request = new XMLHttpRequest();//on créé une nouvelle requête requestrequestRequest
    }
    else{
        var request = new ActiveXObject("Microsoft.XMLHTTP");//pour les navigateurs IE5 et IE6
    }
    
    request.onload = function(){
        //le code qui va s'exécuter si la requête est prête
        if(request.status == 200){//si la requête s'est bien exécutée
            let etudiants = JSON.parse(request.responseText);
            for(let etudiant of etudiants){
                document.writeln(etudiant.nom + " "+ etudiant.prenom + " " + etudiant.matricule+ " <br>");
            }
        }
        else{
            //sinon il y a erreur
            alert("Erreur");
        }
    }

    //essayons d'envoyer des données à la base de donnée
    let data = {
        nom: "Jozo",
        prenom: "dhc",
        matricule: "MAT412",
        classe_id: 2
    };//Nous allons envoyé un objet à la base de donnée
    request.open("POST", "PHP/init.php");//chemin relatif à la racine du projet
    request.setRequestHeader("Content-Type", "application/json");//les informations seront envoyés sous format json
    request.send(JSON.stringify(data));//la requête est émise vers le serveur web pour être éxécuté et on passe en paramètres les données sous format JSON
}

window.onload = initialize;//on executé cette fonction dès que la page se charge