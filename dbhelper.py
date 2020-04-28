import sqlite3


class DBHelper:

    def __init__(self, dbname="julio_bot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (trigger, response text)"
        trig_idx = "CREATE INDEX IF NOT EXISTS triggerIndex ON items (trigger ASC)" 
        resp_idx = "CREATE INDEX IF NOT EXISTS responseIndex ON items (response ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(trig_idx)
        self.conn.execute(resp_idx)
        self.conn.commit()

    def add_item(self, trigger, response):
        stmt = "INSERT INTO items (trigger, response) VALUES (?, ?)"
        args = (trigger, response)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, trigger, response):
        stmt = "DELETE FROM items WHERE trigger = (?) AND response = (?)"
        args = (trigger, response)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, trigger):
        stmt = "SELECT trigger FROM items"
        # args = (trigger)
        return [x[0] for x in self.conn.execute(stmt)]

    def get_response(self, trigger):
        stmt = "SELECT * FROM items WHERE trigger = (?)"
        args = (trigger, )
        return [x for x in self.conn.execute(stmt, args)]
            




