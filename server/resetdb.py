import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("DELETE FROM Coordinate WHERE 1=1")
conn.commit()
conn.close()
