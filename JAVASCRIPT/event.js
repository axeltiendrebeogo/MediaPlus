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

function sendClickEventData(val){//fonction qui sera exécuté en cas de clique d'un bouton ou d'un lien
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : 1, //une constante pour le moment,
        event_type : "click",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : val // contient soit url si c'est un lien ou le libellé si c'est un bouton
    };
    sendEventDataToDatabase(data,"click");//on envoie maintenant les données à la base de donnée
}

function sendPageLoadData(){//fonction qui recolte le moment d'arrivé du visiteur et l'envoie à la base de donnée
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "pageLoad",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : "page chargé" //ici value ne contient rien par défaut
    };
    sendEventDataToDatabase(data,"loadPage");//envoie les données à la base de donnée
}

let isDataSend = false;//flag pour savoir si les données ont été envoyés

function sendPageExitData(){//fonction qui recolte la date du moment ou le visiteur quitte la page et envoie à la base de donnée
    if(isDataSend){
        return 0;
    }
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor") || 1,//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "pageExit",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : "page quitté" //ici value ne contient rien par défaut
    };
    //sendEventDataToDatabase(data,"exitPage");//envoie les données à la base de donnée
    if(document.visibilityState === 'hidden'){
        let blob = new Blob([JSON.stringify(data)], {type : 'application/json'});
        navigator.sendBeacon( "PHP/event.php?phpRequest=" + data.event_type, blob);
        isDataSend = true;//on a envoyé les données
    }
}

function sendVideoPlayData(videoInfo){//fonction qui envoie les données quand le visiteur lance une vidéo
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "playVideo",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : videoInfo,//les informations sur la vidéo
    };
    sendEventDataToDatabase(data,"playVideo");//envoie les données à la base de donnée
}

function sendVideoPauseData(videoInfo){//fonction qui envoie les données quand le visiteur met une vidéo en pause
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "stopVideo",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : videoInfo,//les informations sur la vidéo
    };
    sendEventDataToDatabase(data,"stopVideo");//envoie les données à la base de donnée
}

function sendVideoEndData(videoInfo){//fonction qui envoie les données quand un user fini une vidéo
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "endVideo",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : videoInfo,//les informations sur la vidéo
    };
    sendEventDataToDatabase(data,"endVideo");//envoie les données à la base de donnée
}

function sendCopyTextData(){//fonction quand le visiteur copie un texte dans la page
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "copyText",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : window.getSelection().toString(),//les informations sur le texte copié
    };
    sendEventDataToDatabase(data,"copyText");//envoie les données à la base de donnée
}

const depthsReached = new Set();
function sendScrollDephData(){//fonction qui envoie des informations sur la profondeur de scroll
    const scrolled = window.scrollY + window.innerHeight;//la valeur du scroll
    const total = document.documentElement.scrollHeight;//la taille du document
    const percent = Math.round((scrolled / total) * 100);

    if(total <= window.innerHeight){//si la page est trop longue on ne fait rien
        return;
    }

    [25, 50, 75, 100].forEach(d => {
        if (percent >= d && !depthsReached.has(d)) {
            depthsReached.add(d);
            let data = {
            id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
            id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
            event_type : "scroll",//le type d'évènement qui s'est produit
            date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
            valeur : d,//les informations sur la vidéo
        };
        sendEventDataToDatabase(data,"scroll");//envoie les données à la base de donnée
        }
    });
}

function sendFormSubmitData(formInfo){//fonction qui envoie des informations lorque l'on envoie un formulaire
    let data = {
        id_visitor : sessionStorage.getItem("id_visitor"),//l'id du visiteur
        id_pageweb : sessionStorage.getItem("id_pageweb"), //une constante pour le moment,
        event_type : "formSubmit",//le type d'évènement qui s'est produit
        date_interaction : new Date().toISOString(),//on recupère la date et l'heure exacte ou lévènement s'est produit
        valeur : formInfo,//les informations sur la vidéo
    };
    sendEventDataToDatabase(data,"formSubmit");//envoie les données à la base de donnée
}

/*Fin de la partie de définition des functions */

//on va definir la fonction qui se charge d'écouter tous les évènements
export function listenAllEvents(){//c'est la fonction qui se charge d'écouter tous les évènements
    const buttonsAndLinks = document.querySelectorAll("button, a");//document.querySelector va nous permettre de selections tous les buttons et liens de notre page html

    for(let comp of buttonsAndLinks){
        comp.addEventListener("click", function(e){
            const libelle = e.target.innerText || e.target.value || "inconnu";
            const url = e.target.href || null;
            if(url == null){
                sendClickEventData(libelle);//on envoie les informations sur le lien ou le bouton appuyé
            }
            else if(url != null){
                sendClickEventData(url);//on envoie les informations sur le lien ou le bouton appuyé
            }
        });
    }

    const videos = document.querySelectorAll("video");//recupère tous les sélecteurs de type video
    for(let video of videos){
        const videoInfo = video.title || video.src || video.currentSrc || "inconnu";
        video.addEventListener("play", ()=>{
           sendVideoPlayData(videoInfo);
        });

        video.addEventListener("pause", ()=>{
           sendVideoPauseData(videoInfo);
        });

        video.addEventListener("ended", ()=>{
           sendVideoEndData(videoInfo);
        });
    }

    const forms = document.querySelectorAll("form");//selectionne tous les formulaires
    for(let form of forms){
        const formInfo = form.id || form.action || "formulaire";
        form.addEventListener("submit", ()=>{
            sendFormSubmitData(formInfo);
        });
    }
    //lors du chargement de la page
    sendPageLoadData();//lors du chargement de la page
    //lorsque l'utilisateur quitte la page
    document.addEventListener('visibilitychange', sendPageExitData);//lorqu'il quitte la page
    document.addEventListener("copy", sendCopyTextData);
    window.addEventListener("scroll", sendScrollDephData);//scroll
}
