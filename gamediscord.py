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
async def draw(ctx):
    # Permet de piocher des cartes
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
    # Permet d'utiliser une carte
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

# Remplace 'TON_TOKEN_ICI' par le token du bot
bot.run('TON_TOKEN_ICI')