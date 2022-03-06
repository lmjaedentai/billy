print('music extension')
import asyncio
import nextcord
import youtube_dl
from nextcord.ext import commands
from pytube import YouTube, exceptions
from main import sendmseg, ping

ytdl_format_options = {'format': 'bestaudio/best','outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s','restrictfilenames': True,'noplaylist': True,'nocheckcertificate': True,'ignoreerrors': False,'logtostderr': False,'default_search': 'auto','source_address': '0.0.0.0'}
ffmpeg_options = {'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

queue = []
loop = False

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        # return cls(nextcord.FFmpegPCMAudio(filename,executable='./database/ffmpeg.exe', **ffmpeg_options), data=data)
        return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['music','i','m'])
    async def instant(self,ctx,url:str):
        await ctx.message.delete()
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await sendplayer(self,ctx,"Now Playing",player)

    @commands.command(aliases=['p'])
    async def play(self,ctx):
        await ctx.message.delete()
        global queue, loop
        if not queue: #queue is empty
            await sendmseg(ctx,2,'Nothing in your queue! Use `?add` to add a song!')
            return

        async with ctx.typing(): #play music
            player = await YTDLSource.from_url(queue[0], loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            if loop:
                queue.append(queue[0])
            del(queue[0])
        await sendplayer(self,ctx,"Now Playing",player)

    #QQ basic music command
    @commands.command(aliases=['loop','loops','l'])
    async def toggleloop(self,ctx):
        global loop
        if loop == False:
            await sendmseg(ctx,1,'Loop is turn `on`')
            loop = True
        else:
            await sendmseg(ctx,1,'Loop is turn `off`')
            loop = False

    @commands.command(aliases=['left','stop'])
    async def leave(self,ctx):
        if ctx.voice_client is None:
            return await sendmseg(ctx,2,"You didnt join any voice channel")
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['unpause'])
    async def resume(self,ctx):
        ctx.voice_client.resume()
        await sendmseg(ctx,1,'**Resume** your music')

    @commands.command(aliases=['s'])
    async def pause(self,ctx):
        ctx.voice_client.pause()
        await ctx.message.delete()
        await sendmseg(ctx,1,'**Paused**. Use `==resume` to unpause.')

    @commands.command(aliases=['v'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await sendmseg(ctx,2,"Not connected to a voice channel.")
        try:
            ctx.voice_client.source.volume = volume / 100 
        except Exception as error: 
            await sendmseg(ctx,4,error)
        else:
            await sendmseg(ctx,1,f"Changed volume to {volume}%")

    @commands.command(aliases=['a'])
    async def add(self,ctx, url):
        await ctx.message.delete()
        global queue
        try:
            title = YouTube(url).title 
        except exceptions.RegexMatchError:
            return await sendmseg(ctx,2,'**Invalid url.** We only supported [Youtube](https://youtube.com) videos')
        else: 
            queue.append(url)
            await sendmseg(ctx,1,f'{ctx.author.mention} add **[{title}]({url})** to queue!')

    @commands.command(aliases=['r'])
    async def remove(self,ctx,number):
        global queue
        try:
            del(queue[int(number)])
            await ctx.send(f'Your queue is now `{queue}!`')
        except:
            await sendmseg(ctx,2,'Your queue is either **empty** or the index is **out of range**')

    @commands.command(aliases=['queue','q'])
    async def sendqueue(self,ctx):
        global queue
        content = ''
        async with ctx.typing():
            if not queue: #queue is empty
                content = '**Queue is empty.**\n\nUse `==add` `url` to add some songs'
            else:
                for i in range(len(queue)): 
                    content += f'`{i+1}.` [{YouTube(queue[i]).title }]({queue[i]})\n'
            embed=nextcord.Embed(description=content, color=0x2f3136).set_author(name=f"{ctx.author.display_name}'s Queue",icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


    #QQ error handling
    @instant.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
                try:
                    await ctx.voice_client.resume()
                    await ctx.voice_client.is_playing()
                except:
                    pass
            else:
                try:
                    await ctx.voice_client.move_to(ctx.author.voice.channel)
                except:
                    await sendmseg(ctx,2,"You are not connected to a voice channel.")
                    # raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()



#QQ UI player
async def sendplayer(self,ctx,status,player):  #system use this
    embed=nextcord.Embed(description=f"[{player.title}] ({player.data['webpage_url']})", color=0x2f3136)
    embed.set_thumbnail(url=player.data["thumbnail"])
    embed.set_author(name=status,icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed,view=sendcontrol(ctx)) 

class sendcontrol(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx # You can use `self.ctx` anywhere in the class, like self.ctx.author
    
    @nextcord.ui.button(label='Play / Pause', style=nextcord.ButtonStyle.success)
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.ctx.voice_client.is_playing:
            await music.pause(self,self.ctx)
        else:
            await music.play(self,self.ctx)
    
    @nextcord.ui.button(label='Loop', style=nextcord.ButtonStyle.primary)
    async def loop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await music.toggleloop(self,self.ctx)

    @nextcord.ui.button(label='Leave', style=nextcord.ButtonStyle.danger)
    async def add(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await music.leave(self,self.ctx)

    @nextcord.ui.button(label='Queue', style=nextcord.ButtonStyle.grey)
    async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await music.sendqueue(self,self.ctx)


def setup(client):  
    client.add_cog(music(client))