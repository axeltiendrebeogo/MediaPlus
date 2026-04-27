//le code javascript qui sera à chaque fois qu'un nouveau visiteur arrive dans le site web
//--on commence par récuperer les informations qui seront envoyés à la base de donnée
//--on créé une session storage qui va contenir l'id du visitor dans la base de donnée

function initialize(){//cette fonction d'initialiser va se charger d'initialiser
    if(sessionStorage.getItem("id_visitor") == null){//cela signifie tout simplement que c'est la première fois que le visiteur arrive sur le site web du media
        if(window.XMLHttpRequest){
            var request = new XMLHttpRequest();//on créé une nouvelle requête requestrequestRequest
        }
        else{
            var request = new ActiveXObject("Microsoft.XMLHTTP");//pour les navigateurs IE5 et IE6
        }
        
        request.onreadystatechange = function(){
            //le code qui va s'exécuter si la requête est prête
            if(request.readyState == 4 && request.status == 200){//si la requête s'est bien exécutée
                let result = JSON.parse(request.responseText);
                //maintenant qu'on a eu la réponse c'est à dire l'id stockons là dans le sessionsstorage
                sessionStorage.setItem("id_visitor", result.id_visitor);
                alert("id is " + sessionStorage.getItem("id_visitor"));
            }
            else{
                //sinon il y a erreur
                alert("Erreur");
            }
        }

        //essayons d'envoyer des données à la base de donnée
        let newVisitorData = {
            date_arrivee: "2026-04-12 14:32:21",
            longitude: -46,
            laltitude: 19,
            device_type: "ordinateur",
            os: "windows",
            ip_adress: "192.168.1.2",
            navigator: "firefox"
        };//Nous allons envoyé un objet à la base de donnée
        request.open("POST", "PHP/init.php");//chemin relatif à la racine du projet
        request.setRequestHeader("Content-Type", "application/json");//les informations seront envoyés sous format json
        request.send(JSON.stringify(newVisitorData));//la requête est émise vers le serveur web pour être éxécuté et on passe en paramètres les données sous format JSON*/
    }
    else{
        alert("id existe déjà et le voilà : "+ sessionStorage.getItem("id_visitor"));
    }
}

window.onload = initialize;//on executé cette fonction dès que la page se charge