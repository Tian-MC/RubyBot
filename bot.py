import discord
from discord.ext import commands

intents = discord.Intents.all()

TOKEN = 'MTIwNTIxMTgzNjc0NDQ3MDU4OQ.GmpJ6P.fC2fhapSYs8mDlXZIe2AGMT0JeYgG_pd9Xz1_I'

bot = commands.Bot(command_prefix='.', intents=intents, status=discord.Status.dnd, activity=discord.Game('with your data!'))

@bot.event
async def on_ready():
    print(f'{bot.user} è pronto!')

@bot.command()
async def saluta(ctx):
    await ctx.send(f'Ciao {ctx.author.mention}!')

bot.run(TOKEN)