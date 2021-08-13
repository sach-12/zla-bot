import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


class func(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ratings = {
            "S1": "Student 1",
            "S2": "Student 2",
            "S3": "Student 3",
            "C1": "Controller 1",
            "C3": "Controller 3",
            "I1": "Instructor 1",
            "I3": "Instructor 3"
        }


    def profileFromCid(self, url:str):
        res = requests.get(url=url)
        if(res.status_code == 200):
            soup = BeautifulSoup(res.content, "html.parser")
            name = soup.find("h3", class_="mb-0 text-truncated").text.strip()
            qual = soup.find("p", class_="lead").text.strip()
            rating = self.getRating(qual=qual)
            totals = soup.find_all("td", class_='"totals"')
            month_hours = totals[1].text.strip()
            if(month_hours == ""):
                month_hours = "0:00"
            total_hours = totals[-1].text.strip()
            month_table = soup.find("table", class_="table table-striped table-bordered table-sm stats")
            month = month_table.findChild("th").text.strip().capitalize()
            img = soup.find("img", class_="img-fluid rounded img-thumbnail")
            img_src = img["src"]
            cid = url.split('/')[-1]
            return name, rating, month_hours, total_hours, month, img_src, cid, url
        else:
            return 404


    def getRating(self, qual:str):
        qual_list = qual.split('/')
        if(len(qual_list) == 1):
            if(qual_list[0].strip() in self.ratings):
                return f"{qual_list[0].strip()} - {self.ratings[qual_list[0].strip()]}"
            else:
                return qual_list[0].strip()
        else:
            if(qual_list[1].strip() in self.ratings):
                return f"{qual_list[0].strip()} / {qual_list[1].strip()} - {self.ratings[qual_list[1].strip()]}"
            else:
                return qual_list[1].strip()


    def getUrl(self, initials:str):
        url = "https://laartcc.org/roster"
        res = requests.get(url=url)
        soup = BeautifulSoup(res.content, "html.parser")
        roster = soup.find(id='roster')
        controller_list = roster.findChildren("tr")
        for controller in controller_list:
            try:
                c = (controller.text.strip().split('\n')[-2])
                if(c == initials.upper()):
                    profile = controller.find("a")
                    return profile["href"]
            except:
                continue
        return 404


def setup(client):
    client.add_cog(func(client))