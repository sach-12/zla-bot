import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord_slash import SlashCommand
import asyncio

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='zla!', help_command=None, intents=discord.Intents().all())
slash = SlashCommand(client, sync_on_cog_reload = True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.command(aliases=['reload'])
async def cog_reload(ctx, extenstion:str):
    if(ctx.author.id == 723377619420184668):
        ext = f"cogs.{extenstion}"
        try:
            client.unload_extension(ext)
            await client.get_channel(843879097519308803).send(f"{ext} unloaded")
            await asyncio.sleep(2)
            client.load_extension(ext)
            await client.get_channel(843879097519308803).send(f"{ext} unloaded")
            await ctx.channel.send("Cog reload succesful")
        except Exception as e:
            await ctx.channel.send(e)

client.run(TOKEN)