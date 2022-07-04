import discord
import datetime
import time
from discord.ext import commands
from discord_components import *

class staffcommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rules(self, ctx):
        await ctx.send(file=discord.File('C:\\Users\\jkapt\\PycharmProjects\\shooterboy_bot\\Images2\\rules2.png'))
        await ctx.send('**1.** Do not be rude or disrespectful towards others. This includes using racist, homophobic, hateful, or otherwise bigoted speech.\n\n**2.** No controversial topics such as religion, gender, sexuality, politics, race, etcetera.\n\n**3.** No NSFW, porn, gore or explicit content.\n\n**4.** Please limit and be reasonable with the promotion of content.\n\n**5.** No spam or repeated use of messages and media.\n\n**6.** Please familiarize yourself with the official resources from Discord, as they are also applicable.')
        await ctx.send(file=discord.File('C:\\Users\\jkapt\\PycharmProjects\\shooterboy_bot\\Images2\\punishment.png'))
        await ctx.send('**1st Infraction:** A warning will be issued to you.\n\n**2nd Infraction:** You will be muted.\n\n**3rd Infraction:** You will be banned.\n\n**Note:** In order to report an offender please message an online staff member. Please do not spam staff members as they reserve the right to block or mute you!')

def setup(client):
  client.add_cog(staffcommands(client))