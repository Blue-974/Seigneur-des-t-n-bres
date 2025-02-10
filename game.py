import random

class Card:
    def __init__(self, card_type:bool, text:str):
        self.type = card_type # True si carte d'excuse, False si carte d'action
        self.description = text

class Player:
    def __init__(self, user_id:int,hand:list[Card],blame:int):
        self.id = user_id
        self.hand = hand
        self.blame = blame

# Liste des cartes
listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"]

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
        "Comment jouer au jeu:\n"
        "1. Utilisez `!draw` pour piocher trois cartes.\n"
        "2. Utilisez `!use <nom_de_carte>` pour jouer une carte et en tirer une nouvelle.\n"
        "3. Les cartes sont envoyées en message privé pour garder votre main secrète.\n"
        "4. Amusez-vous et jouez stratégique !\n\n"
        "Règles du jeu:\n"
        "On distribue à chaque joueur 3 cartes.\n"
        "Un joueur est désigné comme seigneur des ténèbres.\n"
        "Grâce aux 3 cartes de sa main, il raconte aux autres joueurs la mission qu'il leur a confiée.\n"
        "Il donne la parole à un joueur qui se défend grâce à au moins une de ses cartes.\n"
        "Le seigneur des ténèbres donne ensuite la parole à un joueur accusé pour qu'il se défende, et ainsi de suite.\n"
        "Si les explications d’un joueur contredisent d’autres informations ou ne satisfont pas le seigneur des ténèbres, il reçoit un regard noir.\n"
        "Le premier joueur à recevoir 3 regards noirs est désigné coupable et la partie est terminée."
    )