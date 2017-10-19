import sqlite3

# connect to sqlite database, read in european soccer data

# tables
# Country, Match, Player_Attributes,
# Team_Attributes, League, Player, Team

conn = sqlite3.connect('data/database.sqlite')
c = conn.cursor()
for row in c.execute('SELECT * FROM Player'):
    print row

