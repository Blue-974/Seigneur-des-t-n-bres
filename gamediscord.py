from discord import *
from discord.ext import tasks
import game

intents = Intents.all()
client = Client(intents=intents)

tree = app_commands.CommandTree(client)

# Status personnaliser à remplacer par "Seigneur des Ténèbres" (affichera "Joue à Seigneur des Ténèbres")
custom_status = Game("Indisponible") 

# Listes des serveurs sur lesquelles les commandes apparaitront (pour des raisons d'optimisation)
allowed_servers = [Object(id=1299459410351095879)] 

# Les classes ci dessous sont des preset de message contenant des boutons ou des menu de selection
class StartUI(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self = self

    @ui.button(label="Règles du Jeu", style=ButtonStyle.grey)
    async def rules(self, interaction:Interaction, button:ui.Button):
        await interaction.response.send_message(game.rules_text,ephemeral=True)

    @ui.button(label="Rejoindre la partie", style=ButtonStyle.grey)
    async def join(self, interaction:Interaction, button:ui.Button):
        if game.add_player(interaction.user.id,interaction.user):
            await interaction.response.send_message(f"{interaction.user.nick} a rejoint la partie !")
        else:
            await interaction.response.send_message(f"Tu es déjà dans la partie ou la limite de joueur (24) a été atteinte !",ephemeral=True)
    
    @ui.button(label="Commencer", style=ButtonStyle.blurple)
    async def begin(self, interaction:Interaction, button:ui.Button):
        if game.start() == False:
            await interaction.response.send_message("Echec de la partie",ephemeral=True)
        else:
            chan : channel= interaction.channel
            await chan.send("Début de la Partie !")
            await chan.send(view=SelectPlayerUI())

class SelectPlayerUI(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @ui.select(placeholder="selectionner le seigneur des ténèbres",min_values = 1, max_values=len(game.players)+1,options=game.player_options)
    async def select_player(self, interaction:Interaction, select):
        for p in game.players:
            if p.sdt == True:
                await interaction.response.send_message("Un joueur a déjà été désigné comme Seigneur des ténèbres !" ,ephemeral=True)
                return
        if select.values[0] == "1":
            chan : channel= interaction.channel
            rand_p = game.select_random_player()
            await chan.send(f"{rand_p.data.nick} a été choisi comme seigneur des ténèbres !")
            rand_p.sdt = True
        else:

            for p in game.players:
                if p.id == select.values[0]:
                    await chan.send(f"{p.data.nick} a été choisi comme seigneur des ténèbres !")
                    p.sdt = True
            
@client.event
async def on_ready():
    await client.change_presence(status=Status.online, activity=custom_status)
    for server in allowed_servers :
        await tree.sync(guild=server)
    await client.wait_until_ready()
    print(f'Connecté en tant que {client.user}')

@tree.command(name="rules", description = "Affiche les règles du jeu.", guilds=allowed_servers)
async def rules(ctx):
    if game.game_state != 0:
        await ctx.response.send_message(game.rules_text,ephemeral = True)
    else:
        await ctx.response.send_message(game.rules_text,ephemeral = False)

@tree.command(name="start", description = "Permet de commencer le jeu", guilds=allowed_servers)
async def start(ctx : Interaction):
    await ctx.response.send_message(view = StartUI())

@tree.command(name="stop", description = "Arrête prématurément le jeu", guilds=allowed_servers)
async def start(ctx : Interaction):
    game.reset()
    await ctx.response.send_message("Partie arrêtée !")


# Remplace 'INSERER TOKEN VALIDE ICI' par le token du client
client.run('INSERER TOKEN VALIDE ICI')