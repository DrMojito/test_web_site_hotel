import sqlite3
import time
import math


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Invalid read DB")
        return []

    def addReviews(self, name, email, message):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO reviews VALUES(NULL, ?, ?, ?, ?)", (name, email, message, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Invalid add reviews' + str(e))
            return False

        return True
    
    def getReviews(self, reviewsId):
        try:
            self.__cur.execute(f'SELECT name, message, time FROM reviews WHERE id = {reviewsId} LIMIT 1')
            res = self.__cur.fetchone()
            if res:
                return res['name'], res['message'], res['time']
        except sqlite3.Error as e:
            print("Invalid take reviews" + str(e))
            
        return(False, False)
    
    
    def getReviewsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, name, message, time FROM reviews ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Invalid take reviews DB" + str(e))
        
        return[]