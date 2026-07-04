//c'est le fichier js qui sera importé comme script dans le code html des sites web media
import { initialize } from "./init.js";//on importe la function qui initialiser le tout
import { listenAllEvents } from "./event.js";//on importe la functionchargé d'écouter tous les évènements

//on recupère d'abord l'id du media
const scriptUrl = new URL(import.meta.url);//on recupère l'url total de l'url qui contient 
const id_media = scriptUrl.searchParams.get("id_media");

if(!id_media){
    alert("Error");
}
else{
    sessionStorage.setItem("id_media", id_media);//on stocke l'identifiant du media dans la sessionStorage
}
//dès qu'on a fini d'importer les fonctions, on lance l'initialisation
initialize();
//listenAllEvents();//on appel cette méthode
