# "Oui, Seigneur des ténèbres" adapté en bot discord par Scottellow et Blue974

from discord import *
from discord.ext import tasks
import game

intents = Intents.all()
client = Client(intents=intents)

tree = app_commands.CommandTree(client)

# Status personnalisé à remplacer par "Oui, Seigneur des Ténèbres" (affichera "Joue à Oui, Seigneur des Ténèbres")
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
async def rules(ctx):
    await send_rules(ctx)
        

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
    sdt_player : game.Player = game.Player(user_id=0,user_data=None)
    if value == "1":
        sdt_player = game.select_random_player()
    else:
        for p in game.players:
            if str(p.id) == value:
                sdt_player = p
    view = ui.View()
    HandButton = ui.Button(label="Voir sa main", style=ButtonStyle.blurple)
    HandButton.callback = tell_stat
    view.add_item(HandButton)
    player_options = await optionsgenerator()
    PSelect = ui.Select(placeholder="Désignez un.e joueur.se",min_values = 1, max_values=1,options=player_options)
    PSelect.callback = lambda param : send_blame(param,PSelect.values[0],0,game.Player(user_id=0))
    view.add_item(PSelect)
    sdt_player.sdt = True
    game.distribute_cards()
    await ctx.response.send_message(f"{sdt_player.data.display_name} a été choisi comme seigneur des ténèbres !", view = view)

async def turn(player : game.Player, round_nm : int, chan : channel):
    view = ui.View()

    C0Button = ui.Button(label="Jouer Carte 0", style=ButtonStyle.grey)
    C0Button.callback = lambda param : use_card(param, player, 0)

    C1Button = ui.Button(label="Jouer Carte 1", style=ButtonStyle.grey)
    C1Button.callback = lambda param : use_card(param, player, 1)

    C2Button = ui.Button(label="Jouer Carte 2", style=ButtonStyle.grey)
    C2Button.callback = lambda param : use_card(param, player, 2)

    HandButton = ui.Button(label="Voir sa main", style=ButtonStyle.blurple)
    HandButton.callback = tell_stat

    player_options = await optionsgenerator()
    PSelect = ui.Select(placeholder="Désignez un.e joueur.se",min_values = 1, max_values=1,options=player_options)
    PSelect.callback = lambda param : send_blame(param,PSelect.values[0],round_nm)

    IntButton = ui.Button(label="Interruption", style=ButtonStyle.blurple)
    IntButton.callback = lambda param : interrupt(param, player)

    BlameButton = ui.Button(label="Jeter un regard noir !", style=ButtonStyle.red)
    BlameButton.callback = lambda param : blame(param,player)

    for i in [C0Button,C1Button,C2Button,HandButton,PSelect,IntButton,BlameButton]:
        view.add_item(i)
    
    await chan.send(f"## {player.data.display_name}, le Seigneur des Ténèbre veut t'entendre !\nUtilise tes cartes excuse pour rejeter la faute sur quelqu'un d'autre !",view=view)

async def send_blame(ctx : Interaction, value : str, round_nm : int):
    if game.get_player(ctx.user.id).sdt:
        for p in game.players:
            if str(p.id) == value:
                if p.sdt :
                    await ctx.response.send_message("Le seigneur des ténèbres ne peut pas être blamé pour l'échec de la mission!", ephemeral= True)
                else:
                    game.distribute_cards()
                    await turn(p, round_nm+1,ctx.channel)
    else :
        await ctx.response.send_message("Seul le seigneur des ténèbres peut blamer quelqu'un !", ephemeral=True)

async def use_card(ctx : Interaction, player : game.Player, id : int):
    caller : game.Player = game.get_player(ctx.user.id)
    if caller == player:
        card = player.use_cards(id)
        if card != "":
            await ctx.response.send_message(f"{player.data.display_name} a joué : {card}")
        else :
            await ctx.response.send_message("Vous ne pouvez pas jouer cette carte", ephemeral=True)

async def tell_stat(ctx : Interaction):
    player : game.Player = game.get_player(ctx.user.id)
    if player.sdt :
        await ctx.response.send_message(f"Vous êtes le Seigneur des Ténèbres.\n\n Vos cartes sont :\n0 - {player.hand[0]}\n1  - {player.hand[1]}\n2 - {player.hand[2]}" , ephemeral= True)
    else:
        await ctx.response.send_message(f"Vous avez reçu **{player.blame}** regards noirs.\n\n Vos cartes sont :\n0 - {player.hand[0]}\n1  - {player.hand[1]}\n2 - {player.hand[2]}" , ephemeral= True)

async def interrupt(ctx : Interaction, turn_p : game.Player):
    player : game.Player = game.get_player(ctx.user.id)
    
    if player == turn_p:
        await ctx.response.send_message("Il ne serait pas judicieux de vous interrompre vous même !", ephemeral=True)
        return

    for d,c in enumerate(player.hand):
        if c == "Interruption":
            player.hand[d] = ""
            view = ui.View()

            C0Button = ui.Button(label="Jouer Carte 0", style=ButtonStyle.grey)
            C0Button.callback = lambda param : use_card(param, player, 0)

            C1Button = ui.Button(label="Jouer Carte 1", style=ButtonStyle.grey)
            C1Button.callback = lambda param : use_card(param, player, 1)

            C2Button = ui.Button(label="Jouer Carte 2", style=ButtonStyle.grey)
            C2Button.callback = lambda param : use_card(param, player, 2)

            HandButton = ui.Button(label="Voir sa main", style=ButtonStyle.blurple)
            HandButton.callback = tell_stat

            for i in [C0Button,C1Button,C2Button,HandButton]:
                view.add_item(i)

            await ctx.response.send_message(f"{player.data.display_name} vous as interrompu, il choisit une carte à vous imposer !",view=view)
            return
    await ctx.response.send_message("Vous n'avez pas de carte Interruption !", ephemeral=True)

async def blame(ctx : Interaction, player : game.Player):
    if game.get_player(ctx.user.id).sdt:
        chan = ctx.channel
        if player.suffer():
            await chan.send(f"## {player.data.display_name}, c'était de ta faute depuis le début ! \n Vous avez reçu 3 regards noirs et perdu la partie")
            game.reset()
        else:
            await ctx.response.send_message(f"{player.data.display_name} a reçu un regard noir ! ({player.blame}/3)")
    else :
        ctx.response.send_message("Seul le seigneur des ténèbres peut jeter un regard noir !", ephemeral=True)

async def send_rules(ctx):
    if game.game_state:
        await ctx.response.send_message(game.rules_text,ephemeral = True)
    else:
        await ctx.response.send_message(game.rules_text,ephemeral = False)
# Remplace 'INSERER TOKEN VALIDE ICI' par le token du client
client.run('INSERER TOKEN VALIDE ICI')