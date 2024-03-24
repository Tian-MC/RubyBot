import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

#========================================================================
# This is a simple Discord bot made by Tian (https://github.com/tian-mc)
#========================================================================

# Set up Discord intents
intents = discord.Intents.all()

# Load environment variables from .env file
load_dotenv()

#========================================================================
#       Make sure to make an .env file with the following content:
#               DISCORD_TOKEN: <your_discord_bot_token>
#========================================================================

# Get the Discord token from environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Raise an error if the token is not set
if TOKEN is None:
    raise ValueError('TOKEN environment variable is not set')

# Create a bot instance with specified settings | Prefix: . | Status: Online | Activity: Playing with your data!
bot = commands.Bot(command_prefix='.', intents=intents, status=discord.Status.online, activity=discord.Game('with your data!'), help_command=None)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

# Command to display help information
@bot.command()
async def help(ctx):
    # Create an embedded message with command information
    embed = discord.Embed(title='Help', description='List of commands available', color=discord.Color.blue())
    embed.add_field(name='.ping', value='Returns the latency of the bot', inline=False)
    embed.add_field(name='.clear <amount>', value='Clears the specified amount of messages', inline=False)
    embed.add_field(name='.ban <member> <reason>', value='Bans the specified member', inline=False)
    embed.add_field(name='.unban <member>', value='Unbans the specified member', inline=False)
    embed.add_field(name='.kick <member> <reason>', value='Kicks the specified member', inline=False)
    embed.add_field(name='.mute <member> <reason>', value='Mutes the specified member', inline=False)
    embed.add_field(name='.unmute <member>', value='Unmutes the specified member', inline=False)
    await ctx.send(embed=embed)

# Command to display bot latency
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')
    await ctx.send('Just kidding, Pong!')

# Command to clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = None):
    if amount is None:
        await ctx.send("Please specify the amount of messages you want to clear.")
        return
    if amount <= 0 or amount > 100:
        await ctx.send("Please specify a number between 1 and 100.")
        return

    # Create an embedded message to show the amount of messages being cleared
    embed = discord.Embed(title='Clear', description='Clearing messages', color=discord.Color.red())
    embed.add_field(name='Amount', value=amount, inline=False)
    
    await ctx.send(embed=embed)

    # Clear the specified amount of messages
    await ctx.channel.purge(limit=amount + 1)

    # Show a confirmation message and delete it after 2 seconds
    confirmation_message = await ctx.send(f'{amount} messages deleted')
    await asyncio.sleep(2)
    await confirmation_message.delete()

# Command to ban a member
@bot.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to ban.")
        return
    
    # Ban the specified member
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned')

# Command to unban a member
@bot.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def unban(ctx, *, member=None):
    if member is None:
        await ctx.send("Please specify the banned user you want to unban.")
        return
    
    # Get the list of banned users
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    # Find the banned user and unban them
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned')
            return
    
    await ctx.send("The specified user was not found among the banned users.")

# Command to kick a member
@bot.command()
async def kick(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to kick.")
        return
    
    # Kick the specified member
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked')

# Command to mute a member
@bot.command()
async def mute(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please specify the member you want to mute.")
        return
    
    # Get or create the "Muted" role
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')

        # Set permissions for the "Muted" role in all channels
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    try:
        # Add the "Muted" role to the member
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'{member} has been muted')
    except discord.Forbidden:
        await ctx.send("I don't have permission to mute members. Please check my permissions.")

# Command to unmute a member
@bot.command()
async def unmute(ctx, member: discord.Member=None):
    if member is None:
        await ctx.send("Please specify the member you want to unmute.")
        return
    
    # Get the "Muted" role
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not muted_role:
        await ctx.send("The 'Muted' role does not exist.")
        return

    try:
        # Remove the "Muted" role from the member
        await member.remove_roles(muted_role)
        await ctx.send(f'{member} has been unmuted')
    except discord.Forbidden:
        await ctx.send("I don't have permission to unmute members. Please check my permissions.")

# Run the bot with the specified token
bot.run(TOKEN)