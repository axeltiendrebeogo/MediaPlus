<?php
/*ce fichier contient toutes les informations necessaires à la connexion à la base de donnée comme le nom de la base de donnée
le nom d'utilisateur de la base de donnée et le mot de passe pour y accéder */
    $databaseName = 'pgsql:host=localhost;port=5432;dbname=MediaDatabase';//le nom de la base de donnée à se connecter
    $databaseUsername = 'postgres';//le nom de l'utilisateur pouvant se connecter à la base de donnée
    $databaseUserPassword = 'epo';//le mot de passe de l'utilisateur pour se connecter à la base de donnée
/*Ce fichier sera inclut dans tous les autres fichiers PHP qui auront besoin de se connecter à la base de données */
?>
