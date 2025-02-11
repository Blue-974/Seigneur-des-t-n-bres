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

@client.event
async def on_ready():
    await client.change_presence(status=Status.online, activity=custom_status)
    for server in allowed_servers :
        await tree.sync(guild=server)
    await client.wait_until_ready()
    print(f'Connecté en tant que {client.user}')

@tree.command(name="rules", description = "Affiche les règles du jeu.", guilds=allowed_servers)
async def send_rules(ctx):
        if game.game_state:
            await ctx.response.send_message(game.rules_text,ephemeral = True)
        else:
            await ctx.response.send_message(game.rules_text,ephemeral = False)

@tree.command(name="start", description = "Permet de commencer le jeu", guilds=allowed_servers)
async def start(ctx : Interaction):
    view = ui.View()

    RulesButton = ui.Button(label="Règles du Jeu", style=ButtonStyle.grey)
    RulesButton.callback = send_rules

    JoinButton = ui.Button(label="Rejoindre la partie", style=ButtonStyle.grey)
    JoinButton.callback = add_player

    StartButton = ui.Button(label="Commencer", style=ButtonStyle.blurple)
    StartButton.callback = start

    buttons = [RulesButton,JoinButton,StartButton]
    for b in buttons:
        view.add_item(item=b)
    await ctx.response.send_message("## Oui, Seigneur des Ténèbres !\nLa partie est sur le point de se lancer ! Limite de joueur max : 24",view=view)

@tree.command(name="stop", description = "Arrête prématurément le jeu", guilds=allowed_servers)
async def stop(ctx : Interaction):
    game.reset()
    await ctx.response.send_message("Partie arrêtée !")


async def add_player(ctx):
    if game.add_player(ctx.user.id,ctx.user):
        await ctx.response.send_message(f"{ctx.user.display_name} a rejoint la partie !")
    else:
        await ctx.response.send_message(f"Tu es déjà dans la partie, la partie a déjà commencé ou la limite de joueur (24) a été atteinte !",ephemeral=True)

# Generateur d'option pour la selection du seigneur des tenebres
async def optionsgenerator():
    player_options = []
    for p in game.players:
        player_options.append(SelectOption(label=p.data.name,value=str(p.id)))
    player_options.append(SelectOption(label="Aléatoire",value="1"))
    return player_options

async def start(ctx):
    view = ui.View()
    if game.game_state:
        await ctx.response.send_message("Une partie est déjà en court !",ephemeral=True)
    elif game.start() == False:
        await ctx.response.send_message("Echec de la partie",ephemeral=True)
    else:
        player_options = await optionsgenerator()
        SdtSelect = ui.Select(placeholder="Désignez un.e joueur.se",min_values = 1, max_values=1,options=player_options)
        SdtSelect.callback = lambda param : sdt_select(param,SdtSelect.values[0])
        view.add_item(SdtSelect)
        await ctx.response.send_message("### Début de la Partie !\nDésignez votre seigneur des ténèbres",view=view)

async def sdt_select(ctx,value):
    for p in game.players:
             if p.sdt == True:
                 await ctx.response.send_message("Un joueur a déjà été désigné comme Seigneur des ténèbres !", ephemeral=True)
                 return
    if value == "1":
        rand_p = game.select_random_player()
        await ctx.response.send_message(f"{rand_p.data.display_name} a été choisi comme seigneur des ténèbres !")
        rand_p.sdt = True
    else:
        for p in game.players:
            if str(p.id) == value:
                await ctx.response.send_message(f"{p.data.display_name} a été choisi comme seigneur des ténèbres !")
                p.sdt = True

# Remplace 'INSERER TOKEN VALIDE ICI' par le token du client
client.run('INSERER TOKEN VALIDE ICI')