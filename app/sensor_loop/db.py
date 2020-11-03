import sqlite3

class Database:
    # Initialize a connection given a sqlite DB file
    def __init__(self, file):
        # connect to sqlite database; if file doesn't exist, this command creates it
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

        # Initialize DB with tables if they don't exist.
        self.cursor.execute('CREATE TABLE IF NOT EXISTS DHT22 (time TIMESTAMP, device TEXT, humidity FLOAT, temperature FLOAT)')
        self.connection.commit()

    def execute(self, *args):
        return self.cursor.execute(*args)

    def commit(self, *args):
        return self.connection.commit(*args)

# Queries

def logDHT22(db, time, device, humidity, temperature):
    db.execute('INSERT INTO DHT22 VALUES (?,?,?,?)', (time, device, humidity, temperature))
    db.commit()
    return True

def logFailure(db, time, device, cause):
    db.execute('INSERT INTO failures VALUES (?,?,?)', (time, device, cause))
    db.commit()
    return True


# TODO: auto compacting
# TODO: exceptions of queries? Return True or return None?
# TODO: fix UTC consistency; always record UTC times (or epoch) and ignore system times for everything
