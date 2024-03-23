import discord
from discord.ext import commands

intents = discord.Intents.all()

TOKEN = 'MTIwNTIxMTgzNjc0NDQ3MDU4OQ.GbRwgw.FS5EehVWSxdGNDPdL_Vq5Z2Zs12YnzxQGNfyHk'

bot = commands.Bot(command_prefix='.', intents=intents, status=discord.Status.dnd, activity=discord.Game('with your data!'), help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} è pronto!')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='List of commands available', color=discord.Color.blue())
    embed.add_field(name='.ping', value='Returns the latency of the bot', inline=False)
    embed.add_field(name='.clear <amount>', value='Clears the specified amount of messages', inline=False)
    embed.add_field(name='.ban <member> <reason>', value='Bans the specified member', inline=False)
    embed.add_field(name='.unban <member>', value='Unbans the specified member', inline=False)
    embed.add_field(name='.kick <member> <reason>', value='Kicks the specified member', inline=False)
    embed.add_field(name='.mute <member> <reason>', value='Mutes the specified member', inline=False)
    embed.add_field(name='.unmute <member>', value='Unmutes the specified member', inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')
    await ctx.send('Just kidding, Pong!')

@bot.command()
async def clear(ctx, amount: int):
    embed = discord.Embed(title='Clear', description='Clearing messages', color=discord.Color.red())
    embed.add_field(name='Amount', value=amount, inline=False)
    await ctx.send(embed=embed)
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'{amount} *deleted messages*', delete_after=5)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned')
            return
        
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked')

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = ctx.guild.get_role(820521183674447058)
    await member.add_roles(muted_role, reason=reason)



bot.run(TOKEN)