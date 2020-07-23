<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="description" content="index">
        <meta name="author" content="Fabbro Pierluigi">
        <title>Attività giornaliera</title>
        <link rel="stylesheet" type="text/css" href="mystyle.css">
        <link rel="icon"  type="image/jpg" href="timer.jpg">
    </head>
    
    <body>
        
        <div class="header">
        <h1>Attività giornaliera</h1>
        </div>
        
        <ul id="menu">
                <li class="active"><a href="index.php">Attività giornaliera</a></li>
                <li><a href="daily_activities.php">Registro attività</a></li>
                <li><a href="battery.php">Batteria</a></li>
                <li><a href="contacts.html">Contatti</a></li>
        </ul>
        
        <div class="content">
            <div class="task">
                <table>
                    <tr>
                        <th>Attività</th>
                        <th>Ora inizio</th>
                        <th>Ora termine</th>
                    </tr>
                    <?php
                        $conn = mysqli_connect("localhost", "phpmyadmin", "BernardiniLab", "labud19");
                        if ($conn->connect_error) 
                        {
                            die("Connection failed: " . $conn->connect_error);
                        }
                        $sql = "SELECT activity, cast(start as TIME)start, cast(end as TIME)end FROM today_time";
                        $result = $conn->query($sql);
                        if ($result->num_rows > 0) 
                        {
                            while($row = $result->fetch_assoc()) 
                            {
                                echo "<tr><td>" 
                                . $row["activity"]. "</td><td>" 
                                . $row["start"] . "</td><td>"
                                . $row["end"]. "</td></tr>";
                            }
                            echo "</table>";
                        }
                        $conn->close();
                    ?>
                </table>
            </div>
        </div>

        <div class="footer">
            Created by Pierluigi Fabbro and Riccardo Deana - 2020
        </div>
    </body>

</html>
