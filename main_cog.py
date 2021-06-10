import random
import discord
from random import randint, choice
import json
import sys
import os
from discord import message
from discord import client
from discord import embeds
from discord.ext.commands.core import command
import requests
from discord.ext import commands, tasks
from datetime import datetime


FAMOUS_NAMES = [
    'Sylvester Stallone', 'Arnold Schwarzenegger', 'Clint Eastwood', 'Professor Akali', 'Dwayne "The Rock" Johnson',
    'Emma Watson', 'Leonardo DiCaprio', 'Young MA', 'Bobby Shmurda', 'The Booba', 'Jeremiah Cole'
]

access_token = ''
access_month = ''

class main(commands.Cog):
    def __init__(self, client, status, db, affirmations, clientid, secretkey):
        self.clientid = clientid
        self.clientsecret = secretkey

        self.client = client
        self.status = status       
        self.db = db
        self.affirmations = affirmations

    def authorisation(self):
        body = {
            'client_id': self.clientid,
            'client_secret': self.clientsecret,
            'grant_type': 'client_credentials'
        }

        r = requests.post('https://id.twitch.tv/oauth/token', body)
        keys = r.json()
        return keys

    def check_user(self, user):
        global access_token
        global access_month
        current_month = datetime.now().month
        if access_token == '' or current_month != access_month:
            keys = self.authorisation()
            access_token = keys['access_token']
            access_month = current_month
        headers = {
            'Client-ID': self.clientid,
            'Authorization': 'Bearer ' + access_token
        }

        try:
            stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + user, headers=headers)
            stream_data = stream.json()
            if len(stream_data['data']) == 1:
                return True
            else:
                return False
        except Exception as e:
            print('Error checking user: ', e)
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        self.db_check.start()
        print('We have logged in as {0.user}'.format(self.client))
       
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(805548508345008130)
        embed = discord.Embed(
            title=f'Welcome {member.name}', 
            description=f'Thanks for joining **{member.guild.name}**! You are now apart of this!',
            timestamp=datetime.utcnow()
            )
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)


    @tasks.loop(minutes=45)
    async def change_status(self):
        if self.check_user('Number1Lover'):
            await self.client.change_presence(activity=discord.Streaming(name="Fastest Growing Twitch Stream", url='https://www.twitch.tv/Number1Lover'))
        else:
            i = random.randint(1, 9)
            if i <= 3:
                # Setting `Playing ` status
                await self.client.change_presence(activity=discord.Game(name=choice(self.status['game'])))
            elif 3 < i <= 6:
                # Setting `Listening ` status
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=choice(self.status['music'])))
            elif i >= 7:
                # Setting `Watching ` status
                await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(self.status['watch'])))

    @tasks.loop(hours=1)
    async def db_check(self):
        options = FAMOUS_NAMES
        if 'names' in self.db.keys():
            options = options + self.db['names']

    @commands.command(name='author', help='Bot creator')
    async def author(ctx):
        await ctx.send('Bot created by `Buko`')

    @commands.command(name='aboutme', help="Displays a quick description of the Number1Lover's experience with the ladies")
    async def aboutme(ctx):
            quote = open(os.path.realpath(os.path.dirname(sys.argv[0])) + '/de_propos.data', 'r').readline().replace('\\n', '\n')
            await ctx.send(quote)

    @commands.command(name='accordingto', help='Who says the Number1Lover is the fastest growing twitch streamer in Australia?')
    async def accordingto(self,ctx):
        rng = randint(0, 10)
        if rng <= 3:
            response = requests.get("https://zenquotes.io/api/random")
            json_data = json.loads(response.text)
            quote = f"I'm the fastest growing twitch stream in Australia, according to {json_data[0]['a']}" 
            await ctx.send(quote)
        elif rng >= 4:
            await ctx.send(f"I'm the fastest growing twitch stream in Australia, according to {choice(FAMOUS_NAMES)}")

    @commands.command(name='newname', help='Adds a name to the list')
    async def newname(self, ctx):
        new_name = ctx.split("$new ", 1)[1]
        if 'names' in self.db.keys():
            names = self.db['names']
            names.append(new_name)
            self.db['names'] = names
        else:
            self.db['names'] = [new_name]

        await ctx.send(choice(self.affirmations))

    @commands.command(name='removename', help='Removes a name from the list.')
    async def removename(self, ctx):
        names = []
        if 'names' in self.db.keys():
            try:
                index = int(ctx.split('$del', 1)[1])
            except ValueError:
                await message.channel.send("Women don't give me digits like this.")
    
            names = self.db['names']
            if len(names) > index:
                del names[index]
            self.db['names'] = names
            names = self.db['names']
        await message.channel.send(names)

    @commands.command(name='inspire', help='Sends an inspirational message.')
    async def inspire(ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + ' -' + json_data[0]['a']
        await message.channel.send(quote)