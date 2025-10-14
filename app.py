from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS

import operations_base as opb
import jeux

app = Flask(__name__)
app.secret_key = 'light_ninja'  # clé secrete pour management de la session


# Initialize CORS for the app
CORS(app)



# base de données
description_jeux = {'Simon': "Ce jeu teste ta mémoire. Une suite de lumière va s'allumer devant toi. Il faut répéter la suite de couleurs avec les boutons devant toi dans le même ordre. Attention, à chaque tour la suite augmente d'une couleur.",
                    'Simon_2': "Ce jeu teste ta mémoire. Une suite de lumières va s'allumer devant toi. Il faut répéter la suite de couleurs avec les boutons devant toi dans le même ordre. Attention, à chaque tour la suite de couleur change totalement.",
                    'Reflex': "Ce jeu teste tes réflexes. Dès que la lumière s'allume, appuiez sur le bouton rouge le plus vite possible.",
                    'Reflex_Couleur': "Ce jeu teste tes réflexes sur 15 secondes. Dès qu'une lumière s'allume, appuiez sur le bouton de la couleur correspondante le plus vite possible.",
                    'Reflex_Multijoueur': "Ce jeu teste les réflexes de toi et tes amis. Prenez tous un bouton. Dès que la lumière s'allume, appuyez. Le plus rapide gagnera, et son temps s'affichera.",
                    'Mastermind': "Ce jeu teste ta réflexion. Il faut deviner une suite de quatre couleurs. Les 4 boutons devant toi représentent chacun une couleur. Utilise les boutons pour essayer de deviner la suite. Si une lumière devient blanche, alors la couleur devinée à cet emplacement est correcte. Si une lumière devient rouge, alors la couleur est dans la suite, mais pas au bon emplacement."}


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to the login page

    # Show user's name if logged in
    username = session.get('username')
    ranking = {Jeu.replace('_', ' '):opb.get_ranking(Jeu, username) for Jeu in ['Simon','Simon_2','Reflex','Reflex_Couleur','Reflex_Multijoueur','Mastermind']}
    profile_pic = session.get('profile_pic', 'no-profile.jpg')

    return render_template('home.html', username=username, ranking=ranking, profile_pic=profile_pic)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = opb.get_user(username)

        if existing_user:
            flash("Il y a déjà un utilisateur sous ce nom!")  # User exists
        else:
            # Insert the new user into the database
            opb.create_account(username, password)
            session['username'] = username  # Log in the user immediately after registration

            return redirect(url_for('profile_picture_selection'))  
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = opb.check_login(username, password)

        if not user:
            flash("Il n'y a pas d'utilisateur sous ce nom!")  # If the username doesn't exist
        elif user['mdp'] != password:  # Use dictionary-style access
            flash("Mot de passe incorrect!")  # If the password is incorrect
        else:
            # Store the username in the session
            session['username'] = username

            pfp_row = opb.get_pfp(username)
            session['profile_pic'] = pfp_row['pfp'] if pfp_row else None  # Safely set profile pic

            return redirect(url_for('home'))  # Redirect to the home page

    return render_template('login.html')

### PHOTO DE PROFIL ###
@app.route('/profile_picture_selection', methods=['GET', 'POST'])
def profile_picture_selection():

    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to the login page

    if request.method == 'POST':
    
        username = session.get('username')
        selected_image = request.form.get('selected-img')  # Get the value from the hidden input
                    
        if not selected_image:
            if 'profile_pic' not in session:
                selected_image = 'no-profile.jpg'
            else:
                selected_image = session['profile_pic']
            
        opb.update_pfp(username, selected_image)

        session['profile_pic'] = selected_image

        return redirect(url_for('home'))  # Redirect to home page after saving the profile picture    

    return render_template('profile_picture_selection.html')  # Show the page if GET request


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user isn't logged in
        
    # Render the settings page
    return render_template('settings.html', username=session.get('username'), profile_pic=session.get('profile_pic'))


# Change username route
@app.route('/change_username', methods=['POST'])
def change_username():
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure the user is logged in
    
    new_username = request.json.get('username')  # Get new username from the request
    current_username = session.get('username')
    
    if not new_username:
        return jsonify({'success': False, 'message': 'Username cannot be empty'})

    existing_user = opb.get_user(new_username)

    if existing_user:
        return jsonify({'success': False, 'message': 'This username is already taken'})
    
    # Update the username in the database
    opb.update_username(new_username, username)

    # Update the session with the new username
    session['username'] = new_username
    
    return jsonify({'success': True})


# Change password route
@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure the user is logged in
    
    new_password = request.json.get('password')  # Get new password from the request
    
    if not new_password:
        return jsonify({'success': False, 'message': 'Password cannot be empty'})

    opb.update_password(new_password, session['username'])
    
    return jsonify({'success': True})


@app.route('/logout')
def logout():
    session.pop('username', None)  # Enlever l'utilisateur de la session
    session.pop('profile_pic', None)
    return redirect(url_for('login'))



# # # PAGES DE JEU # # #

Game_Chart_Info = {'Simon': {'DataType': 'Palier', 'YAxisText': 'Palier atteint', 'AvgTitle': 'Palier atteint en moyenne', 'GameBins':1}, 
                   'Simon_2': {'DataType': 'Palier', 'YAxisText': 'Palier atteint', 'AvgTitle': 'Palier atteint en moyenne', 'GameBins':1},
                    'Reflex': {'DataType': 'Temps', 'YAxisText': 'Temps de réaction (ms)', 'AvgTitle': 'Temps de réaction moyen', 'GameBins':40},
                    'Reflex_Couleur': {'DataType': 'Temps', 'YAxisText': 'Temps de réaction (ms)', 'AvgTitle': 'Temps de réaction moyen', 'GameBins':40},
                    'Reflex_Multijoueur': {'DataType': 'Victoire', 'YAxisText': 'Défaite (0) Victoire (1)', 'AvgTitle': 'Temps de réaction gagnant moyen', 'GameBins':40},
                    'Mastermind': {'DataType': 'Niveau', 'YAxisText': "Nombre d'essais", 'AvgTitle': "Nombre d'essais moyens par partie", 'GameBins':1}}

value_type = {
    'Simon':'',
    'Simon_2':'',
    'Reflex':' ms',
    'Reflex_Couleur':' ms',
    'Reflex_Multijoueur':' ms',
    'Mastermind':''
}

# Page gamepage.html, personnalisé pour chaque jeu
@app.route('/<game_name>')
def gamepage(game_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if game_name not in description_jeux:
        return redirect(url_for('home')) 

    username = session.get('username')
    profile_pic = session.get('profile_pic', 'no-profile.jpg')
    
    description = description_jeux.get(game_name, "Description not available.")

    valeur_recente = str(opb.valeur_recente(game_name, username))+value_type[game_name]

    # Statistiques d'utilisateur

    nb_partie, moy, pos = opb.get_game_stats(game_name, username)
    
    if nb_partie != '?':
        moy = str(round(moy))+value_type[game_name]
        pos = 'Top '+str(round((pos*100),2))+'%'

    game_stats = {'Nombre de parties: ': nb_partie,
            'Ta moyenne: ': moy,
            'Positionnement: ': pos
            }

    
    ranking = {Jeu.replace('_', ' '):opb.get_ranking(Jeu, username) for Jeu in ['Simon','Simon_2','Reflex','Reflex_Couleur','Reflex_Multijoueur','Mastermind']}

    # Infos des graphes

    infos = Game_Chart_Info[game_name]
    DataType = infos['DataType']
    YAxisText = infos['YAxisText']
    AvgTitle = infos['AvgTitle']
    GameBins = infos['GameBins']
    return render_template('gamepage.html', username=username, profile_pic=profile_pic, game_name=game_name.replace('_', ' '), description=description, ranking=ranking, game_stats=game_stats, DataType=DataType, YAxisText=YAxisText, AvgTitle=AvgTitle, GameBins=GameBins, valeur_recente=valeur_recente)


# Lance le jeu et continue d'afficher gamepage.html avec les valeurs updatées
@app.route('/jouer/<game_name>/<username>')
def jouer(game_name, username):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user isn't logged in
        
    jeux.correspondances_jeux[game_name](jeux.cbase, username)

    return redirect(url_for('gamepage', game_name=game_name.replace(' ', '_')))


### Données envoyées sur gamepage javascript pour faire les graphiques Highcharts ###

# Data Progres
@app.route('/data_progres/<game_name>/<username>', methods=['GET'])
def get_progres(game_name, username):
    
    rows = opb.get_data_progres(game_name.replace(' ', '_'), username)

    progress_data = [{'x': row[0], 'y': row[1]} for row in rows]

    return jsonify(progress_data)

@app.route('/data_moyenne/<game_name>', methods=['GET'])
def get_moyenne(game_name):
    # Fetch raw data
    game_name = game_name.replace(' ', '_')
    
    rows = opb.get_data_moyenne(game_name)
    avg_times = [round(row[0]) for row in rows if row[0] is not None]

    if not avg_times:
        return jsonify([])  # Return empty list if no data is found

    bin_size = Game_Chart_Info[game_name]['GameBins']

    # Define bin width (you may adjust or dynamically set this based on the game)
    bin_counts = {}
    for value in avg_times:
        bin_start = (value // bin_size) * bin_size
        if bin_start in bin_counts:
            bin_counts[bin_start] += 1
        else:
            bin_counts[bin_start] = 1
    
    bins = [{'x':bin_start, 'count':count} for bin_start, count in sorted(bin_counts.items())]
    
    # If you want to return to previous range bins: Photo 16/12
    
    return jsonify(bins)



# Lancer le serveur

if __name__ == '__main__':
    print("\n=========================================")
    print("Le serveur Flask démarre!")
    print("Accèdez au site sur http://127.0.0.1:5000")
    print("=========================================\n")
    
    app.run(debug=True)
