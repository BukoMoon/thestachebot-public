import discord
import json
import sys
import os
import logging
import configparser
from discord import message
from discord.client import Client
from discord.ext import commands
from discord.ext.commands import bot


from main_cog import main

intents = discord.Intents(messages=True, guilds=True, members=True)
client = commands.Bot(command_prefix='$', intents=intents)

data = json.load(open(os.path.realpath(os.path.dirname(sys.argv[0])) + '/data.json', 'r+t'))
db = data['data']
status = data['data']['status']
affirmations = data['data']['affirmations']

discord_token = ''
discord_logfile = ''
discord_debug = False
discord_clientid = ''
discord_clientsecret = ''
league_api = ''


def __init__() -> None:
    load_configuration()
    if discord_debug:
        start_logging()

    client.add_cog(main(client, status, db, affirmations, discord_clientid, discord_clientsecret))

    client.run(discord_token)

def load_configuration():
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')

    try:
        bot_config = config_file['Bot']
    except KeyError:
        print('[Bot] section not found in config file. Please set values for [Bot] in config.ini')
        sys.exit()
    
    global discord_token
    try:
        discord_token = bot_config['Token']
    except KeyError:
        print('Token not found in Bot section of config file. Please set Token under [Bot] in config.ini')

    global discord_debug
    try:
        discord_debug = bot_config['Debug']
    except KeyError:
        print('Debug not found in Bot section of config file. Please set Debug under [Bot] in config.ini')
    
    global discord_logfile
    try:
        discord_logfile = bot_config['Logfile']
    except KeyError:
        print('Logfile not found in Bot section of config file. Please set Logfile under [Bot] in config.ini')
    
    global discord_clientid
    try:
        discord_clientid = bot_config['ClientId']
    except KeyError:
        print('Client Id not found in Bot section of config file. Please set Client Id under [Bot] in config.ini')

    global discord_clientsecret
    try:
        discord_clientsecret = bot_config['ClientSecret']
    except KeyError:
        print('Client Secret not found in Bot section of config file. Please set Client Secret under [Bot] in config.ini')  

    global league_api
    try:
        league_api = bot_config['LeagueApi']
    except KeyError:
        print('League Api not found in Bot section of config file. Please set League Api under [Bot] in config.ini')


def start_logging():
    logging.basicConfig(filename=os.path.realpath(os.path.dirname(sys.argv[0])) + '/' + discord_logfile, level=logging.DEBUG)

if __name__ == '__main__':
    __init__()