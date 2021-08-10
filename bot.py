import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_slash import SlashCommand

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='zla!', help_command=None, intents=discord.Intents().all())
slash = SlashCommand(client, sync_on_cog_reload = True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)