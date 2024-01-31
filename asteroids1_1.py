import sqlite3

con = sqlite3.connect('records')
cur = con.cursor()


cur.execute('INSERT INTO results VALUES("a", 432)')
con.commit()

