import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.all()

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    raise ValueError('TOKEN environment variable is not set')

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
async def clear(ctx, amount: int = None):
    import asyncio
    if amount is None:
        await ctx.send("Please specify the amount of messages you want to clear.")
        return
    if amount <= 0 or amount > 100:
        await ctx.send("Please specify a number between 1 and 100.")
        return

    embed = discord.Embed(title='Clear', description='Clearing messages', color=discord.Color.red())
    embed.add_field(name='Amount', value=amount, inline=False)
    
    await ctx.send(embed=embed)

    await ctx.channel.purge(limit=amount + 1)

    confirmation_message = await ctx.send(f'{amount} messages deleted')
    await asyncio.sleep(2)
    await confirmation_message.delete()


@bot.command()
async def ban(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to ban.")
        return
    
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned')


@bot.command()
async def unban(ctx, *, member=None):
    if member is None:
        await ctx.send("Please specify the banned user you want to unban.")
        return
    
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned')
            return
    
    await ctx.send("The specified user was not found among the banned users.")

        
@bot.command()
async def kick(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to kick.")
        return
    
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked')

@bot.command()
async def mute(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to mute.")
        return
    
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    try:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'{member} has been muted')
    except discord.Forbidden:
        await ctx.send("I don't have permission to mute members. Please check my permissions.")
        
bot.run(TOKEN)