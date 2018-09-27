import discord
from discord.ext import commands
import asyncio
import random
import ast

suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
suitsdict = {"Diamonds":1, "Hearts":2, "Spades":3, "Clubs":4}
cardnums = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
cardnumsdict= {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Jack":11, "Queen":12, "King":13, "Ace":14}

class poker:
    def __init__(self, bot):
        self.bot = bot
        with open('bank.json', "r") as f:
            self.bank =  ast.literal_eval(f.read())


    @commands.command()
    async def phost(self, ctx, monies:int = 100):
        """host game of poker"""
        self.pokergame = {}
        self.pokergame["users"] = {}
        self.pokergame["pot"] = 0
        self.players = []
        self.puser = []
        id = ctx.message.author.id
        if monies >= 100:
            if id in self.bank:
                if monies > self.bank[id]["money"]:
                    await ctx.send("You can't afford to participate")
                else:
                    self.players.append(id)
                    self.puser.append(id)
                    self.pokergame["users"][id] = {}
                    self.pokergame["users"][id]["ucards"] = []
                    self.pokergame["users"][id]["status"] = ""
                    self.pokergame["users"][id]["markers"] = monies*4
                    self.bank[id]["money"] -= monies
                    await ctx.send("You pay {}$ and get {} markers".format(monies, monies*4))
                    self.pokergame["users"][id]["turn"] = "yes"
                    self.pokergame["users"][id]["bet"] = 0
                    self.pokergame["carderino"] = 0
                    self.pokergame["users"][id]["check"] = 0
                    self.pokergame["users"][id]["hand"] = {}
                    self.pokergame["globalbet"] = 0
                    await ctx.send("Game starting! use -pjoin to join")
                    self.pmessage = "Game starting"
                    await save()
            else:
                await ctx.send("You don't own a bank account!")
        else:
            await ctx.send("You need to pay at least 100$ to participate")


    @commands.command()
    async def pjoin(self, ctx, monies:int = 100):
        """join hosted game of poker"""
        id = ctx.message.author.id
        if monies >= 100:
            if id in self.bank:
                if monies > self.bank[id]["money"]:
                    await ctx.send("You can't afford to participate")
                else:
                    self.players.append(id)
                    self.puser.append(id)
                    self.pokergame["users"][id] = {}
                    self.pokergame["users"][id]["ucards"] = []
                    self.pokergame["users"][id]["status"] = ""
                    self.pokergame["users"][id]["markers"] = monies*4
                    self.bank[id]["money"] -= monies
                    await ctx.send("You pay {}$ and get {} markers".format(monies, monies*4))
                    self.pokergame["users"][id]["turn"] = "no"
                    self.pokergame["users"][id]["bet"] = 0
                    self.pokergame["users"][id]["check"] = 0
                    self.pokergame["users"][id]["hand"] = {}
                    await save()
                    await ctx.send("{} has joined the poker game, use -pstart when ready to start".format(ctx.author.display_name))
            else:
                await ctx.send("You don't own a bank account!")
        else:
            await ctx.send("You need to pay at least 100$ to participate")

    @commands.command()
    async def endpoker(self, ctx):
        """end ongoing poker game"""
        if ctx.message.author.id in self.pokergame["users"]:
            self.pokergame = {}
            self.pokergame["users"] = {}
            self.pokergame["pot"] = 0
            self.players = []
            self.puser = []
            self.pmessage ="The poker game has been ended manually"
        else:
            await ctx.send("You're not a part of the poker game you can't end it!")

    @commands.command()
    async def bump(self, ctx):
        """bump poker embed"""
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(self.pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(self.pokergame["globalbet"]))
        for z in self.players:
            embed.add_field(name="{}".format(self.bot.get_user(z)), value="Markers: {}  Bet: {}".format(self.pokergame["users"][z]["markers"], self.pokergame["users"][z]["bet"]))
        if self.pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{}   {}   {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2] ))
        elif self.pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3]))
        elif self.pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3], self.pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(self.pmessage))
        self.mes = await ctx.send(embed = embed)
        self.mes4 = await ctx.send("Hi")
        await ctx.message.delete()


    @commands.command()
    async def pstart(self, ctx):
        """starts pokergame"""
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(self.pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(self.pokergame["globalbet"]))
        for z in self.players:
            embed.add_field(name="{}".format(self.bot.get_user(z)), value="Markers: {}  Bet: {}".format(self.pokergame["users"][z]["markers"], self.pokergame["users"][z]["bet"]))
        if self.pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{}   {}   {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2] ))
        elif self.pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3]))
        elif self.pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3], self.pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(self.pmessage))
        self.mes = await ctx.send(embed = embed)
        self.mes4 = await ctx.send("Hi")
        await self.startpoker(ctx)

    @commands.command()
    async def fold(self, ctx):
        """fold cards and excludes you from rest of round"""
        id = ctx.message.author.id
        if self.pokergame["users"][id]["turn"] == "yes":
            self.pokergame["users"][id]["status"] = "fold"
            self.puser.remove(id)
            self.pmessage = "{} has folded".format(ctx.message.author.display_name)
            await self.nextturn(ctx, ctx.message.author.id)
        else:
            await ctx.send("It's not your turn!")
        await self.updatemsg(ctx)
        await ctx.message.delete()


    @commands.command(name='raise')
    async def rais(self, ctx, num:int):
        """raise bet and force others to call"""
        id = ctx.message.author.id
        if self.pokergame["users"][id]["turn"] == "yes":
            dif = self.pokergame["globalbet"] - self.pokergame["users"][id]["bet"]
            if num + dif < self.pokergame["users"][id]["markers"]:
                self.pokergame["users"][id]["bet"] += num + dif
                if self.pokergame["globalbet"] < self.pokergame["users"][id]["bet"]:
                    self.pokergame["globalbet"] = self.pokergame["users"][id]["bet"]
                self.pokergame["users"][id]["markers"] -= num + dif
                self.pokergame["pot"] += num + dif
                self.pmessage = "{} raised by {}. Everyone needs to match {}".format(ctx.message.author.display_name, num, self.pokergame["globalbet"])
                await self.updatemsg(ctx)
                await self.nextturn(ctx, ctx.message.author.id)
            else:
                self.pmessage = "You can't afford that!"
                await self.updatemsg(ctx)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    @commands.command()
    async def quit(self, ctx):
        """Leave game and exchange markers"""
        id = ctx.message.author.id
        if id in self.pokergame["users"]:
            self.players.remove(id)
            self.puser.remove(id)
            a = self.pokergame["users"][id]["markers"]
            self.bank[id]["money"] += round(a/4)
            await ctx.send("{} has left the game! They exchanged their markers for {}$".format(ctx.message.author, round(a/4)))
            del self.pokergame["users"][id]
            await save()
        else:
            await ctx.send("You're not in the game")

    @commands.command()
    async def check(self, ctx):
        """check when done for turn"""
        id = ctx.message.author.id
        if self.pokergame["users"][id]["turn"] == "yes":
            if self.pokergame["users"][id]["bet"] < self.pokergame["globalbet"]:
                self.pmessage = "You can't check before calling"
                await self.updatemsg(ctx)
            else:
                self.pokergame["users"][id]["check"] = 1
                self.pmessage = "{} has checked".format(ctx.message.author.display_name)
                await self.nextturn(ctx, ctx.message.author.id)
                await self.updatemsg(ctx)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    @commands.command()
    async def call(self, ctx):
        """match the highest bet"""
        id = ctx.message.author.id
        if self.pokergame["users"][id]["turn"] == "yes":
            difference = self.pokergame["globalbet"] - self.pokergame["users"][id]["bet"]
            self.pokergame["users"][id]["bet"] += difference
            self.pokergame["pot"] += difference
            self.pokergame["users"][id]["markers"] -= difference
            if self.pokergame["globalbet"] < self.pokergame["users"][id]["bet"]:
                self.pokergame["globalbet"] = self.pokergame["users"][id]["bet"]
            self.pmessage ="{} calls!".format(ctx.message.author.display_name)
            await self.updatemsg(ctx)
            await self.nextturn(ctx, ctx.message.author.id)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    async def nextturn(self, ctx, arg):
        """Switches turn to someone else and looks if everyone has checked. Also reveals communitycards"""
        self.pokergame["users"][arg]["turn"] = "no"
        a  = 0
        for b in range(len(self.puser)):
            if not self.pokergame["users"][self.puser[b]]["status"] == "fold":
                if self.pokergame["users"][self.puser[b]]["bet"] < self.pokergame["globalbet"]:
                    a = 1
                    c = b
        if a == 1:
            self.pokergame["users"][self.puser[c]]["turn"] = "yes"
            a = 0
            return await self.mes4.edit(content = "It's {}'s turn. use -fold, -check, -raise or -call ".format(self.bot.get_user(self.puser[c])))
            await self.updatemsg(ctx)
        else:
            checkval = 0
            for z in range(len(self.puser)):
                if self.pokergame["users"][self.puser[z]]["check"] == 0 and self.pokergame["carderino"] < 3:
                    self.pokergame["users"][self.puser[z]]["turn"] = "yes"
                    checkval = 1
                    if checkval > 0:
                        return await self.mes4.edit(content = "Waiting for {} to re-raise, fold or check".format(self.bot.get_user(self.puser[z])))
                        await self.updatemsg(ctx)
                        break
        if checkval == 0:
            if self.pokergame["carderino"] == 0:
                self.pokergame["carderino"] +=1
                await self.flop(ctx)
                await ctx.send("Flop comes down")
                for z in range(len(self.puser)):
                    self.pokergame["users"][self.puser[z]]["check"] = 0
            elif self.pokergame["carderino"] == 1:
                self.pokergame["carderino"] +=1
                await self.turn(ctx)
                await ctx.send("Turn comes down")
                for z in range(len(self.puser)):
                    self.pokergame["users"][self.puser[z]]["check"] = 0
            elif self.pokergame["carderino"] == 2:
                self.pokergame["carderino"] +=1
                await self.river(ctx)
                await ctx.send("River comes down")
                for z in range(len(self.puser)):
                    self.pokergame["users"][self.puser[z]]["check"] = 0
            elif self.pokergame["carderino"] >= 3:
                await self.reveal(ctx)
        folderino = 0
        for k in self.puser:
            if self.pokergame["users"][k]["status"] == "fold":
                folderino += 1
        if len(self.puser) - folderino == 1:
            await self.reveal(ctx)

    async def flop(self, ctx):
        """reveal first three communitycards"""
        self.pokergame["users"][self.puser[0]]["turn"] = "yes"
        return await self.mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(self.puser[0])))
        await self.updatemsg(ctx)
    async def turn(self, ctx):
        """reveal fourth communitycard"""
        self.pokergame["users"][self.puser[0]]["turn"] = "yes"
        return await self.mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(self.puser[0])))
        await self.updatemsg(ctx)
    async def river(self, ctx):
        """reveal final communitycard"""
        self.pokergame["users"][self.puser[0]]["turn"] = "yes"
        return await self.mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(self.puser[0])))
        await self.updatemsg(ctx)

    async def reveal(self, ctx):
        """calculates the values of everyone's hands"""
        await self.countc(ctx)
        await self.straight(ctx)
        await self.flush(ctx)
        await self.pair(ctx)
        await ctx.send("On the table is {},  {},  {},  {},  and {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3], self.pokergame["table"][4]))
        for z in self.puser:
            self.pokergame["users"][z]["result2"] = 0
            await ctx.send("{} had {} and {}".format(self.bot.get_user(z), self.pokergame["users"][z]["ucards"][0],self.pokergame["users"][z]["ucards"][1] ))
            if self.pokergame["users"][z]["hand"]["flush"] == 1 and self.pokergame["users"][z]["hand"]["straight"] == 1:
                self.pokergame["users"][z]["result"] = 9
            elif self.pokergame["users"][z]["hand"]["FoaK"] == 1:
                self.pokergame["users"][z]["result"] = 8
            elif self.pokergame["users"][z]["hand"]["pair"] == 1 and self.pokergame["users"][z]["hand"]["ToaK"] == 1:
                self.pokergame["users"][z]["result"] = 7
            elif self.pokergame["users"][z]["hand"]["flush"] == 1:
                self.pokergame["users"][z]["result"] = 6
            elif self.pokergame["users"][z]["hand"]["straight"] == 1:
                self.pokergame["users"][z]["result"] = 5
            elif self.pokergame["users"][z]["hand"]["ToaK"] == 1:
                self.pokergame["users"][z]["result"] = 4
            elif self.pokergame["users"][z]["hand"]["pair"] == 2:
                self.pokergame["users"][z]["result"] = 3
            elif self.pokergame["users"][z]["hand"]["pair"] == 1:
                self.pokergame["users"][z]["result"] = 2
            else:
                self.pokergame["users"][z]["result"] = 1
            for bk in self.pokergame["users"][z]["hand"]["card"]:
                self.pokergame["users"][z]["result2"] += bk
        await self.pokerwin(ctx)
        await self.killoff(ctx)
        await self.pokerend(ctx)

    async def pokerend(self, ctx):
        """ends the round and checks if there is a winner"""
        self.pokergame["users"][self.players[0]]["turn"] = "yes"
        self.pokergame["carderino"] = 0
        for z in self.players:
            self.pokergame["users"][z]["ucards"] = []
            self.pokergame["users"][z]["status"] = ""
            self.pokergame["users"][z]["bet"] = 0
            self.pokergame["users"][z]["check"] = 0
            self.pokergame["users"][z]["hand"] = {}
        self.puser = self.players[:]
        if len(self.players) <= 1:
            await ctx.send("{} is the only person left standing and has won! They exchange their markers for {}$".format(self.bot.get_user(self.players[0]), round(self.pokergame["users"][self.players[0]]["markers"]/3)))
            wa = self.pokergame["users"][self.players[0]]["markers"]
            self.bank[self.players[0]]["money"] += round(wa/3)
            self.pokergame = {}
            self.players = []
            self.puser = []
            self.pokergame["users"] = {}
            self.pokergame["pot"] = 0
            await save()
        else:
            await ctx.send("Next round starting...")
            await self.startpoker(ctx)

    async def killoff(self, ctx):
        """removes self.players with too few markers"""
        for z in self.players:
            if self.pokergame["users"][z]["markers"] < 20:
                self.players.remove(z)
                await ctx.send("{} doesn't have enough markers to keep on playing!".format(self.bot.get_user(z)))

    async def pokerwin(self, ctx):
        """checks which hand is the highest"""
        a = [self.pokergame["users"][self.puser[0]]["result"], self.puser[0], self.pokergame["users"][self.puser[0]]["result2"]]
        for z in self.puser:
            if self.pokergame["users"][z]["result"] > a[0]:
                a = [self.pokergame["users"][z]["result"], z, self.pokergame["users"][z]["result2"]]
            elif self.pokergame["users"][z]["result"] == a[0]:
                if self.pokergame["users"][z]["result2"] > a[2]:
                    a = [self.pokergame["users"][z]["result"], z, self.pokergame["users"][z]["result2"]]
        await ctx.send("{} has won the round and got {} markers".format(self.bot.get_user(a[1]), self.pokergame["pot"]))
        self.pokergame["users"][a[1]]["markers"] += self.pokergame["pot"]
        self.pokergame["pot"] = 0


    async def countc(self, ctx):
        """calculates each card's value"""
        for z in self.puser:
            self.pokergame["users"][z]["hand"]["pair"] = 0
            self.pokergame["users"][z]["hand"]["straight"] = 0
            self.pokergame["users"][z]["hand"]["flush"] = 0
            self.pokergame["users"][z]["result"] = 0
            bleh = self.pokergame["users"][z]["ucards"] + self.pokergame["table"]
            self.pokergame["users"][z]["hand"]["card"] = []
            self.pokergame["users"][z]["hand"]["suit"] = []
            for n in range(0,7):
                card,of,suit = bleh[n].split(" ")
                for k in cardnums:
                    if card == k:
                        card = cardnumsdict[k]
                for k in suits:
                    if suit == k:
                        suit = suitsdict[k]
                self.pokergame["users"][z]["hand"]["card"].append(card)
                self.pokergame["users"][z]["hand"]["suit"].append(suit)

    async def pair(self, ctx):
        """looks for pairs in hand"""
        for z in self.puser:
            self.pokergame["users"][z]["hand"]["pair"] = 0
            self.pokergame["users"][z]["hand"]["ToaK"] = 0
            self.pokergame["users"][z]["hand"]["FoaK"] = 0
            paircards = self.pokergame["users"][z]["hand"]["card"][:]
            for a in paircards:
                x = self.pokergame["users"][z]["hand"]["card"].count(a)
                paircards.remove(a)
                if x == 4:
                    self.pokergame["users"][z]["hand"]["FoaK"] = 1
                elif x == 3:
                    self.pokergame["users"][z]["hand"]["ToaK"] = 1
                elif x == 2 and self.pokergame["users"][z]["hand"]["pair"] == 1:
                    self.pokergame["users"][z]["hand"]["pair"] = 2
                elif x == 2:
                    self.pokergame["users"][z]["hand"]["pair"] = 1

    async def straight(self, ctx):
        """checks for straight"""
        for z in self.puser:
            self.pokergame["users"][z]["hand"]["straight"] = 0
            self.pokergame["users"][z]["hand"]["card"].sort
            if self.pokergame["users"][z]["hand"]["card"][6] == 14:
                self.pokergame["users"][z]["hand"]["card"].append(1)
            self.pokergame["users"][z]["hand"]["card"].sort
            for a in range(1,7):
                if self.pokergame["users"][z]["hand"]["card"][a-1] + 1 == self.pokergame["users"][z]["hand"]["card"][a]:
                    if self.pokergame["users"][z]["hand"]["card"][a] + 1 == self.pokergame["users"][z]["hand"]["card"][a+1]:
                        if self.pokergame["users"][z]["hand"]["card"][a+1] + 1 == self.pokergame["users"][z]["hand"]["card"][a+2]:
                            if self.pokergame["users"][z]["hand"]["card"][a+2] + 1 == self.pokergame["users"][z]["hand"]["card"][a+3]:
                                if self.pokergame["users"][z]["hand"]["card"][a+3] + 1 == self.pokergame["users"][z]["hand"]["card"][a+4]:
                                    self.pokergame["users"][z]["hand"]["straight"] = 1
    async def flush(self, ctx):
        """checks for flush"""
        for z in self.puser:
            self.pokergame["users"][z]["hand"]["flush"] = 0
            for a in self.pokergame["users"][z]["hand"]["suit"]:
                x = self.pokergame["users"][z]["hand"]["suit"].count(a)
                if x >= 5:
                    self.pokergame["users"][z]["hand"]["flush"] = 1

    async def updatemsg(self, ctx):
        """updates poker embed"""
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(self.pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(self.pokergame["globalbet"]))
        for z in self.players:
            embed.add_field(name="{}".format(self.bot.get_user(z)), value="Markers: {}  Bet: {}".format(self.pokergame["users"][z]["markers"], self.pokergame["users"][z]["bet"]))
        if self.pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{},   {} and  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2] ))
        elif self.pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{},   {},   {} and  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3]))
        elif self.pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{},   {},   {},  {} and  {}".format(self.pokergame["table"][0], self.pokergame["table"][1], self.pokergame["table"][2], self.pokergame["table"][3], self.pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(self.pmessage))
        return await self.mes.edit(embed = embed)

    async def startpoker(self, ctx):
        """deals cards and resets bets and pot"""
        self.pokergame["cards"] = []
        self.pokergame["table"] = []
        self.pokergame["globalbet"] = 0
        for a in cardnums:
            for b in suits:
                self.pokergame["cards"].append("{} of {}".format(a,b))
        for n in range(1,6):
            c = random.choice(self.pokergame["cards"])
            self.pokergame["table"].append(c)
            self.pokergame["cards"].remove(c)
        for n in self.pokergame["users"]:
            for x in range(1,3):
                c = random.choice(self.pokergame["cards"])
                self.pokergame["cards"].remove(c)
                self.pokergame["users"][n]["ucards"].append(c)
        for n in self.players:
            a = n
            await self.bot.get_user(n).send("You have {} and {}".format(self.pokergame["users"][a]["ucards"][0],self.pokergame["users"][a]["ucards"][1]))
        for i in self.puser:
            self.pokergame["pot"] +=20
            self.pokergame["users"][i]["markers"] -=20
        await ctx.send("20 Markers from every participant has been put in the pot")
        return await self.mes4.edit(content = "It's {}'s turn. use -fold, -raise or -call ".format(self.bot.get_user(self.puser[0])))
        await self.updatemsg(ctx)

async def save():
    with open('bank.json', 'w') as f:
        f.write(repr(obj.bank))


def setup(bot):
    global obj
    obj = poker(bot)
    bot.add_cog(obj)
