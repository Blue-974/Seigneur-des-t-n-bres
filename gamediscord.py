import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des cartes
listcard = ["card1", "card2", "card3", "card4", "card5", "card6", "card7", "card8", "card9", "card10"]

# Dictionnaire pour stocker les mains des joueurs
player_hands = {}

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.command()
async def rules(ctx):
    """Affiche les règles du jeu."""
    rules_text = (
        "Voici les règles du jeu:\n"
        "1. Utilisez `!draw` pour piocher trois cartes.\n"
        "2. Utilisez `!use <nom_de_carte>` pour jouer une carte et en tirer une nouvelle.\n"
        "3. Les cartes sont envoyées en message privé pour garder votre main secrète.\n"
        "4. Amusez-vous et jouez stratégique !\n\n"
        "Voici les règles détaillées:\n"
        "- On distribue à chaque joueur 3 cartes.\n"
        "- Un joueur est désigné comme seigneur des ténèbres.\n"
        "- Grâce aux 3 cartes de sa main, il raconte aux autres joueurs la mission qu'il leur a confiée.\n"
        "- Il donne la parole à un joueur qui se défend grâce à au moins une de ses cartes.\n"
        "- Le seigneur des ténèbres donne ensuite la parole à un joueur accusé pour qu'il se défende, et ainsi de suite.\n"
        "- Si les explications d’un joueur contredisent d’autres informations ou ne satisfont pas le seigneur des ténèbres, il reçoit un regard noir.\n"
        "- Le premier joueur à recevoir 3 regards noirs est désigné coupable et la partie est terminée."
    )
    await ctx.send(rules_text)

@bot.command()
async def draw(ctx):
    """Permet de piocher des cartes."""
    if ctx.author.id not in player_hands:
        player_hands[ctx.author.id] = []
    
    if len(listcard) < 3:
        await ctx.author.send("Tu n'as pas assez de cartes pour jouer.")
    else:
        player_hands[ctx.author.id] = random.sample(listcard, 3)
        await ctx.author.send(f"Voici tes cartes: {', '.join(player_hands[ctx.author.id])}")
        await ctx.send(f"{ctx.author.mention}, tes cartes ont été envoyées en message privé.")

@bot.command()
async def use(ctx, card: str):
    """Permet d'utiliser une carte."""
    if ctx.author.id not in player_hands or not player_hands[ctx.author.id]:
        await ctx.author.send("Tu dois d'abord piocher des cartes avec !draw.")
        return

    if card in player_hands[ctx.author.id]:
        player_hands[ctx.author.id].remove(card)
        if len(listcard) > 0:
            new_card = random.choice(listcard)
            player_hands[ctx.author.id].append(new_card)
            await ctx.author.send(f"Tu as utilisé la carte {card}. Voici ta nouvelle main: {', '.join(player_hands[ctx.author.id])}")
        else:
            await ctx.author.send(f"Tu as utilisé la carte {card}, mais il n'y a plus de cartes à piocher.")
    else:
        await ctx.author.send(f"La carte {card} n'est pas dans ta main.")

# Remplace 'TON_TOKEN_ICI' par le token de ton bot
bot.run('TON_TOKEN_ICI')