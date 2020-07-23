<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="description" content="registro attività">
        <meta name="author" content="Fabbro Pierluigi">
        <title>Registro attività</title>
        <link rel="stylesheet" type="text/css" href="mystyle.css">
        <link rel="icon"  type="image/jpg" href="timer.jpg">
    </head>
    
    <body>
        
        <div class="header">
        <h1>Registro attività</h1>
        </div>
        
        <ul id="menu">
                <li><a href="index.php">Attività giornaliera</a></li>
                <li><a href="daily_activities.php">Registro attività</a></li>
                <li><a href="battery.php">Batteria</a></li>
                <li><a href="contacts.html">Contatti</a></li>
        </ul>
        
        <div class="content">
            <div class="task">
                <?php
                    $conn = mysqli_connect("localhost", "phpmyadmin", "BernardiniLab", "labud19");
                    // Check connection
                    if ($conn->connect_error) 
                    {
                        die("Connection failed: " . $conn->connect_error);
                    }
                    $sql = "DELETE FROM daily_activities;";
                    $result = $conn->query($sql);
                    $conn->close();
                ?>
                <p>Registro resettato con successo.</p>
            </div>            
        </div>

        <div class="footer">
            Created by Pierluigi Fabbro and Riccardo Deana - 2020
        </div>
    </body>
</html>