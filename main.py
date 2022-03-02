print('==========start==========') #QQ startup & import module 
import os 
import sys
import json
import time
import random
import asyncio
import traceback
import urllib.request
import nextcord  
from nextcord.ext import commands 
from nextcord import Interaction, SlashOption, ChannelType
import mediawiki
from mediawiki import MediaWiki
from pytube import YouTube

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=["==","-"], intents=intents,help_command=None)


#QQ setup
@bot.event
async def on_ready():
    await bot.change_presence(activity = nextcord.Activity(name='Putin',type=nextcord.ActivityType.watching),status = nextcord.Status.online)
    print('==========login==========')
    thread = bot.get_channel(936550091160956978)
    await thread.send(f'\n__**login**__\ndevice: heroku\ntime: <t:{round(time.time())}:f>\nLatency: `{round(bot.latency * 1000)}`ms')

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    await bot.process_commands(message)

@bot.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        await sendmseg(ctx,2,mseg='**Command not found**',text='Click `help` to view tag list',view=sendhelp())
    else:
        # test = traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
        await sendmseg(ctx,4,mseg='An unexpected error was occur.',error=error)


#QQ user def func
def readcsv(url):
    with urllib.request.urlopen(url) as f:
        last = f.readlines()[-1]
        last2 = last.decode("utf-8") 
        data = last2.split(",")
        return data

async def sendmseg(user,types,mseg,text=None,delete=None,error=None,footer=None,view=None,back=False):
    element = [None, [None,nextcord.Color.green(),nextcord.Color.red(),nextcord.Color.blue(),nextcord.Color.orange()], [None,'<:check:903141744806346752>','<:cross:903141744919580692>', '<:info:903470117436928050>   ','<:error:903141745129320478> **error:**']]
    color = element[1][types]
    icon = element[2][types]
    embed = nextcord.Embed(description=f'{icon} {mseg}',color=color)
    if footer != None:
        embed.set_footer(text=footer)
    if error != None:
        view = senderror(error=error)
        test = traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
    if back == False:
        if text == None:
            await user.send(embed=embed,delete_after=delete,view=view)
        else:
            await user.send(text,embed=embed,delete_after=delete,view=view)
    else:
        return embed
    if view != None:
        await view.wait()

@bot.command() #lots of error handling here
async def err(ctx):
    raise Exception(f'**this is an fake error from {ctx.author.mention}** by using `=err`')

@bot.command() 
async def ping(ctx):
    await sendmseg(ctx,1,text=f'Latency: `{round(bot.latency * 1000)}`ms',mseg='**Pong!!**')

@bot.command() 
async def shutdown(ctx):
    if ctx.author.id != 734255881839050793:
        await sendmseg(ctx,2,'Only **bot developer** can use this command.')
    else:
        await sendmseg(ctx,1,'Shutting down...')
        sys.exit(0)

class senderror(nextcord.ui.View):
    def __init__(self,error):
        super().__init__()
        self.value = None
        self.error = error

    @nextcord.ui.button(label='print error', style=nextcord.ButtonStyle.grey, emoji='🖨️')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(self.error, ephemeral=True)
        # self.stop()

class sendhelp(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(nextcord.ui.Button(label='help', url='https://gist.github.com/lmjaedentai/df357af611371d875ad35d150339640f#commands'))

    @nextcord.ui.button(label='tags list', style=nextcord.ButtonStyle.grey, emoji='🖨️')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(self.error,files=['https://cdn.discordapp.com/attachments/893367501608599574/948523172523827200/unknown.png','https://cdn.discordapp.com/attachments/893367501608599574/948523172033077268/unknown.png','https://cdn.discordapp.com/attachments/893367501608599574/948523171680776232/unknown.png'], ephemeral=True)

class senddiscard(nextcord.ui.View):
    def __init__(self,error):
        super().__init__()
        self.value = None
        self.error = error

    @nextcord.ui.button(label='print error', style=nextcord.ButtonStyle.grey, emoji='🖨️')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(self.error, ephemeral=True)

@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji.name

    if message.author.id != bot.user.id or payload.member.id == bot.user.id:
        return
    if emoji == '❌':
        await message.delete()
    
    reaction = nextcord.utils.get(message.reactions, emoji=emoji)
    # await reaction.remove(payload.member)


#QQ bot cmd
@bot.slash_command(name='sk',description='Soul Knight Online Coop')
async def code(interaction: Interaction, code, comment=SlashOption(required=False)):
    output = ''
    for a in range(len(code)):
        output = output + f'`{code[a]}` '
    if comment == None:
        comment = ''
    embed=nextcord.Embed(description=f'code: {output}', color=0x2f3136)
    embed.set_author(name=f'Soul Knight Multiplayer', icon_url='https://i.imgur.com/2gQRdKN.png')
    embed.set_thumbnail(url='https://i.imgur.com/Xe6AbpC.png')
    await interaction.send(f'<@&893367490736963604> {comment}',embed=embed)

@bot.slash_command(name='covid',description='check covid 19 statistic in Malaysia') 
async def covid(interaction: Interaction):
    img = ["https://i.imgur.com/r8cpDgz.png",'https://i.imgur.com/Nfdps3y.png','https://i.imgur.com/dCaacT7.png','https://i.imgur.com/0CkAAct.png']
    cases = readcsv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
    deaths = readcsv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
    embed = nextcord.Embed(title=f'**Active: `{cases[4]}` **', url='https://covidnow.moh.gov.my/',description=f'\nNew cases: `{cases[1]}`\nRecovered: `{cases[3]}`\nDeath: `{deaths[1]}`\n\n👉🏻 [more detials](https://covidnow.moh.gov.my/)',color=nextcord.Color.red())
    embed.set_thumbnail(url=img[random.randint(0, 3)])
    await interaction.send('Stay home to stay safe',embed=embed)

@bot.slash_command(name='wiki',description='Search wiki articles')
async def wiki(interaction: Interaction,search):
    wiki = MediaWiki()
    async with interaction.channel.typing():
        try:
            content = wiki.summary(search, sentences=5)
        except mediawiki.DisambiguationError as error:
            embed = nextcord.Embed(title=f'Please specify your search query', description=error,color=0xffffff)
            embed.set_footer(text="Your search query matched mutliple pages.")
        except mediawiki.PageError:
            embed = nextcord.Embed(title=f'No search result', description='This page is not exist\nTry Google.',color=0xffffff)
        except Exception as error:
            raise Exception(error)
        else:
            result = wiki.page(search)
            embed = nextcord.Embed(title=result.title, url=result.url, description=content,color=0xffffff)
            try: #article no image
                embed.set_image(url=result.images[random.randint(0, 5)])
            except:
                None
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Tango_style_Wikipedia_Icon.svg/1024px-Tango_style_Wikipedia_Icon.svg.png')
    await interaction.send(embed=embed)

@bot.slash_command(name='bombserver',description='Nuke it out')
async def bombserver(interaction: Interaction):
    rick = random.randint(0,2)
    if rick == 0:
        for a in range(random.randint(7, 15)):
            truck = ['💥 ','💣 ','🤯 ','🔥 ','🚒 ','🧨 ','**Boom** ']
            content = truck[random.randint(0,6)]*random.randint(3, 7)
            await interaction.channel.send(content=content,delete_after=60)
        await interaction.channel.send("https://c.tenor.com/Wz6r_-CYusQAAAAC/nuclear-catastrophic.gif")
    elif rick ==1:
        await interaction.send('https://c.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif')
    else:
        await interaction.send('https://baike.baidu.com/item/颠覆国家政权罪/193235')
        await asyncio.sleep(2)
        await interaction.send('https://tenor.com/view/%E6%88%91%E4%BB%AC%E6%80%80%E5%BF%B5%E4%BB%96-%E6%88%91%E5%80%91%E6%87%B7%E5%BF%B5%E4%BB%96-%E6%87%B7%E5%BF%B5-%E6%80%80%E5%BF%B5-%E4%B8%BB%E5%B8%AD-gif-22955757')

@bot.slash_command(name='pl',description='lets join the vc')
async def pl(interaction: Interaction,member : nextcord.Member):
    await interaction.send(f'<#893367497389113394>  {member.mention}')

@bot.slash_command(name='clear',description='delete messages in chats')
async def clear(interaction:Interaction, amount:int=SlashOption(description='How many messages you want to clear? Max is 200.'), member:nextcord.Member=SlashOption(required=False)):
    if interaction.user.guild_permissions.manage_channels == False:
        await sendmseg(interaction.channel,2,f'**You dont have permission**')
        return
    await interaction.send(embed=nextcord.Embed(description='Clearing messages. Please wait for a while.',color=0x2f3136).set_footer(text='Please note that we cant delete message older than 20d'),ephemeral=True)
    if member == None:
        await interaction.channel.purge(limit=amount)
    else:
        async with interaction.channel.typing():
            await interaction.channel.purge(limit=amount, check=lambda m: m.author == interaction.user)
    await sendmseg(interaction.channel,1,f'**{amount} messages** were deleted')

@bot.slash_command(name='fandom',description='Search soul knight articles')
async def searchfandom(interaction: Interaction,search):
    sk_fandom = MediaWiki(url='https://soul-knight.fandom.com/api.php')
    async with interaction.channel.typing():
        try:
            content = sk_fandom.summary(search, sentences=5)
        except mediawiki.DisambiguationError as error:
            embed = nextcord.Embed(title=f'Please specify your search query', description=error,color=0x01e2b9)
            embed.set_footer(text="Your search query matched mutliple pages.")
        except mediawiki.PageError:
            embed = nextcord.Embed(title=f'No search result', description='This page is not exist\n*Push it along, gotta be strong.*.',color=0x01e2b9)
        except Exception as error:
            raise Exception(error)
        else:
            result = sk_fandom.page(search)
            embed = nextcord.Embed(title=result.title, url=result.url, description=content,color=0x01e2b9)
            embed.set_footer(text="Adapted from soul-knight.fandom.com")
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/soul-knight/images/8/8d/DrillMaster.png/revision/latest/scale-to-width-down/139?cb=20180712160915')
    me = await interaction.send(embed=embed)
    await me.add_reaction('❌')

@bot.slash_command(name='华晨宇',description='治疗三部曲')
async def huachenyu(interaction: Interaction):
    with open('./database/huahua.txt', 'r',encoding="utf8") as f:
        await interaction.send(f.read(),ephemeral=True,view=senderror(error='==instant https://www.youtube.com/watch?v=3SG9u--CZXQ'))
    from music import music
    try:
        await music.instant(bot,interaction.user,'https://www.youtube.com/watch?v=3SG9u--CZXQ')
    except:        
        # await sendmseg(interaction.channel,4,mseg='waiting for Nextcord to support slash commands in cogs...',error='==instant https://www.youtube.com/watch?v=3SG9u--CZXQ')
        None

@bot.slash_command(name='youtube',description='download media from youtube')
async def youtube(interaction: Interaction, option=SlashOption(choices=['mp3 audio','mp4 video']),* ,url):
    await interaction.response.defer(with_message=True,ephemeral=True)
    async with interaction.channel.typing():
        if option == 'mp4 video':
            music = YouTube(url).streams.filter(file_extension='mp4').first().download()
        elif option == 'mp3 audio':
            music = YouTube(url).streams.filter(file_extension='mp4',only_audio=True).first().download()
            base, ext = os.path.splitext(music)
            new_file = base + '.mp3'
            os.rename(music, new_file)
            music = new_file
    await interaction.send('Done downloading task. Remember to save.',file=nextcord.File(music),ephemeral=True)
    os.remove(music)




#QQ cogs and run the bot
# from online import keep_alive  
# keep_alive()
bot.load_extension('music')
bot.load_extension('mod')
bot.run('ODg5Mzk1MTgyNzE2NDg1NjMy.YUgnzw.3pmDMY-cL9JIgmOyslszmV5ZQeg')