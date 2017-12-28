import discord
import requests
import feedparser
from lxml import html
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

@bot.command(description='Search for an asm instruction Ex: ?asm inc')
async def asm(asm_cmd : str):
    """Search for asm commands"""
    url = 'http://faydoc.tripod.com/cpu/{}.htm'.format(asm_cmd.lower())
    r = requests.get(url)
    if r.status_code == 404:
        await bot.say('Poh brother essa instrução existe não.')
    else:
        raw_html = r.text.split('Description</b><br>')[1].split('<table border=1 cellpadding=5 cellspacing=0>')[0]
        cleantext = BeautifulSoup(raw_html, "lxml").text
        await bot.say(cleantext.split('\n')[0])
        await bot.say(url)

@bot.command(description='Search for windows functions')
async def winapi(win_function : str):
    """Search for windows functions"""
    url = 'https://social.msdn.microsoft.com/search/en-US/feed?query={}&format=RSS&theme=windows'.format(win_function.lower())
    feed = feedparser.parse(url)
    if feed['entries']:
        url = feed['entries'][0]['link']
        if 'library/windows/desktop' not in url:
            await bot.say('Poh brother essa função existe não.')
        else:
            r = requests.get(url)
            tree = html.fromstring(r.text)
            await bot.say(''.join(tree.xpath('//*[@id="mainSection"]/p[1]/text()')))
            msg = '''```c
            {}```'''.format(tree.xpath('//*[@dir="ltr"]/div/pre/text()')[0])
            await bot.say(msg)
            await bot.say(url)
    else:
        await bot.say('Poh brother essa função existe não.')

bot.run('API GOES HERE')
