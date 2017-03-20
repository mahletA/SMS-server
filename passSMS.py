#!/usr/bin/python
import threading
import subprocess
import MySQLdb

from os import system
# Open database connection
class ParsingThread(threading.Thread):

   def run(self):
      threading.Timer(0.25, self.run).start ()
      db = MySQLdb.connect("localhost","root","mah","Fetal-Activity-Monitor" )

      # prepare a cursor object using cursor() method
      cursor = db.cursor()

      # to save data fetched from the sql query 
      queried_data=[] 



      sql = """
            SELECT TextDecoded , ReceivingDateTime , SenderNumber
            FROM inbox ,Activity_Monitor_gsmdevice 
            WHERE inbox.Parsed=0 AND inbox.SenderNumber=device_id AND status='A'; 

            """

      mark = """
            UPDATE inbox
            SET inbox.Parsed=1
            WHERE inbox.Parsed=0;

            """


      try:
         # Execute the SQL command
         cursor.execute(sql)
       
         # Fetch all the rows in a list of lists.
         results = cursor.fetchall()
         for row in results:
            queried_data.append([row[0],row[1],row[2]])
          
      except:
      	
         print "Error: unable to fecth data"






      for x in queried_data:
         a =x[0].split('_')


         try:
            cursor.execute("""INSERT INTO  `Fetal-Activity-Monitor`.`Activity_Monitor_smsdata` (`heart_rate` ,`kick_count` ,`date` ,`gsm_id`)
                              VALUES (%s, %s, %s,%s )""", (a[1], a[3], str(x[1]), x[2]))
            db.commit()

         except:
            db.rollback()
            print "Error: unable to parse data" 

   



      try:
         # Execute the SQL command
         cursor.execute(mark)
       
      except:
         
         print "Error: unable to mark parsed sms"


      #print queried_data
      #print str(queried_data[0][1]).split(' ')
      # disconnect from server
      db.close()


class GammuThread(threading.Thread):

   def run(self):
      system("gammu-smsd -c /etc/gammu-smsdrc")
