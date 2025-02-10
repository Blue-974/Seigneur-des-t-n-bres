from discord import *
import game

class Start(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @ui.button(label="Rejoindre la partie", style=ButtonStyle.grey)
    async def join(self, interaction:Interaction, button:ui.Button):
        await interaction.response.send_message("Test")
    
    @ui.button(label="Commencer", style=ButtonStyle.blurple)
    async def begin(self, interaction:Interaction, button:ui.Button):
        await interaction.response.send_message("Begin")