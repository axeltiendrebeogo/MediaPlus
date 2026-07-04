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

    $realIpAddress = $_SERVER['REMOTE_ADDR'];
    //on va créer le script sql qui va permettre d'envoyer les informations de base sur le visiteur
    $sqlCode = 'INSERT INTO Visitor(date_visite, platform, langue, ip_address) VALUES(NOW(), :platform, :langue, :ip_address)';//la requete qui va envoyer les informations à la base de donnée
    $dataToSend = json_decode(file_get_contents("php://input"), true);//on recupère les données envoyés par le init.js
    $sqlRequest = $database->prepare($sqlCode);//on reparer la requête sql
    $succes = $sqlRequest->execute([
        ':platform' => $dataToSend['platform'],
        ':langue' => $dataToSend['langue'],
        ':ip_address' => $realIpAddress, //parce que javascript ne permet d'obtenir l'adresse ip
    ]);//la requête qui va envoyer les données à la base de donnée

    if($succes){//si tout c'est bien passé

        $lastId = $database->lastInsertId();//retourne l'id du dernier élément inséré

        //maintenant on doit chercher à recupérer l'id de la page web
        $sqlCode = 'SELECT id_pageweb FROM pageweb where url = :url';
        $sqlRequest = $database->prepare($sqlCode);
        $sqlRequest->execute([':url' => $dataToSend['url']]);
        $pageWeb_id = $sqlRequest->fetch(PDO::FETCH_ASSOC);//nous retourne le résultat de la commande

        if($pageWeb_id === false){//dans le cas contraire on envoie la donnée dans la base de donnée
            $sqlCode = 'INSERT INTO pageweb(id_media, url, collecte_le) VALUES(:id_media, :url, NOW())';
            $sqlRequest = $database->prepare($sqlCode);//on prepare la requête
            $sqlRequest->execute([
                ':id_media' => $dataToSend['id_media'],
                ':url' => $dataToSend['url']]);
            $lastPageWebAddId = $database->lastInsertId();//l'id du dernier élément ajouté
            $response = ["id_visitor" => $lastId,"id_pageweb" => $lastPageWebAddId];
        }
        else{//si l'url existe dejà dans la base de donnée pas la peine de l'ajouter
            $response = ["id_visitor" => $lastId, "id_pageweb" => $pageWeb_id['id_pageweb']];
        }
        header('Content-Type: application/json');// on dit au navigateur qu'il s'agit que c'est du JSON
        echo json_encode($response);//on envoie le resultat de la requête au format JSON à js
    }
    else{
        http_response_code(500);//le numéro de retour d'erreur
        header('Content-Type: application/json');// on dit au navigateur qu'il s'agit que c'est du JSON
        echo json_encode(['status' => 'error', 'message' => 'insertion échouée']);
    }
?>
