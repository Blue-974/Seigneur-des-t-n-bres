from discord import *
import random

class Card:
    def __init__(self, card_type:bool = False, text:str = ""):
        self.type = card_type # True si carte d'excuse, False si carte d'action
        self.description = text

class Player:
    def __init__(self, user_id:int, user_data, hand:list[Card] = [], blame:int = 0, sdt:bool = False):
        self.id = user_id
        self.data = user_data
        self.hand = hand # Main du joueur
        self.blame = blame # Regards noirs
        self.sdt = sdt # Seigneur des ténèbres

listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"] # Placeholder

players = [] #Liste des joueurs

# je spam le mot clef global sur cette variable parce que j'ai la flemme de chercher où est ce que le code croit qu'elle est locale (mais c'est temporaire tkt)
global game_state
game_state = 0 # Etat de la partie, différent de 0 partie en cours, 0 pas de partie en cours

player_options = [] # Placeholder

def reset():
    global players
    players = []
    global game_state
    game_state = 0
    global listcard
    listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"] # Placeholder

def add_player(id:int,data):
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
    if game_state != 0:
        return False
    if len(players)<1:
        return False
    game_state = 1
    optionsgenerator()

# Generateur d'option pour la selection du seigneur des tenebres
def optionsgenerator():
    for p in players:
        player_options.append(SelectOption(label=p.data.name,value=str(p.id)))
    player_options.append(SelectOption(label="Aléatoire",value="1"))
    return player_options

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