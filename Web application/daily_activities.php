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
                <li class="active"><a href="daily_activities.php">Registro attività</a></li>
                <li><a href="battery.php">Batteria</a></li>
                <li><a href="contacts.html">Contatti</a></li>
        </ul>
        
        <div class="content">
            <div class="task">
                <table>
                    <tr>
                        <th>Data</th>
                        <th>1</th>
                        <th>2</th>
                        <th>3</th>
                        <th>4</th>
                        <th>5</th>
                        <th>6</th>
                        <th>7</th>
                        <th>8</th>
                    </tr>
                    <?php
                        $conn = mysqli_connect("localhost", "phpmyadmin", "BernardiniLab", "labud19");
                        // Check connection
                        if ($conn->connect_error) 
                        {
                            die("Connection failed: " . $conn->connect_error);
                        }
                        $sql = "SELECT DATE_FORMAT(data,'%d/%m/%Y') AS 'data', act1, act2,  act3, act4, act5, act6, act7, act8 
                                FROM daily_activities;";
                        //$sql = "SELECT DATE_FORMAT(data,'%d/%m/%Y') AS 'data',
                        //                TIME_FORMAT(act1,'%H:%i') AS 'act1',
                        //                TIME_FORMAT(act2,'%H:%i') AS 'act2', 
                        /*                TIME_FORMAT(act3,'%H:%i') AS 'act3',
                                        TIME_FORMAT(act4,'%H:%i') AS 'act4',
                                        TIME_FORMAT(act5,'%H:%i') AS 'act5',
                                        TIME_FORMAT(act6,'%H:%i') AS 'act6',
                                        TIME_FORMAT(act7,'%H:%i') AS 'act7',
                                        TIME_FORMAT(act8,'%H:%i') AS 'act8' FROM daily_activities;";*/
                        $result = $conn->query($sql);
                        if ($result->num_rows > 0) 
                        {
                            // output data of each row
                            while($row = $result->fetch_assoc()) 
                            {
                                echo "<tr><td>" 
                                . $row["data"]. "</td><td>" 
                                . $row["act1"] . "</td><td>"
                                . $row["act2"] . "</td><td>"
                                . $row["act3"] . "</td><td>"
                                . $row["act4"] . "</td><td>"
                                . $row["act5"] . "</td><td>"
                                . $row["act6"] . "</td><td>"
                                . $row["act7"] . "</td><td>"
                                . $row["act8"]. "</td></tr>";
                            }
                            echo "</table>";
                        } 
                        $conn->close();
                    ?>
                </table>
            </div>
            
            <br/><button onclick="location.href='reset_daily_activities.php'">Reset del registro</button>
            
        </div>

        <div class="footer">
            Created by Pierluigi Fabbro and Riccardo Deana - 2020
        </div>
    </body>
</html>
