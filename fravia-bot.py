import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

description = '''Oi meu nome é Fravia, eu sou o bot aqui do MenteBinária, manda um ?help e eu te falo no que posso ajudar.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description='Search for asm instructions')
async def asm(asm_cmd : str):
    """Search for asm instructions"""
    url = 'http://faydoc.tripod.com/cpu/{}.htm'.format(asm_cmd.lower())
    r = requests.get(url)
    if r.status_code == 404:
        await bot.say('Poh brother essa instrução existe não.')
    else:
        raw_html = r.text.split('Description</b><br>')[1].split('<table border=1 cellpadding=5 cellspacing=0>')[0]
        cleantext = BeautifulSoup(raw_html, "lxml").text
        await bot.say(cleantext.split('\n')[0])
        await bot.say(url)

bot.run('API_KEY_HERE')
