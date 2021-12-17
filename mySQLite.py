import sqlite3

#con = sqlite3.connect('example.db')

class database( object ):
    def __init__(self, nameDB, tableName = 'weather'):
        self.nameDB = nameDB
        self.con = sqlite3.connect(nameDB)
        self.cursor = self.con.cursor()
        self.tableName = tableName
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + self.tableName + "';")
        if not self.cursor.fetchall(): 
            self.cursor.execute( "CREATE table " + self.tableName + " (date text, POGODA text, temp real, odczuwalna real, cisnienie real, predkoscWiatru real, wilgotnosc real)" )
    
    def pushWeather( self, weather ):
        self.cursor.execute( "INSERT INTO " + self.tableName + " values ('{}','{}',{},{},{},{},{});".format( weather[0], weather[1], weather[2], weather[3], weather[4], weather[5], weather[6] ) )
        self.con.commit()

    def getMinimum( self ):
        self.cursor.execute( "select min(temp) from " + self.tableName  )
        res = self.cursor.fetchall()
        return res
    def getMaximum( self ): 
        self.cursor.execute( "select max(temp) from " + self.tableName  )
        res = self.cursor.fetchall()
        return res
    def getAvg( self ):
        self.cursor.execute( "select avg(temp) from " + self.tableName  )
        res = self.cursor.fetchall()
        return res