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


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        string = f"Something's wrong, I can feel it\n{str(error)}"
        await self.client.get_channel(self.logs).send(f"{string}\n{ctx.author.mention} invoked this error in {ctx.channel.mention}")


def setup(client):
    client.add_cog(events(client))