import sqlite3

# Connection
# todo: get path via variable
# connect to sqlite database; if file doesn't exist, this command creates it
_conn = sqlite3.connect('sensors.db')
_c = _conn.cursor()

# Initialize DB with tables if they don't exist.
_c.execute('CREATE TABLE IF NOT EXISTS DHT22 (time TIMESTAMP, device TEXT, humidity FLOAT, temperature FLOAT)')
_conn.commit()

## Queries
def logDHT22(time, device, humidity, temperature):
    _c.execute('INSERT INTO DHT22 VALUES (?,?,?,?)', (time, device, humidity, temperature))
    _conn.commit()
    return True

def logFailure(time, device, cause):
    _c.execute('INSERT INTO failures VALUES (?,?,?)', (time, device, cause))
    _conn.commit()
    return True


# TODO: auto compacting
# TODO: exceptions of queries? Return True or return None?
# TODO: fix UTC consistency; always record UTC times (or epoch) and ignore system times for everything
