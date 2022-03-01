print('mod extension')
import nextcord
from nextcord.ext import commands
import asyncio
from datetime import timedelta
from main import sendmseg

class mod(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command() 
    async def kick(self,ctx, member : nextcord.Member, *, reason = None):
        if ctx.author.guild_permissions.kick_members == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        try:
            await member.kick(reason = reason)
        except nextcord.Forbidden:
            await sendmseg(ctx,2,f'**Failed to kick {member.display_name}**. No permission to kick admin')
        except Exception as error:
            await sendmseg(ctx,4,error=error)
        else:
            if reason == None:
                await sendmseg(ctx,1,f'**{member.display_name}** was kicked')
            else:
                await sendmseg(ctx,1,f'**{member.display_name}** was kicked',reason)

    @commands.command() 
    async def freeze(self,ctx,channel:nextcord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        if ctx.author.guild_permissions.manage_channels == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        try:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        except Exception as error:
            await sendmseg(ctx,4,error=error)
        else:
            sendmseg(channel,1,f'**<#{channel.id}> was freezed.** Members cant send message here now.')
        
    @commands.command() 
    async def unfreeze(self,ctx,channel:nextcord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        await sendmseg(channel,1,f'**<#{channel.id}> was unfreezed.** Members could send message freely now.')
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

    @commands.command()
    async def clear(self,ctx, member : nextcord.Member=None, amount=100):
        if ctx.author.guild_permissions.manage_channels == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        try:
            if member == None:
                await ctx.channel.purge(limit=amount)
            else:
                async with ctx.channel.typing():
                    await ctx.channel.purge(limit=amount, check=lambda m: m.author == ctx.author)
        except Exception as error:
            await sendmseg(ctx,4,f'**Failed to delete message**',error=error)
        else:
            await sendmseg(ctx,1,f'**{amount} messages** was deleted')

    @commands.command()
    async def mute(self,ctx, member: nextcord.Member,time,*, reason = None):
        if ctx.author.guild_permissions.kick_members == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        duration = int(time[0]) * time_convert[time[-1]]
        try:
            await member.edit(timeout=nextcord.utils.utcnow() + timedelta(seconds=duration))
        except Forbidden:
            await sendmseg(ctx,2,'No permission to mute moderators')
        except Exception as error:
            await sendmseg(ctx,4,error=error)
        else:
            await sendmseg(ctx,1,f'mute {member.mention} for {time}',reason)

    @commands.command()
    async def addcurseword(self,ctx, curse=None):
        if ctx.author.guild_permissions.manage_channels == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        if curse == None:
            await sendmseg(ctx,2,'**Missing curseword:** Please provide a word behind the command.')
            return
        f = open("./db/bad word.txt", "a")
        f.write(f"\n{curse}")
        await sendmseg(ctx,1,'**done**')

    

def setup(client):  
    client.add_cog(mod(client))