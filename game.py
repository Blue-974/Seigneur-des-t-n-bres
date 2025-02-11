import json
import random

class Player:
    def __init__(self, user_id:int, user_data, hand:list = [], blame:int = 0, sdt:bool = False):
        self.id = user_id
        self.data = user_data
        self.hand = hand # Main du joueur
        self.blame = blame # Regards noirs
        self.sdt = sdt # Seigneur des ténèbres

with open('cartes.json', 'r') as f:
    allcards = json.load(f)  # Reference de toutes les cartes

listcard = allcards #listcard peut être détruit à souhait
players = [] #Liste des joueurs

game_state = False

player_options = []

def reset():
    global players
    global game_state
    global listcard

    players = []
    game_state = False
    listcard = allcards

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

# Fonction pour piocher des cartes
def draw_cards(player:Player):
    if len(listcard) < 3:
        return
    else:
        # Vide la main
        player.hand.clear()
        # Pioche 3 cartes
        player.hand.extend(random.sample(listcard, 3))
        return


# Fonction pour utiliser des cartes
def use_cards(player:Player):
    while True:
        card_to_use = input("Quelle carte veux-tu utiliser? (ou tape 'exit' pour quitter): ")
        if card_to_use == 'exit':
            break
        if card_to_use in player.hand:
            # Retire la carte de la main
            player.hand.remove(card_to_use)
            # Pioche une nouvelle carte
            player.hand.extend(random.sample(listcard, 1))
        else:
            return

# règles du jeu
rules_text = (
        "### Règles du jeu:\n"
        "On distribue à chaque joueur 3 cartes.\n"
        "Un joueur est désigné comme seigneur des ténèbres.\n"
        "Grâce aux 3 cartes de sa main, il raconte aux autres joueurs la mission qu'il leur a confiée.\n"
        "Il donne la parole à un joueur qui se défend grâce à au moins une de ses cartes.\n"
        "Le seigneur des ténèbres donne ensuite la parole à un joueur accusé pour qu'il se défende, et ainsi de suite.\n"
        "Si les explications d’un joueur contredisent d’autres informations ou ne satisfont pas le seigneur des ténèbres, il reçoit un regard noir.\n"
        "Le premier joueur à recevoir 3 regards noirs est désigné coupable et la partie est terminée."
    )