import os
import textwra
import requests
import feedparser
from lxml import html
from bs4 import BeautifulSoup
from discord.ext import commands

description = '''Hi my name is Fravia I'm here to help you'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description='Search for syscalls on http://man7.org/')
async def syscall(syscall_name : str):
    """
    Search for syscalls on http://man7.org/
    Examples:
    ?syscall read
    """
    url = 'http://man7.org/linux/man-pages/man2/{}.2.html'.format(syscall_name.lower())
    r = requests.get(url)
    if r.status_code != 404:
        tree = html.fromstring(r.text)
        code = '''```c
        {}```'''.format(textwrap.dedent(''.join(tree.xpath('/html/body/pre[3]')[0].itertext())))
        desc = textwrap.dedent(''.join(tree.xpath('/html/body/pre[4]')[0].itertext()))
        if len(desc) >= 2000:
            await bot.say('Poh brother a descrição dessa syscall é muito grande, não consigo enviar, mas se liga que to mandando o link ai em baixo')
        else:
            await bot.say(desc)
            await bot.say(code)
        await bot.say(url)
    else:
        await bot.say('Poh brother essa syscall existe não.')

@bot.command(description='Search for shellcodes on http://shell-storm.org.')
async def shellcode(search : str):
    """
    Search for shellcodes on http://shell-storm.org
    Examples:
    ?shellcode linux (search with single parameter)
    ?shellcode linux|86|reverse (search with multiple parameters)
    """
    url = 'http://shell-storm.org/api/?s={}'.format(search.replace('|','*'))
    r = requests.get(url)
    for line in r.text.split('\n'):
        line = line.split('::::')
        if len(line) == 5:
            await bot.say('%s - %s' % (line[2],line[4]))

@bot.command(description='Decode opcodes to asm')
async def d_opcodes(payload : str,arch : str):
    """
    Decode opcodes to asm
    Ex: ?d_opcodes 5589E583EC0A686E2F7368682F2F626931C083C00B89E331D231D1CD80 x86
    """
    url = 'https://defuse.ca/online-x86-assembler.htm#disassembly2'
    data = {'hexstring':payload,'arch':arch,'submit':'Disassemble'}
    r = requests.post(url,data=data)
    tree = html.fromstring(r.text)
    await bot.say('```{}```'.format(''.join(tree.xpath('//*[@id="content"]/div[2]/div[4]/p/text()')).strip()))

@bot.command(description='Search for an asm instruction Ex: ?asm inc')
async def asm(asm_cmd : str):
    """Search for asm commands"""
    url = 'http://faydoc.tripod.com/cpu/{}.htm'.format(asm_cmd.lower())
    r = requests.get(url)
    if r.status_code == 404:
        await bot.say('Poh brother essa instrução existe não.')
    else:
        try:
            raw_html = r.text.split('Description</b><br>')[1].split('<table border=1 cellpadding=5 cellspacing=0>')[0]
            cleantext = BeautifulSoup(raw_html, "lxml").text
            await bot.say(cleantext.split('\n')[0])
            await bot.say(url)
        except:
            await bot.say('Brother ou eu fiz merda ou você fez merda, mas deu alguma coisa errada aqui.')

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

bot.run(os.environ["API_KEY"])
