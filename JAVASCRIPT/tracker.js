//c'est le fichier js qui sera importé comme script dans le code html des sites web media
//alert("Salut");
import { initialize } from "http://172.16.9.53/init.js";//on importe la function qui initialiser le tout
import { listenAllEvents } from "http://172.16.9.53/event.js";//on importe la functionchargé d'écouter tous les évènements

//dès qu'on a fini d'importer les fonctions, on lance l'initialisation
initialize();
listenAllEvents();//on appel cette méthode
