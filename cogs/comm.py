import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime
from cogs.func import func


class comm(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['help'])
    async def help_command(self, ctx):
        await ctx.channel.send("I am help command")


    @commands.command(aliases=['online'])
    async def online_command(self, ctx):
        await ctx.channel.trigger_typing()
        url = 'https://laartcc.org/'
        res = requests.get(url)
        if(res.status_code == 200):
            soup = BeautifulSoup(res.content, "html.parser")
            online = soup.find("div", class_="list-group")
            controller_list = online.find_all("a")
            emb = discord.Embed(title="Controllers online in Los Angeles ARTCC", timestamp=datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30))
            if(len(controller_list) == 0):
                emb.description = "No controllers online"
                emb.color = discord.Color.red()
                await ctx.channel.send(embed=emb)
                return
            else:
                emb.color = discord.Color.green()
            for controller in controller_list:
                info = controller.text.strip().split('\n')
                position = info[0]
                name = info[1].split('/')[0].strip()
                profile_link = controller["href"]
                cid = profile_link.split('/')[-1]
                online_time = controller["data-title"].strip().split('–')[1].strip()
                emb.add_field(name=f"{position} - {name} ({cid})",value=f"{online_time} [Controller Profile]({profile_link})", inline=False)
            await ctx.channel.send(embed=emb)
        else:
            emb = discord.Embed(title="Something's wrong", description="Try again after a while", timestamp=datetime.datetime.now(), color=discord.Color.red())
            await ctx.channel.send(embed=emb)


    @commands.command(aliases = ['controller'])
    async def controller_command(self, ctx, query:str = ''):
        await ctx.channel.trigger_typing()
        help_embed = discord.Embed(title="LA ARTCC Controller Information", color=discord.Color.blue())
        help_embed.add_field(name="zla!controller [initials or CID]", value="Returns information about a specific ZLA controller given the query")
        if(query == ''):
            await ctx.channel.send(embed=help_embed)
            return
        url = f"https://laartcc.org/controller/{query}"
        profile = func.profileFromCid(func(self.client), url)
        if(profile == 404):
            ret = func.getUrl(func(self.client), query)
            if(ret == 404):
                await ctx.channel.send(content="Controller not found on the roster", embed=help_embed)
                return
            else:
                profile = func.profileFromCid(func(self.client), ret)
                if(profile == 404):
                    embx = discord.Embed(title="Something's wrong", description="Try again after a while", color=discord.Color.red())
                    await ctx.channel.send(embed=embx)
                    return
        name = f"{profile[0]} - {profile[6]}"
        rating = profile[1]
        month = profile[4]
        month_hours = profile[2]
        total_hours = profile[3]
        img_src = profile[5]
        profile_url = profile[7]
        online_status = profile[8]
        emb = discord.Embed(title=name, description=rating, url=profile_url, color=0xff10f0)
        emb.set_thumbnail(url=img_src)
        emb.add_field(name=f"Hours - {month}", value=month_hours)
        emb.add_field(name="Hours - Total", value=total_hours)
        emb.set_footer(text=online_status)
        await ctx.channel.send(embed=emb)
        
        
def setup(client):
    client.add_cog(comm(client))
