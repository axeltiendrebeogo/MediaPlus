//le script js qui va se charger d'intercepter les différents évènements de la page web et d'envoyer

/*On commence par définir les functions utiles */
function sendEventDataToDatabase(eventData, eventType){
    //on commence par créer un objet de type XMLHttpRequest
    const request = new XMLHttpRequest();//un nouveau objet de type http request

    request.onload = function(){
        //quoi faire lorsque la fonction a fini son exécution
        if(request.status == 200){
            //let result = JSON.parse(request.responseText);//on recupère le resultat
            //alert("voici le résultat de la requête " + result.response);
        }
    }
    request.open("POST", "PHP/event.php?phpRequest=" + eventType);//chemin relatif à la racine du projet
    //requete permet de passer des arguments au script php et d'éxécuter différente tâche en fonction des arguments passés au script
    request.setRequestHeader("Content-Type", "application/json");//les informations seront envoyés sous format json
    request.send(JSON.stringify(eventData));//on envoie les données
}

function sendClickEventData(){//fonction qui sera exécuté en cas de clique d'un bouton
    let data = {
        type : "click",
        date_event: "2026-07-12"
    };
    sendEventDataToDatabase(data,"click");//on envoie maintenant les données à la base de donnée
}

/*Fin de la partie de définition des functions */
const buttons = document.querySelectorAll("button");//document.querySelector va nous permettre de selections tous les buttons de notre page html

for(let btn of buttons){
    btn.addEventListener("click", sendClickEventData);//A chaque clique d'un bouton on envoi les données à la base de donnée
}

sendEventDataToDatabase(data, "hello");