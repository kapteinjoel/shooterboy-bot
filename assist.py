import discord
import datetime
import time
from discord.ext import commands
from discord_components import *

class assist(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.buttons = [[Button(style=2, label='Back', id='1'), Button(style=2, label='Next', id='2')]]
        DiscordComponents(client)

    @commands.command()
    async def assist(self, ctx):
        current_page = 1
        max_pages = 1
        embed = discord.Embed(title='Server Commands', description='Page {}/{}'.format(current_page, max_pages),
                              color=0xF9c442)
        message = await ctx.send(
            embed=embed,
            components=self.buttons
        )
        while True:
            event = await self.client.wait_for('button_click')
            if event.channel is not ctx.channel:
                return
            if event.channel == ctx.channel:
                response = event.component.id
                if response is None:
                    await event.channel.send('Something went wrong. Please try again.')
                if event.channel == ctx.channel:
                    if response == '1':
                        current_page -= 1

                        await message.edit(embed=discord.Embed(title='Server Commands',
                                                               description='Page {}/{}'.format(current_page, max_pages)))
                        await event.respond(type=7)
                    if response == '2':
                        current_page += 1
                        await message.edit(embed=discord.Embed(title='Server Commands',
                                                               description='Page {}/{}'.format(current_page, max_pages)))
                        await event.respond(type=7)
    @commands.command()
    async def msghistory(self, ctx):
        msg = (await self.client.get_channel(982665005277282316).history(limit=1).flatten())[0]
        await ctx.send(msg.created_at.date())

        await ctx.send(msg.created_at)
        await ctx.send((datetime.datetime.now(datetime.timezone.utc)).time(datetime.hour))

    @commands.command()
    async def lastmsg(self,ctx):
        msg = (await self.client.get_channel(984678013872525353).history(limit=1).flatten())[0]
        print(msg.created_at)
        print(msg.created_at.date())
        print(datetime)
        if msg.created_at.date() == datetime.date.today():
            await ctx.send('true')

def setup(client):
  client.add_cog(assist(client))