
############################################################################################
# Importation des bibliothèques.
from led_setup import * 

import operations_base as opb

import RPi.GPIO as GPIO
import time
import random

# Définition des ports où se trouvent les boutons.
GPIO.setmode(GPIO.BCM)
button_pins = [16, 18, 22, 24]
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)


def bouton_appuye(pin):
    # Fonction qui détecte si un bouton est appuyé.
    return GPIO.input(pin) == GPIO.HIGH

# Différents couples de couleurs possibles
cbase : list = [Rouge, Bleu, Vert, Or]



def Simon(couleur : list, username : str):
    """Créer une liste de plus en plus longue dont le joueur doit se
    souvenir et qu'il doit répéter. La liste reprend la précédente et
    ajoute un élément à chaque tour. À la fin le programme met dans
    la table le niveau jusqu'auquel le joueur est arrivé à aller.
    """
    tout_eteindre()
    
    partie : bool = True
    liste : list = []
    temps_affichage : float = 1.0
    temps_repos : float = 0.5
    
    while partie: # Boucle de jeu.
        if temps_affichage > 0.4:
            temps_affichage -= 0.1
        if temps_repos > 0.2:
            temps_repos -= 0.05
        nombre = random.randint(0,3)
        liste.append((couleur[nombre], nombre)) # Ajout d'un nouvel élement.
        
        for element in liste: # Affichage de la liste.
            allumer(element[1], element[0])
            time.sleep(temps_affichage)
            eteindre(element[1])
            time.sleep(temps_repos)
            
        for element2 in liste: # Vérifie que les boutons appuyés correspondent au couleurs de la liste.
            bouton = [18, 16, 24, 22]
            attendre = True
            bouton_cible = bouton[element2[1]]
            
            while attendre == True:
                tout_eteindre()
                for bou in bouton:
                    if bouton_appuye(bou):
                        if bou == bouton_cible:
                            allumer(element2[1], element2[0])
                            time.sleep(0.5)
                            eteindre(element2[1])
                            time.sleep(0.5)
                            attendre = False
                        else:
                            partie = False
                            attendre = False
                        break
    
    tout_eteindre()
                                                
    opb.insere('Simon', (username, len(liste) - 1, opb.incrementation_essais('Simon', username)) )

def Simon_2(couleur : list, username : str):
    """Créer une liste de plus en plus longue dont le joueur doit se
    souvenir et qu'il doit répéter. La liste est différente à chaque
    tours. À la fin le programme met dans la table le niveau
    jusqu'auquel le joueur est arrivé à aller.
    """
    tout_eteindre()
    partie : bool = True
    compt : int = 0
    while partie == True: # Boucle de jeu.
        compt += 1
        liste : list = []
        for i in range(compt): # Génération d'une nouvelle liste
            nombre : int = random.randint(0,3)
            liste.append((couleur[nombre], nombre))
        for element in liste: # Affichage de la liste.
            allumer(element[1], element[0])
            time.sleep(1)
            eteindre(element[1])
            time.sleep(0.5)
        for element2 in liste: # Vérifie que les boutons appuyer
                               # correspondes au couleurs de la liste.
    
            bouton = [18, 16, 24, 22]
            attendre = True
            bouton_cible = bouton[element2[1]]
            
            while attendre == True:
                tout_eteindre()
                for bou in bouton:
                    if bouton_appuye(bou):
                        if bou == bouton_cible:
                            allumer(element2[1], element2[0])
                            time.sleep(0.5)
                            eteindre(element2[1])
                            time.sleep(0.5)
                            attendre = False
                        else:
                            partie = False
                            attendre = False
                        break
    
    tout_eteindre()
    
    opb.insere('Simon_2', (username, len(liste) - 1, opb.incrementation_essais('Simon_2', username)) )

def Reflex(couleur : list, username : str):
    """Le jeu allume de façon aléatoire dans le temps une lumière.
    Le joueur doit appuyer sur le bouton le plus rapidement possible.
    Le temps de réaction du joueur sera mis dans un tableau
    avec son username.
    """
    tout_eteindre()
    a : int = random.randint(1,6)
    jeu : bool = True
    reaction_time : float = 0.0
    time.sleep(a) # Temps d'attente.
    start : float = time.time()
    allumer(0, couleur[0])
    while jeu == True: # Boucle de jeu.
        if bouton_appuye(18): # Tant que le bouton n'est pas appuyer,
                              # la boucle continu.
            jeu = False
            reaction_time = time.time() - start
            reaction_time = round(round(reaction_time, 3)*1000)
    eteindre(0)
    
    tout_eteindre()
    
    opb.insere('Reflex', (username, reaction_time, opb.incrementation_essais('Reflex', username)) )

def Reflex_Couleur(couleur : list, username : str, temps : int = 15):
    """Pendant un temps donné en paramètre,
    une lumière s'allume jusqu'à ce que le joueur appuie sur
    le bouton correspondant à la couleur. Une fois le temps écoulé,
    le programme met dans la table Reflex l'id du joueur et
    le temps moyen qu'il a fait pendant ce jeu.
    """
    tout_eteindre()
    start = time.time()
    compte : int = 0
    eteint : bool = True
    capteur : list = [18, 16, 24, 22]
    while time.time() - start < temps: # boucle de jeu.
        nombre : int = random.randint(0, 3) #choix couleur.
        if eteint == True:
            allumer(nombre, couleur[nombre])
            eteint = False
        bouton : bool = False
        while bouton == False: #attend boutons correspondants soit appuyer.
            if bouton_appuye(capteur[nombre]):
                bouton = True
                compte += 1
        eteindre(nombre)
        eteint = True
    tout_eteindre()
    compte = round(round(temps/compte,3)*1000)
    
    opb.insere('Reflex_Couleur', (username, compte, opb.incrementation_essais('Reflex_Couleur', username)) )

def Reflex_Multijoueur(couleur : list, username : str):
    """Le programme allume une lumière et détecte le premier bouton
    à être appuyé et en combien de temps il a été pressé.
    """
    tout_eteindre()
    temps : int = random.randint(1, 6)
    jeu : bool = True
    capteur : list=[18, 16, 24, 22]
    gagnant : int = -1
    reaction_time : float = 0.0
    time.sleep(temps)
    start : float = time.time()
    allumer(0, couleur[0])
    while jeu == True: # boucle de jeu
        for element in range(len(capteur)):
            if bouton_appuye(capteur[element]):
                jeu = False
                reaction_time = time.time() - start
                gagnant = element
    eteindre(0)
    reaction_time = round(round(reaction_time, 3)*1000)
    tout_eteindre()
    if gagnant != -1:
        allumer(gagnant, couleur[gagnant])
        time.sleep(1.5)
        tout_eteindre()
    opb.insere('Reflex_Multijoueur', (username, gagnant, reaction_time, opb.incrementation_essais('Reflex_Multijoueur', username)) )

def demarage(couleur : list):
    t : int = 1
    c : int = 0
    while t > 0:
        c += 1
        if c > 3:
            c = 0
        t -= 0.2
        for i in range(4):
            b = c + i
            if b > 3:
                b -= 4
            allumer(i, couleur[b])
        time.sleep(0.2)
        tout_eteindre()

def Mastermind(couleur : list, username : str):
    """Le programme génère un code et le joueur doit le deviner
    en 8 coups. Pour rentrer ses conjectures, il utilise les boutons,
    et les lumières correspondantes sont allumées.
    Si une couleur est au bon endroit, une lumière blanche s'allume,
    si une lumière est bien dans la réponse,
    mais pas à la bonne place, une lumière rouge s'allume.
    Si le joueur gagne ou perd, c'est rentré dans la table
    mastermind avec son id.
    """
    tout_eteindre()
    capteur : list = [18, 16, 24, 22]
    partie : bool = True
    code : list = []
    points : int = 0
    for i in range(4): # Création code.
        code.append(random.randint(0, 3))
    while partie: # Boucle jeu
        points += 1
        reponse : list = []
        allumée : list = [0, 0, 0, 0]
        copie_code : list = code[:]
        while len(reponse) < 4: # Entrée code par joueur
            for i in range(4):
                if bouton_appuye(capteur[i]):
                    reponse.append(i)
                    allumer(len(reponse) - 1, couleur[i])
                    time.sleep(0.5)
        tout_eteindre()
        
        if code == reponse: # Vérifie si le code est le bon
            partie = False
            break
        for i in range(4): # Vérifie si des couleurs sont a la bonne place
            if copie_code[i] == reponse[i]:
                allumer(i, Blanc)
                copie_code[i] = -1
                reponse[i] = -2
                allumée[i] = 1
        for i in range(4): # Vérifie si il y a des bonne couleurs à la mauvaise place.
            if reponse[i] != -2:
                for j in range(4):
                    if copie_code[j] == reponse[i]:
                        copie_code[j] = -1
                        allumer(i, Rouge)
                        allumée[i] = 1
                        break
        for i in range(4):
            if allumée[i] == 0:
                eteindre(i)
        time.sleep(2)
        tout_eteindre()
    
    demarage(cbase)
    opb.insere('Mastermind', (username, points, opb.incrementation_essais('Mastermind', username)) )
    
    tout_eteindre()


correspondances_jeux = {'Simon': Simon, 'Simon 2': Simon_2, 'Reflex': Reflex, 'Reflex Couleur': Reflex_Couleur, 'Reflex Multijoueur': Reflex_Multijoueur, 'Mastermind': Mastermind}
