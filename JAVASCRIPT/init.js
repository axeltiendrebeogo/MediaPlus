//le code javascript qui sera à chaque fois qu'un nouveau visiteur arrive dans le site web
//--on commence par récuperer les informations qui seront envoyés à la base de donnée
//--on créé une session storage qui va contenir l'id du visitor dans la base de donnée

import { listenAllEvents } from "./event";

export function initialize(){//cette fonction d'initialiser va se charger d'initialiser
    if(sessionStorage.getItem("id_visitor") == null){//cela signifie tout simplement que c'est la première fois que le visiteur arrive sur le site web du  media
        let request = new XMLHttpRequest();//on créé une nouvelle requête requestrequestRequest
        
        request.onreadystatechange = function(){
            //le code qui va s'exécuter si la requête est prête
            if(request.readyState == 4){
                if(request.status == 200){//si la requête s'est bien exécutée
                    let result = JSON.parse(request.responseText);
                    //maintenant qu'on a eu la réponse c'est à dire l'id stockons là dans le sessionsstorage
                    sessionStorage.setItem("id_visitor", result.id_visitor);
                    sessionStorage.setItem("id_pageweb", result.id_pageweb);
                    listenAllEvents();//je me mets maintenant à tout écouter
                }
            } 
        }
        let visitorData = {
            platform : navigator.userAgent, //retourne le nom du navigateur utilisé pour se connecter
            langue : navigator.language, //la langue utilisé
            url : window.location.href,//on recupère l'url de la page sur laquelle l'utilisateur se trouve
            id_media : sessionStorage.getItem("id_media")//l'id du media
        };//on envoie ces données relatifs au visiteur et à la base de donnée

        //maintenant que toutes les données ont été recoltés on envoie les données dans la base de données
        request.open("POST", "PHP/init.php");//chemin relatif à la racine du projet
        request.setRequestHeader("Content-Type", "application/json");//les informations seront envoyés sous format json
        request.send(JSON.stringify(visitorData));//la requête est émise vers le serveur web pour être éxécuté et on passe en paramètres les données sous format JSON
    }
    else{
        //alert("id existe déjà et le voilà : "+ sessionStorage.getItem("id_visitor"));
    }
}
