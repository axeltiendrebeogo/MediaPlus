<?php
//la partie du script PHP qui se charge d'envoyer dans la base de donnée les informations relatifs au évènements
	require_once __DIR__ . '/cors.php';
    function sendEventDataToDatabase($eventType){
        //on commence d'abord par créer le pdo et à ce connecter à la base de donnée
        include_once("database_info.php");//on charge en une seule fois les informations
        try{
        $database = new PDO($databaseName,$databaseUsername,$databaseUserPassword,[PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        }
        catch(Exception $e){
            die('Erreur : '.$e->getMessage());
        }

        $sqlCode = 'INSERT INTO Interactions(id_visitor, id_pageweb, event_type, date_interaction, valeur) VALUES(:id_visitor, :id_pageweb, :event_type, :date_interaction, :valeur)';//pour le moment stockons juste le type d'evènement et la date ou elle s'est réalisée
        $sqlRequest = $database->prepare($sqlCode);//on prepare la requete sql
        $dataToSend = json_decode(file_get_contents("php://input"), true);//on recupère les informations à envoyer
        $sqlRequest->execute([
            ':id_visitor' => $dataToSend['id_visitor'], 
            ':id_pageweb' => $dataToSend['id_pageweb'],
            ':event_type' => $dataToSend['event_type'],
            ':date_interaction' => $dataToSend['date_interaction'],
            ':valeur' => $dataToSend['valeur'],
        ]);
    }
    //on fait maintenant appel maintenant à notre méthode chargé d'envoyer les données
    sendEventDataToDatabase($_GET['phpRequest']);
?>
