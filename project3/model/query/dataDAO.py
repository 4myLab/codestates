import os
import sqlite3

class dataDAO:
    DB_FILENAME = 'project3.db'
    DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    
    def __init__(self):        
        # DB_FILENAME = 'project3.db'
        # DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
        # conn = sqlite3.connect(DB_FILENAME)
        # cur = conn.cursor()
        pass

    def createTableGameCode(self):
        self.cur.execute("""CREATE TABLE if not exists game_code_info(
                            code VARCHAR(10) NOT NULL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL);""")
        self.conn.commit()
    
    def insertDataGameCode(self, id, name):
        self.cur.execute('REPLACE INTO game_code_info (code, name) VALUES (?,?);',
                        (id, name))
        self.conn.commit()
