//le script js qui va se charger d'intercepter les différents évènements de la page web et d'envoyer
const btn = document.querySelector("button");//document.querySelector permet de sélectionner qu'un seul élément

function greet(){
    alert("tu as cliqué sur le bouton hello world");
}

function link(){
    alert("Tu ne peux pas aller sur facebook");
}

function paragraph(){
    alert("Tu as double cliqué sur un paragraphe");
}

const lien = document.querySelector("a");
const par = document.querySelectorAll("p");//je recupère tous les paragraphes de ma page html

btn.addEventListener("click", greet);//écoute l'évènement de type click et exécute la function greet dans lequel cas
//je peux lier plusieurs fonction aussi
lien.addEventListener("click",link);
for(let p of par){
    p.addEventListener("dblclick",paragraph);//lorqu'on double clique
}

//on peut aussi supprimer l'écoute des évènements
btn.removeEventListener("click",greet);//permet de supprimer l'écoute des évènements

function close(){
    alert("La fenêtre va se fermer");
}

window.beforeunload = close;