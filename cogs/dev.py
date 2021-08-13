import discord
from discord.ext import commands
import subprocess
import sys


class dev(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['pull'])
    async def git_pull_command(self, ctx):
        if ctx.author.id == 723377619420184668:
            sys.stdout.flush()
            p = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
            for line in iter(p.stdout.readline, ''):
                if not line:
                    break
                await ctx.channel.send(str(line.rstrip(), 'utf-8', 'ignore'))
            sys.stdout.flush()
        else:
            await ctx.channel.send("This is a developer-only command. You can't use it")


    @commands.command(aliases=['restart'])
    async def restart_command(self, ctx):
        if ctx.author.id == 723377619420184668:
            await self.git_pull_command(ctx)
            p = subprocess.Popen(['python3', 'start.py'])
            sys.exit(0)
        else:
            await ctx.channel.send("This is a developer-only command. You can't use it")


def setup(client):
    client.add_cog(dev(client))