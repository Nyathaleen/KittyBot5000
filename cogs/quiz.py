import discord
from discord.ext import commands
import asyncio
import random
import ast
class quiz:
    def __init__(self, bot):
        self.bot = bot
        self.quez = ""
        self.questions = ["Vad är bäst?","Who is the creator of KittyBot5000?", "How many cats does the creator of the bot have?", "If you find a waffle on the ground would you:","När äter Liam våfflor?"]
        self.options ={"Vad är bäst?":["hundar", "katter", "Liam", "chocklad"],"Who is the creator of KittyBot5000?":["Starwort", "Uncappingprism", "Liam", "Nyathaleen"],"How many cats does the creator of the bot have?":["1","2","3","4"],
         "If you find a waffle on the ground would you:":["Not eat it", "Eat it if it has maple syrup", "Eat it if it's clean", "Eat it"], "När äter Liam våfflor?":["Annandag våffel", "Julafton", "Varje dag", "På våffeldagen hemma hos mormor klockan tre"],}
        self.answer = {"Vad är bäst?":"chocklad","Who is the creator of KittyBot5000?":"Nyathaleen","How many cats does the creator of the bot have?":"3", "If you find a waffle on the ground would you:":"Eat it if it has maple syrup","När äter Liam våfflor?":"På våffeldagen hemma hos mormor klockan tre"}

    @commands.command()
    async def quiz(self, ctx):
        self.quez = random.choice(self.questions)
        self.quizid = ctx.message.author.id
        embed = discord.Embed(title="Question", description=self.quez, colour=0xb40a78)
        embed.add_field(name="option 1", value="{}".format(self.options[self.quez][0]))
        embed.add_field(name="option 2", value="{}".format(self.options[self.quez][1]))
        embed.add_field(name="option 3", value="{}".format(self.options[self.quez][2]))
        embed.add_field(name="option 4", value="{}".format(self.options[self.quez][3]))
        await ctx.send(embed = embed)
        await ctx.send("Use -guess and the option number")

    @commands.command()
    async def guess(self, ctx, opt:int = 0):
        opt -=1
        if self.quez != "":
            if self.quizid == ctx.message.author.id:
                if self.options[self.quez][opt] == self.answer[self.quez]:
                    await ctx.send("{} was the correct answer!".format(self.answer[self.quez]))
                    self.quez = ""
                else:
                    await ctx.send("{} is not the correct answer!".format(self.options[self.quez][opt]))
                    self.quez = ""
            else:
                await ctx.send("You're not the one who asked the question")
        else:
            await ctx.send("Use -quiz to get a question first")

def setup(bot):
    global obj
    obj = quiz(bot)
    bot.add_cog(obj)
