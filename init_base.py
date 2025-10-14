
import sqlite3
from datetime import datetime


conn = sqlite3.connect('data/donnees.db')
c = conn.cursor()

sqlite3.register_adapter(datetime, lambda d: d.strftime('%Y-%m-%d %H:%M:%S'))


# TABLE USER #
c.execute("""
        CREATE TABLE IF NOT EXISTS User(
            username TEXT PRIMARY KEY,
            mdp TEXT,
            pfp TEXT,
            date_création DATETIME
        );
    """)
    
c.executemany("INSERT OR IGNORE INTO User (username, mdp, pfp, date_création) VALUES (?, ?, ?, ?);", 
            [('alex', 'potato', 'pfp2.jpg', datetime.now()),
            ('hermance', 'neige78', 'pfp3.jpg', datetime.now()),
            ('camille', 'soleil34', 'pfp6.jpg', datetime.now())])


# TABLE SIMON #
c.execute("""
        CREATE TABLE IF NOT EXISTS Simon(
            username TEXT,
            palier_atteint INTEGER,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)

# TABLE SIMON 2 #
c.execute("""
        CREATE TABLE IF NOT EXISTS Simon_2(
            username TEXT,
            palier_atteint INTEGER,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)


# TABLE REFLEX #
c.execute("""
        CREATE TABLE IF NOT EXISTS Reflex(
            username TEXT,
            temps_reaction REAL,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)
    
# TABLE REFLEX COULEUR #
c.execute("""
        CREATE TABLE IF NOT EXISTS Reflex_Couleur(
            username TEXT,
            temps_reaction REAL,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)

# TABLE REFLEX MULTIJOUEUR #
c.execute("""
        CREATE TABLE IF NOT EXISTS Reflex_Multijoueur(
            username TEXT,
            gagnant INTEGER,
            temps_reaction REAL,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)
    
# TABLE MASTERMIND #
c.execute("""
        CREATE TABLE IF NOT EXISTS Mastermind(
            username TEXT,
            tours INTEGER,
            num_essai INTEGER,
            FOREIGN KEY(username) REFERENCES User(username)
        );
    """)



conn.commit()
conn.close()
