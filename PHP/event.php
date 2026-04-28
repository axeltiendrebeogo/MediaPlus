<?php
//la partie du script PHP qui se charge d'envoyer dans la base de donnée les informations relatifs au évènements

    function sendEventDataToDatabase($eventType){
        //on commence d'abord par créer le pdo et à ce connecter à la base de donnée
        include_once("database_info.php");//on charge en une seule fois les informations
        try{
        $database = new PDO($databaseName,$databaseUsername,$databaseUserPassword,[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        }
        catch(Exception $e){
            die('Erreur : '.$e->getMessage());
        }
        //maintenant on exécute les différentes requêtes en fonction du type d'évènement
        if($eventType == 'click'){
            $sqlCode = 'INSERT INTO Event(type, date_event) VALUES(:type, :date_event)';//pour le moment stockons juste le type d'evènement et la date ou elle s'est réalisée
            $sqlRequest = $database->prepare($sqlCode);//on prepare la requete sql
            $dataToSend = json_decode(file_get_contents("php://input"), true);//on recupère les informations à envoyer
            $sqlRequest->execute([':type' => $dataToSend['type'], ':date_event' => $dataToSend['date_event']]);
        }
    }
    
    //on fait maintenant appel maintenant à notre méthode chargé d'envoyer les données
    sendEventDataToDatabase($_GET['phpRequest']);
?>