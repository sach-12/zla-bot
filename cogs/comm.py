import discord
from discord.ext import commands


class comm(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logs = 843879097519308803


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        await self.client.get_channel(self.logs).send("Bot is online")


    @commands.command(aliases=['help'])
    async def help_command(self, ctx):
        await ctx.channel.send("I am help command")


def setup(client):
    client.add_cog(comm(client))
