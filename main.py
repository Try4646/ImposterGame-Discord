import discord
from discord.ext import commands
from game_manager import GameManager

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed to send DMs

bot = commands.Bot(command_prefix='>', intents=intents)
game_manager = GameManager(bot)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name='create', help='Create a new imposter game [0-10 chance for custom words]')
async def create_game(ctx, chance: int = None):
    await game_manager.create_game(ctx, chance)

@bot.command(name='join', help='Join an existing game')
async def join_game(ctx):
    await game_manager.join_game(ctx)

@bot.command(name='start', help='Start the game (creator only)')
async def start_game(ctx):
    await game_manager.start_game(ctx)

@bot.command(name='reroll', help='Reroll word if its bad (creator only)')
async def reroll_word(ctx):
    await game_manager.reroll_word(ctx)


@bot.command(name='end', help='End the game (creator only)')
async def end_game(ctx):
    await game_manager.end_game(ctx)

@bot.command(name='info', help='End the game (creator only)')
async def info_game(ctx):
    print("ran")
    await game_manager.info_game(ctx)

@bot.command(name='vote', help='Vote a player you suspect is the imposter (e.g. >vote @username)')
async def vote_player(ctx, player: discord.User = None):
    await game_manager.vote_player(ctx, player)


bot.run('')  #Discord-token