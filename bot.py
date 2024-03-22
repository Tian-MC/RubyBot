import discord
from discord.ext import commands


intent = discord.Intents.default()
intent.typing = False
intent.presences = False
intent.members = True

TOKEN = 'MTIwNTIxMTgzNjc0NDQ3MDU4OQ.GmpJ6P.fC2fhapSYs8mDlXZIe2AGMT0JeYgG_pd9Xz1_I'

bot = commands.Bot(command_prefix='!', intents=intent, status=discord.Status.dnd, activity=discord.Game('with your data!'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')



bot.run(TOKEN)
