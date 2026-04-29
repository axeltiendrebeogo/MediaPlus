<?php
/*Le fichier init.php contient le code php à éxécuter dès qu'on nouveau visiteur arrive sur le site web du média
**Il créé d'abord un nouveau champ dans la table visiteur de la base de donnée
**Il retourne au fichier init.js l'id du dernier visiteur ajouté à la base de donnée. */
	require_once __DIR__ . '/cors.php';
    include_once("database_info.php");/*On inclut les informations necessaires à la connexion à la base de donnée */
    try{
        $database = new PDO($databaseName,$databaseUsername,$databaseUserPassword,[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        /* [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION] permet d'afficher les erreurs si le sql est mal écrit*/
    }
    catch(Exception $e){
        die('Erreur : '.$e->getMessage());
    }

    //on va créer le script sql qui va permettre d'envoyer les informations de base sur le visiteur
    $sqlCode = 'INSERT INTO Visitor(date_arrivee, longitude, laltitude, device_type, os, ip_adress, navigator) VALUES(:date_arrivee, :longitude, :laltitude, :device_type, :os, :ip_adress, :navigator)';//la requete qui va envoyer les informations à la base de donnée
    $dataToSend = json_decode(file_get_contents("php://input"), true);//on recupère les données envoyés par le init.js
    $sqlRequest = $database->prepare($sqlCode);//on reparer la requête sql
    $sqlRequest->execute([':date_arrivee' => $dataToSend['date_arrivee'], ':longitude' => $dataToSend['longitude'],':laltitude' => $dataToSend['laltitude'],':device_type' => $dataToSend['device_type'],':os' => $dataToSend['os'],':ip_adress' => $dataToSend['ip_adress'],':navigator' => $dataToSend['navigator']]);//la requête qui va envoyer les données à la base de donnée

    $sqlCode = 'SELECT id_visitor FROM Visitor ORDER BY id_visitor DESC LIMIT 1';//le code sql qui retourne l'id du visiteur
    $sqlRequest = $database->prepare($sqlCode);/*La requête sql qui sera exécuté */
    $sqlRequest->execute();//on éxécute la requête SQL

    $sqlRequestResults = $sqlRequest->fetch(PDO::FETCH_ASSOC);//on recupère le résultat de la requête sql
    header('Content-Type: application/json');// on dit au navigateur qu'il s'agit que c'est du JSON
    echo json_encode($sqlRequestResults);//on envoie le resultat de la requête au format JSON à js

?>
