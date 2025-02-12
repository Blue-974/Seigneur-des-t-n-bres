#"Oui, Seigneur des ténèbres" adapté en bot discord par Scottellow et Blue974

import json
import random

with open('cartes.json', 'r', encoding='utf-8') as f:
    allcards = json.load(f)  # Reference de toutes les cartes

listcard = allcards['cartes'] #listcard peut être détruit à souhait
players = [] #Liste des joueurs

game_state = False

player_options = []

class Player:
    def __init__(self, user_id:int, user_data = None, hand:list=None, blame:int = None, sdt:bool = None):
        self.id = user_id
        self.data = user_data
        self.hand = hand if hand is not None else ["", "", ""] # Main du joueur
        self.blame = blame if blame is not None else 0 # Regards noirs
        self.sdt = sdt if sdt is not None else False # Seigneur des ténèbres

    # Fonction pour piocher des cartes
    def draw_cards(self):
        for d,c in enumerate(self.hand):
            if c == "" and len(listcard) != 0:
                while True:
                    i = random.randint(0,len(listcard)-1)
                    if listcard[i] == "Interruption":
                        if not self.sdt:
                            if d == 2:
                                if not(self.hand[0] == "Interruption" or self.hand[1] == "Interruption"):
                                    break
                            else: break
                    else : break
                self.hand[d] = listcard.pop(i)
    
    # Fonction pour utiliser des cartes
    def use_cards(self,index):
        if self.hand[index] != "" and self.hand[index] != "Interruption":
            played_card = self.hand[index]
            self.hand[index] = ""
            return played_card
        return ""
    
    def suffer(self):
        self.blame += 1
        if self.blame >= 3:
            return True
        return False

def distribute_cards():
    for p in players:
        p.draw_cards()

def get_player(id:int):
    for p in players:
        if p.id == id:
            return p

def reset():
    global players
    global game_state
    global listcard

    players = []
    game_state = False
    listcard = allcards['cartes']

def add_player(id:int,data):
    global game_state

    if game_state:
        return False
    for p in players:
        if p.id == id :
            return False
    if len(players) > 24:
        return False
    new_player = Player(user_id=id,user_data=data)
    players.append(new_player)
    return True

def start():
    global game_state

    if game_state == True:
        return False
    elif len(players)<1:
        return False
    else:
        game_state = 1

def select_random_player():
    return random.choice(players)

# règles du jeu
rules_text = (
        "### Règles du jeu:\n"
        "On distribue à chaque joueur 3 cartes.\n"
        "Un joueur est désigné comme seigneur des ténèbres.\n"
        "Grâce aux 3 cartes de sa main, il raconte aux autres joueurs la mission qu'il leur a confiée.\n"
        "Il donne la parole à un joueur qui se défend grâce à au moins une de ses cartes.\n"
        "Le seigneur des ténèbres donne ensuite la parole à un joueur accusé pour qu'il se défende, et ainsi de suite.\n"
        "Si les explications d’un joueur contredisent d’autres informations ou ne satisfont pas le seigneur des ténèbres, il reçoit un regard noir.\n"
        "Vous pouvez parler sans que le seigneur des ténèbres ne vous donne la parole grâce à la carte interruption qui coupe la parole du joueur s’exprimant, vous pourrez ainsi vous défendre ou accuser quelqu’un.\n"
        "Le premier joueur à recevoir 3 regards noirs est désigné coupable et la partie est terminée."
    )