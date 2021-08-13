import discord
from discord.ext import commands


class events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.logs = 843879097519308803


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        await self.client.get_channel(self.logs).send("Bot is online")


def setup(client):
    client.add_cog(events(client))