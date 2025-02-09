# Oui Seigneur des ténèbres python

import random

# règles du jeu
print("Voici les règles: On distribue à chaque joueur 3 cartes. Un joueur est désigné comme seigneur des ténèbres Grâce aux 3 cartes de sa main il raconte aux autres joueurs la mission qu'il leur a confié. Il donne la parole à un joueur qui se défend grâce à au moins une de ses cartes. Le seigneur des ténèbres donne la parole à un joueur qui a été accusé pour qu'il se défende et ainsi de suite. Quand les explications d’un joueur qui contredisent d’autres informations ou qui ne satisfassent pas le seigneur des ténèbres il se prend un regard noir, le premier joueur qui en récupère 3 est désigné comme coupable, la partie est donc terminée.")


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