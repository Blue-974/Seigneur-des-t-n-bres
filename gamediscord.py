from discord import *
from discord.ext import tasks
import gameui
import game

intents = Intents.all()
client = Client(intents=intents)

tree = app_commands.CommandTree(client)

# Status personnaliser à remplacer par "Seigneur des Ténèbres" (affichera "Joue à Seigneur des Ténèbres")
custom_status = Game("Indisponible") 

# Listes des serveurs sur lesquelles les commandes apparaitront, ajouter un Object(id=id_du_server) pour chaque server autorisés.
# Si cette liste n'est pas remplie tous les serveurs sont autorisés, ce qui semble causer beaucoup de latence pour le chargement des commandes du bot.
# Actuellement seul mon serveur test est dans la liste.
allowed_servers = [Object(id=1079439311201648681)] 

# Liste des cartes
listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"]

# Dictionnaire pour stocker les mains des joueurs
player_hands = {}

@client.event
async def on_ready():
    await client.change_presence(status=Status.online, activity=custom_status)
    for server in allowed_servers :
        await tree.sync(guild=server)
    await client.wait_until_ready()
    print(f'Connecté en tant que {client.user}')

@tree.command(name="rules", description = "Affiche les règles du jeu.", guilds=allowed_servers)
async def rules(ctx):
    await ctx.response.send_message(game.rules_text)

@tree.command(name="start", description = "Permet de commencer le jeu", guilds=allowed_servers)
async def start(ctx):
    view = gameui.Start()
    await ctx.response.send_message(view = view)


# Remplace 'INSERER TOKEN VALIDE ICI' par le token du client
client.run('INSERER TOKEN VALIDE ICI')