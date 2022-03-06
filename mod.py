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
            await sendmseg(ctx,2,f'**Failed to kick {member.mention}**. No permission to kick admin')
        except Exception as error:
            await sendmseg(ctx,4,error,'Failed to kick')
        else:
            if reason == None:
                await sendmseg(ctx,1,f'**{member.mention}** was kicked')
            else:
                await sendmseg(ctx,1,f'**{member.mention}** was kicked',reason)

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
            await sendmseg(ctx,4,error,'Failed to freeze the channel')
        else:
            sendmseg(channel,1,f'**{ctx.author.mention} freeze <#{channel.id}>. ** Members cant send message here now.')
        
    @commands.command() 
    async def unfreeze(self,ctx,channel:nextcord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        await sendmseg(channel,1,f'**<#{channel.id}> was unfreezed.** Members could send message freely now.')
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

    @commands.command()
    async def clear(self,ctx, amount=10 ,member : nextcord.Member=None):
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
            await sendmseg(ctx,4,error,'Failed to delete message')
        else:
            await sendmseg(ctx,1,f'**{amount} messages** was deleted')

    @commands.command(aliases=['diam'])
    async def mute(self,ctx, member: nextcord.Member,time=None,*, reason = None):
        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        if ctx.author.guild_permissions.kick_members == False:
            await sendmseg(ctx,2,f'**You dont have permission**')
            return
        try:
            duration = int(time[0]) * time_convert[time[-1]]
        except (ValueError, KeyError,TypeError):
            await sendmseg(ctx,2,f'Please input the **duration** to mute the member','To use this command, follow this:  `==mute` `@member` `time` `reason`\n\n**Example:**\n`==mute` `@tests` `2d` `staff disresepct`\n> I want to mute <@886833929145974794> for 2 days because he didnt respect mod\n\n**Time:**\n10 second: `10s`\n20 minutes: `20m`\n3 hours: `3h`\n4 days: `4d`')
            return
        try:
            await member.edit(timeout=nextcord.utils.utcnow() + timedelta(seconds=duration))
        except nextcord.Forbidden:
            await sendmseg(ctx,2,'No permission to mute moderators')
        except Exception as error:
            await sendmseg(ctx,4,error,'Failed to mute')
        else:
            await sendmseg(ctx,1,f'mute {member.mention} for {time}',reason)

    

def setup(client):  
    client.add_cog(mod(client))