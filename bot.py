from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch
from nextcord.ext import commands
from discord.utils import get
import os
import datetime
import json
import discord
import requests
import discord
import asyncio
import time
import os

#import classes here
import assist, staffcommands

if __name__ == '__main__':

    intents = discord.Intents.all()
    intents.members = True

    # command prefix
    client = commands.Bot(intents=intents, command_prefix='!')

    #initiate new classes
    cogs = [assist, staffcommands]
    for i in range(len(cogs)):
        cogs[i].setup(client)

    # Authentication with Twitch API.
    client_id = "ybwr1vdufov389eau5tcxqed837et8"
    client_secret = "7a1so44ylbvs4w54b3128uj7x4ydpg"
    twitch = Twitch(client_id, client_secret)
    twitch.authenticate_app([])
    TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
    API_HEADERS = {
        'Client-ID': client_id,
        'Accept': 'application/vnd.twitchtv.v5+json',
    }

    def checkuser(username):
        url = "https://gql.twitch.tv/gql"
        query = """query($login: String) {
          user(login: $login) {
            stream {
              id
            }
          }
        }"""
        return True if requests.post(url, json={"query": query, "variables": {"login": username}},
                                     headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()['data']['user'][
            'stream'] else False

    # Command to add Twitch usernames to the json.
    @client.command(name='addtwitch', help='Adds your Twitch to the live notifs.', pass_context=True)
    async def add_twitch(ctx, twitch_name):
        # Opens and reads the json file.
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())

        # Gets the users id that called the command.
        user_id = ctx.author.id
        # Assigns their given twitch_name to their discord id and adds it to the streamers.json.
        streamers[user_id] = twitch_name

        # Adds the changes we made to the json file.
        with open('streamers.json', 'w') as file:
            file.write(json.dumps(streamers))
        # Tells the user it worked.
        await ctx.send(f"Added {twitch_name} for {ctx.author} to the notifications list.")

    #welcome new users
    @client.event
    async def on_member_join(member):
        channel = client.get_channel(982528568561131540)
        await channel.send(f"Hey {member.mention}, welcome to my discord! 👋🏼")

    @client.event
    async def on_ready():
        print("Your bot is now running!")
        #activity status displayed by bot
        await client.change_presence(activity=discord.Game('!assist'))
        # Defines a loop that will run every 10 seconds (checks for live users every 10 seconds).
        @tasks.loop(seconds=5)
        async def live_notifs_loop():
            # Opens and reads the json file
            with open('streamers.json', 'r') as file:
                streamers = json.loads(file.read())
            # Makes sure the json isn't empty before continuing.
            if streamers is not None:
                # Gets the guild, 'twitch streams' channel, and streaming role.
                guild = client.get_guild(982526779996659752)
                channel = client.get_channel(984678013872525353)
                #role = get(guild.roles, id=982527150819250196)
                # Loops through the json and gets the key,value which in this case is the user_id and twitch_name of
                # every item in the json.
                for user_id, twitch_name in streamers.items():
                    # Takes the given twitch_name and checks it using the checkuser function to see if they're live.
                    # Returns either true or false.
                    status = checkuser('shooterboy')
                    # Gets the user using the collected user_id in the json
                    user = client.get_user(int(user_id))
                    # Makes sure they're live
                    if status is True:

                        msg = (await client.get_channel(984678013872525353).history(limit=1).flatten())[0]
                        if msg.created_at.date() != datetime.datetime.now(datetime.timezone.utc).date():
                            await channel.send(
                                f"Hey @everyone, Shooterboy is now streaming on Twitch!"
                                f"\nhttps://www.twitch.tv/{twitch_name}")
                            print(f"{user} started streaming. Sending a notification.")
                            break

                        # Checks to see if the live message has already been sent.
                        async for message in channel.history(limit=200):
                            # If it has, break the loop (do nothing).
                            if message.content and "is now streaming" in message.content:
                                break
                            # If it hasn't, assign them the streaming role and send the message.
                            else:
                                # Gets all the members in your guild.
                                #async for member in guild.fetch_members(limit=None):
                                    # If one of the id's of the members in your guild matches the one from the json and
                                    # they're live, give them the streaming role.
                                    #if member.id == int(user_id):
                                        #await member.add_roles(role)
                                # Sends the live notification to the 'twitch streams' channel then breaks the loop.
                                await channel.send(
                                    f"Hey @everyone, Shooterboy is now streaming on Twitch!"
                                    f"\nhttps://www.twitch.tv/{twitch_name}")
                                print(f"{user} started streaming. Sending a notification.")
                                break


                    # If they aren't live do this:
                    else:
                        return 'hi'
        # Start your loop.
        live_notifs_loop.start()

TOKEN = "OTgyNTM0MDcyMTMzODk4MjUw.G01iPp.Vt3Dcjkt0pkQDAL5Qyw1F4nkXrH-m4nPbEod0U"
client.run(os.environ['DISCORD_TOKEN'])