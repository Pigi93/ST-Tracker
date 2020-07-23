import MySQLdb
from datetime import datetime
from datetime import timedelta

def insert_today_activity(state, start, end):
    #Database connection
    db = MySQLdb.connect('localhost', 'phpmyadmin', 'BernardiniLab', 'labud19')
    cursor = db.cursor()
    #Add activity in the today_time  table
    sql = "INSERT INTO today_time SET activity ='%d', start ='%d-%d-%d %d:%d:%d', end='%d-%d-%d %d:%d:%d'" \
        %(state, start.year, start.month, start.day, start.hour, start.minute, start.second, end.year, end.month, end.day, end.hour, end.minute, end.second)
    cursor.execute(sql)
    db.commit()
    print "Data added to the database."
    #End of connection
    db.close()
    
def check_last_date():
    #Database connection
    db = MySQLdb.connect('localhost', 'phpmyadmin', 'BernardiniLab', 'labud19')
    cursor = db.cursor()
    #Add activity in the today_time  table
    sql = "SELECT start FROM today_time ORDER BY start DESC LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.commit()
    #End of connection
    db.close()
    if len(results) > 0:
        return results[0][0]
    else:
        return datetime.now()
        
def timedelta_to_hms(t):
    s = t.seconds % 60
    m = t.seconds // 60
    h = m // 60
    m = m % 60
    return (h,m,s)
    

def updates_daily_activities():
    #Database connection
    db = MySQLdb.connect('localhost', 'phpmyadmin', 'BernardiniLab', 'labud19')
    cursor = db.cursor()
    
    #Read today_time Database
    time=[]
    for n in range (1, 9):
        sql = "SELECT * FROM today_time WHERE activity ='%d'" %n
        cursor.execute(sql)
        results = cursor.fetchall()
        diff=timedelta(microseconds = 0)
        for row in results:
            start = row[1]
            end = row[2]
            diff += end - start
        time.append(timedelta_to_hms(diff))
        print "Activity=%s, Time=%s" %(n, time[n-1])
    sql = "SELECT start FROM today_time ORDER BY start DESC LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    #Update daily_activities Database
    i = results[0][0]
    sql = "INSERT INTO daily_activities SET data ='%d-%d-%d', \
            act1 ='%d:%d:%d', act2 ='%d:%d:%d', act3 ='%d:%d:%d', act4 ='%d:%d:%d', act5 ='%d:%d:%d', act6 ='%d:%d:%d', act7 ='%d:%d:%d', act8 ='%d:%d:%d' " \
            %(i.year,i.month,i.day, \
            time[0][0], time[0][1], time[0][2], \
            time[1][0], time[1][1], time[1][2], \
            time[2][0], time[2][1], time[2][2], \
            time[3][0], time[3][1], time[3][2], \
            time[4][0], time[4][1], time[4][2], \
            time[5][0], time[5][1], time[5][2], \
            time[6][0], time[6][1], time[6][2], \
            time[7][0], time[7][1], time[7][2])
    cursor.execute(sql)
    db.commit()
    print ("Update done.")
    #Reset the today_time table
    sql = "DELETE FROM today_time"
    cursor.execute(sql)
    db.commit()
    print ("Reset done.")
    #End of connection
    db.close()

def update_battery_status(voltage, percentage):
    #Database connection
    db = MySQLdb.connect('localhost', 'phpmyadmin', 'BernardiniLab', 'labud19')
    cursor = db.cursor()
	#Reset battery_status table
    sql = "DELETE FROM battery_status"
    cursor.execute(sql)
    db.commit()
    #Insert battery status in the battery_status table
    sql = "INSERT INTO battery_status SET voltage ='%.2f', percentage ='%i'" \
        %(voltage, percentage)
    cursor.execute(sql)
    db.commit()
    print "Battery status updated to the database."
    #End of connection
    db.close()