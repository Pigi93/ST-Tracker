<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="description" content="index">
        <meta name="author" content="Fabbro Pierluigi">
        <title>Batteria</title>
        <link rel="stylesheet" type="text/css" href="mystyle.css">
        <link rel="icon"  type="image/jpg" href="timer.jpg">
    </head>
    
    <body>
        
        <div class="header">
        <h1>Batteria</h1>
        </div>
        
        <ul id="menu">
                <li><a href="index.php">Attività giornaliera</a></li>
                <li><a href="daily_activities.php">Registro attività</a></li>
                <li class="active"><a href="battery.php">Batteria</a></li>
                <li><a href="contacts.html">Contatti</a></li>
        </ul>
        
        <div class="content">
            <div class="task">
                <?php
                    $conn = mysqli_connect("localhost", "phpmyadmin", "BernardiniLab", "labud19");
                    if ($conn->connect_error) 
                    {
                        die("Connection failed: " . $conn->connect_error);
                    }
                    $sql = "SELECT * FROM battery_status";
                    $result = $conn->query($sql);
                    if ($result->num_rows > 0) 
                    {
                        while($row = $result->fetch_assoc()) 
                        {
                            echo "<p>Tensione:      " . $row["voltage"] . "V</p>" .
                                 "<p>Percentuale:   " . $row["percentage"] . "%</p>";
                        }
                    }
                    $conn->close();
                ?>
            </div>
        </div>

        <div class="footer">
            Created by Pierluigi Fabbro and Riccardo Deana - 2020
        </div>
    </body>

</html>
