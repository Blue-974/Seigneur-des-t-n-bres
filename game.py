# Oui Seigneur des ténèbres python

import random

# règles du jeu
print("Voici les règles: ")


# Liste des cartes
listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"]
# Main du joueur
main = []

# Fonction pour piocher des cartes
def draw_cards():
    if len(listcard) < 3:
        print("Tu n'a pas assez de carte pour jouer")
    else:
        # Vide la main
        main.clear()
        # Pioche 3 cartes
        main.extend(random.sample(listcard, 3))
        print("Voici tes cartes: ", main)


# Fonction pour utiliser des cartes
def use_cards():
    while True:
        card_to_use = input("Quelle carte veux-tu utiliser? (ou tape 'exit' pour quitter): ")
        if card_to_use == 'exit':
            break
        if card_to_use in main:
            # Retire la carte de la main
            main.remove(card_to_use)
            # Pioche une nouvelle carte
            main.extend(random.sample(listcard, 1))
            print(f"Tu as utilisé la carte {card_to_use}. Voici ta nouvelle carte: {main}")
        else:
            print(f"La carte {card_to_use} n'est pas dans ta main.")


# Lancement du jeu
draw_cards()
# Utilisation des cartes
use_cards()