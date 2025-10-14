import sqlite3
from datetime import datetime

specific_data = {'Simon':'palier_atteint', 'Simon_2':'palier_atteint', 'Reflex':'temps_reaction', 'Reflex_Couleur':'temps_reaction', 'Reflex_Multijoueur':'temps_reaction', 'Mastermind':'tours'}

ordre_pourcentile = {'Simon':'DESC', 'Simon_2':'DESC', 'Reflex':'ASC', 'Reflex_Couleur':'ASC', 'Reflex_Multijoueur':'ASC', 'Mastermind':'ASC'}

# Fonction qui ouvre la base de données et renvoie la connexion
def get_db():
    conn = sqlite3.connect('data/donnees.db')
    conn.row_factory = sqlite3.Row  # Permet d'acceder a des colones par nom (ex: user['username'])
    return conn


def get_user(username):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT username FROM User WHERE username = ?", (username,))
    existing_user = c.fetchone()
    
    conn.close()
    
    return existing_user


def get_pfp(username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT pfp FROM User WHERE username = ?", (username,))
    pfp_row = c.fetchone()

    conn.close()
    
    return pfp_row


def create_account(username, password):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("INSERT INTO User (username, mdp, pfp, date_création) VALUES (?, ?, ?, ?)",
                           (username, password, 'no-profile.jpg', datetime.now()))
    
    conn.commit()
    conn.close()
    

def update_username(new_username, username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("UPDATE User SET username = ? WHERE username = ?", (new_username, current_username))
    
    conn.commit()
    conn.close()


def update_password(new_password, username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("UPDATE User SET mdp = ? WHERE username = ?", (new_password, username))
    
    conn.commit()
    conn.close()

    
def check_login(username, password):
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT username, mdp FROM User WHERE username = ?", (username,))
    
    user = c.fetchone()
    conn.commit()
    conn.close()
    
    return user


def update_pfp(username, selected_image):
    conn = get_db()
    c = conn.cursor()

    c.execute("UPDATE User SET pfp = ? WHERE username = ?", (selected_image, username))

    conn.commit()
    conn.close()


def incrementation_essais(Jeu, username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute(f"SELECT MAX(num_essai) FROM {Jeu} WHERE username = ?;", (username,))
    res = c.fetchone()
    
    conn.close()
    
    return 1 if res[0] == None else res[0] + 1


def insere(Jeu, donnees):
    conn = get_db()
    c = conn.cursor()
        
    if Jeu in ('Simon','Simon_2','Reflex','Reflex_Couleur','Mastermind'):
        c.execute(f"INSERT INTO {Jeu} VALUES (?,?,?);", donnees )
    else:
        c.execute("INSERT INTO Reflex_Multijoueur VALUES (?,?,?,?);", donnees )
    
    conn.commit()
    conn.close()
    

def get_data_progres(game_name, username):
    conn = get_db()
    c = conn.cursor()

    c.execute(f"""
        SELECT num_essai, {specific_data[game_name]} 
        FROM {game_name} 
        WHERE username = ? 
        ORDER BY num_essai ASC 
        LIMIT 15 OFFSET (SELECT COUNT(*) FROM {game_name} WHERE username = ?) - 15;
    """, (username, username))

    
    rows = c.fetchall()
    conn.close()

    return rows


def get_data_moyenne(game_name):
    conn = get_db()
    c = conn.cursor()

    c.execute(f"SELECT AVG({specific_data[game_name]}) FROM {game_name} GROUP BY username;")
    
    rows = c.fetchall()
    conn.close()

    return rows

def get_game_stats(game_name, username):
    conn = get_db()
    c = conn.cursor()

    c.execute(f"""WITH AllStats AS (
        SELECT
            username,
            AVG({specific_data[game_name]}) AS moyenne,
            MAX(num_essai) AS nb_parties
        FROM {game_name}
        GROUP BY username
    ),
    Percentiles AS (
        SELECT
            username,
            moyenne,
            nb_parties,
            PERCENT_RANK() OVER (ORDER BY moyenne {ordre_pourcentile[game_name]}) AS percentile
        FROM AllStats
    )
    SELECT
        nb_parties,
        moyenne,
        percentile
    FROM Percentiles
    WHERE username = ?;""", (username,))
    
    rows = c.fetchone()
    conn.close()

    return ('?','?','?') if rows is None else rows


def get_ranking(game_name, username):
    conn = get_db()
    c = conn.cursor()

    c.execute(f"""WITH Rankings AS (
        SELECT
            username,
            AVG({specific_data[game_name]}) AS avg_time,
            RANK() OVER (ORDER BY AVG({specific_data[game_name]}) {ordre_pourcentile[game_name]}) AS rank
        FROM {game_name}
        GROUP BY username
    )
    SELECT
        rank
    FROM Rankings
    WHERE username = ?;
""", (username,))

    rows = c.fetchone()
    conn.close()

    return '?' if rows == None else rows[0]
    

def valeur_recente(game_name, username):
    conn = get_db()
    c = conn.cursor()

    c.execute(f"SELECT {specific_data[game_name]} FROM {game_name} WHERE username=? ORDER BY num_essai DESC LIMIT 1;",(username,))

    rows = c.fetchone()
    conn.close()

    return '. . .' if rows == None else rows[0]

