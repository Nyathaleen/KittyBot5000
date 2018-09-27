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

    global bank
    with open('bank.json', "r") as f:
          bank =  ast.literal_eval(f.read())

    @commands.command()
    async def phost(self, ctx, monies:int = 100):
        """host game of poker"""
        global pokergame
        global players
        global puser
        pokergame = {}
        pokergame["users"] = {}
        pokergame["pot"] = 0
        players = []
        puser = []
        id = ctx.message.author.id
        if monies >= 100:
            if id in bank:
                if monies > bank[id]["money"]:
                    await ctx.send("You can't afford to participate")
                else:
                    players.append(id)
                    puser.append(id)
                    pokergame["users"][id] = {}
                    pokergame["users"][id]["ucards"] = []
                    pokergame["users"][id]["status"] = ""
                    pokergame["users"][id]["markers"] = monies*4
                    bank[id]["money"] -= monies
                    await ctx.send("You pay {}$ and get {} markers".format(monies, monies*4))
                    pokergame["users"][id]["turn"] = "yes"
                    pokergame["users"][id]["bet"] = 0
                    pokergame["carderino"] = 0
                    pokergame["users"][id]["check"] = 0
                    pokergame["users"][id]["hand"] = {}
                    pokergame["globalbet"] = 0
                    await ctx.send("Game starting! use -pjoin to join")
                    global pmessage
                    pmessage = "Game starting"
                    global pturn
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
            if id in bank:
                if monies > bank[id]["money"]:
                    await ctx.send("You can't afford to participate")
                else:
                    players.append(id)
                    puser.append(id)
                    pokergame["users"][id] = {}
                    pokergame["users"][id]["ucards"] = []
                    pokergame["users"][id]["status"] = ""
                    pokergame["users"][id]["markers"] = monies*4
                    bank[id]["money"] -= monies
                    await ctx.send("You pay {}$ and get {} markers".format(monies, monies*4))
                    pokergame["users"][id]["turn"] = "no"
                    pokergame["users"][id]["bet"] = 0
                    pokergame["users"][id]["check"] = 0
                    pokergame["users"][id]["hand"] = {}
                    await save()
                    await ctx.send("{} has joined the poker game, use -pstart when ready to start".format(ctx.author.display_name))
            else:
                await ctx.send("You don't own a bank account!")
        else:
            await ctx.send("You need to pay at least 100$ to participate")

    @commands.command()
    async def endpoker(self, ctx):
        """end ongoing poker game"""
        global pokergame
        global players
        global puser
        if ctx.message.author.id in pokergame["users"]:
            pokergame = {}
            pokergame["users"] = {}
            pokergame["pot"] = 0
            players = []
            puser = []
            global pmessage
            pmessage ="The poker game has been ended manually"
        else:
            await ctx.send("You're not a part of the poker game you can't end it!")

    @commands.command()
    async def bump(self, ctx):
        """bump poker embed"""
        global mes
        global mes4
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(pokergame["globalbet"]))
        for z in players:
            embed.add_field(name="{}".format(bot.get_user(z)), value="Markers: {}  Bet: {}".format(pokergame["users"][z]["markers"], pokergame["users"][z]["bet"]))
        if pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{}   {}   {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2] ))
        elif pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3]))
        elif pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(pmessage))
        mes = await ctx.send(embed = embed)
        mes4 = await ctx.send("Hi")
        await ctx.message.delete()


    @commands.command()
    async def pstart(self, ctx):
        """starts pokergame"""
        global mes
        global mes4
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(pokergame["globalbet"]))
        for z in players:
            embed.add_field(name="{}".format(bot.get_user(z)), value="Markers: {}  Bet: {}".format(pokergame["users"][z]["markers"], pokergame["users"][z]["bet"]))
        if pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{}   {}   {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2] ))
        elif pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3]))
        elif pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{}   {}   {}  {}  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(pmessage))
        mes = await ctx.send(embed = embed)
        mes4 = await ctx.send("Hi")
        await startpoker(ctx)

    @commands.command()
    async def fold(self, ctx):
        """fold cards and excludes you from rest of round"""
        global pturn
        global pmessage
        id = ctx.message.author.id
        if pokergame["users"][id]["turn"] == "yes":
            pokergame["users"][id]["status"] = "fold"
            puser.remove(id)
            pmessage = "{} has folded".format(ctx.message.author.display_name)
            await nextturn(ctx, ctx.message.author.id)
        else:
            await ctx.send("It's not your turn!")
        await updatemsg(ctx)
        await ctx.message.delete()


    @commands.command(name='raise')
    async def rais(self, ctx, num:int):
        """raise bet and force others to call"""
        global pturn
        global pmessage
        id = ctx.message.author.id
        if pokergame["users"][id]["turn"] == "yes":
            dif = pokergame["globalbet"] - pokergame["users"][id]["bet"]
            if num + dif < pokergame["users"][id]["markers"]:
                pokergame["users"][id]["bet"] += num + dif
                if pokergame["globalbet"] < pokergame["users"][id]["bet"]:
                    pokergame["globalbet"] = pokergame["users"][id]["bet"]
                pokergame["users"][id]["markers"] -= num + dif
                pokergame["pot"] += num + dif
                pmessage = "{} raised by {}. Everyone needs to match {}".format(ctx.message.author.display_name, num, pokergame["globalbet"])
                await updatemsg(ctx)
                await nextturn(ctx, ctx.message.author.id)
            else:
                pmessage = "You can't afford that!"
                await updatemsg(ctx)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    @commands.command()
    async def quit(self, ctx):
        """Leave game and exchange markers"""
        id = ctx.message.author.id
        if id in pokergame["users"]:
            global pturn
            global pmessage
            global players
            global puser
            players.remove(id)
            puser.remove(id)
            a = pokergame["users"][id]["markers"]
            bank[id]["money"] += round(a/4)
            await ctx.send("{} has left the game! They exchanged their markers for {}$".format(ctx.message.author, round(a/4)))
            del pokergame["users"][id]
            await save()
        else:
            await ctx.send("You're not in the game")

    @commands.command()
    async def check(self, ctx):
        """check when done for turn"""
        global pturn
        global pmessage
        id = ctx.message.author.id
        if pokergame["users"][id]["turn"] == "yes":
            if pokergame["users"][id]["bet"] < pokergame["globalbet"]:
                pmessage = "You can't check before calling"
                await updatemsg(ctx)
            else:
                pokergame["users"][id]["check"] = 1
                pmessage = "{} has checked".format(ctx.message.author.display_name)
                await nextturn(ctx, ctx.message.author.id)
                await updatemsg(ctx)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    @commands.command()
    async def call(self, ctx):
        """match the highest bet"""
        global pturn
        global pmessage
        id = ctx.message.author.id
        if pokergame["users"][id]["turn"] == "yes":
            difference = pokergame["globalbet"] - pokergame["users"][id]["bet"]
            pokergame["users"][id]["bet"] += difference
            pokergame["pot"] += difference
            pokergame["users"][id]["markers"] -= difference
            if pokergame["globalbet"] < pokergame["users"][id]["bet"]:
                pokergame["globalbet"] = pokergame["users"][id]["bet"]
            pmessage ="{} calls!".format(ctx.message.author.display_name)
            await updatemsg(ctx)
            await nextturn(ctx, ctx.message.author.id)
        else:
            await ctx.send("It's not your turn!")
        await ctx.message.delete()

    async def nextturn(self, ctx, arg):
        """Switches turn to someone else and looks if everyone has checked. Also reveals communitycards"""
        pokergame["users"][arg]["turn"] = "no"
        a  = 0
        global mes4
        global pmessage
        for b in range(len(puser)):
            if not pokergame["users"][puser[b]]["status"] == "fold":
                if pokergame["users"][puser[b]]["bet"] < pokergame["globalbet"]:
                    a = 1
                    c = b
        if a == 1:
            pokergame["users"][puser[c]]["turn"] = "yes"
            a = 0
            return await mes4.edit(content = "It's {}'s turn. use -fold, -check, -raise or -call ".format(self.bot.get_user(puser[c])))
            await updatemsg(ctx)
        else:
            checkval = 0
            for z in range(len(puser)):
                if pokergame["users"][puser[z]]["check"] == 0 and pokergame["carderino"] < 3:
                    pokergame["users"][puser[z]]["turn"] = "yes"
                    checkval = 1
                    if checkval > 0:
                        return await mes4.edit(content = "Waiting for {} to re-raise, fold or check".format(self.bot.get_user(puser[z])))
                        await updatemsg(ctx)
                        break
        if checkval == 0:
            if pokergame["carderino"] == 0:
                pokergame["carderino"] +=1
                await flop(ctx)
                await ctx.send("Flop comes down")
                for z in range(len(puser)):
                    pokergame["users"][puser[z]]["check"] = 0
            elif pokergame["carderino"] == 1:
                pokergame["carderino"] +=1
                await turn(ctx)
                await ctx.send("Turn comes down")
                for z in range(len(puser)):
                    pokergame["users"][puser[z]]["check"] = 0
            elif pokergame["carderino"] == 2:
                pokergame["carderino"] +=1
                await river(ctx)
                await ctx.send("River comes down")
                for z in range(len(puser)):
                    pokergame["users"][puser[z]]["check"] = 0
            elif pokergame["carderino"] >= 3:
                await reveal(ctx)
        folderino = 0
        for k in puser:
            if pokergame["users"][k]["status"] == "fold":
                folderino += 1
        if len(puser) - folderino == 1:
            await reveal(ctx)

    async def flop(self, ctx):
        """reveal first three communitycards"""
        pokergame["users"][puser[0]]["turn"] = "yes"
        return await mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(puser[0])))
        await updatemsg(ctx)
    async def turn(self, ctx):
        """reveal fourth communitycard"""
        pokergame["users"][puser[0]]["turn"] = "yes"
        return await mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(puser[0])))
        await updatemsg(ctx)
    async def river(self, ctx):
        """reveal final communitycard"""
        pokergame["users"][puser[0]]["turn"] = "yes"
        return await mes4.edit(content = "It's {}'s turn!".format(self.bot.get_user(puser[0])))
        await updatemsg(ctx)

    async def reveal(self, ctx):
        """calculates the values of everyone's hands"""
        await countc()
        await straight()
        await flush()
        await pair()
        await ctx.send("On the table is {},  {},  {},  {},  and {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
        for z in puser:
            pokergame["users"][z]["result2"] = 0
            await ctx.send("{} had {} and {}".format(self.bot.get_user(z), pokergame["users"][z]["ucards"][0],pokergame["users"][z]["ucards"][1] ))
            if pokergame["users"][z]["hand"]["flush"] == 1 and pokergame["users"][z]["hand"]["straight"] == 1:
                pokergame["users"][z]["result"] = 9
            elif pokergame["users"][z]["hand"]["FoaK"] == 1:
                pokergame["users"][z]["result"] = 8
            elif pokergame["users"][z]["hand"]["pair"] == 1 and pokergame["users"][z]["hand"]["ToaK"] == 1:
                pokergame["users"][z]["result"] = 7
            elif pokergame["users"][z]["hand"]["flush"] == 1:
                pokergame["users"][z]["result"] = 6
            elif pokergame["users"][z]["hand"]["straight"] == 1:
                pokergame["users"][z]["result"] = 5
            elif pokergame["users"][z]["hand"]["ToaK"] == 1:
                pokergame["users"][z]["result"] = 4
            elif pokergame["users"][z]["hand"]["pair"] == 2:
                pokergame["users"][z]["result"] = 3
            elif pokergame["users"][z]["hand"]["pair"] == 1:
                pokergame["users"][z]["result"] = 2
            else:
                pokergame["users"][z]["result"] = 1
            for bk in pokergame["users"][z]["hand"]["card"]:
                pokergame["users"][z]["result2"] += bk
        await pokerwin(ctx)
        await killoff(ctx)
        await pokerend(ctx)

    async def pokerend(self, ctx):
        """ends the round and checks if there is a winner"""
        global puser
        global pokergame
        global players
        pokergame["users"][players[0]]["turn"] = "yes"
        pokergame["carderino"] = 0
        for z in players:
            pokergame["users"][z]["ucards"] = []
            pokergame["users"][z]["status"] = ""
            pokergame["users"][z]["bet"] = 0
            pokergame["users"][z]["check"] = 0
            pokergame["users"][z]["hand"] = {}
        puser = players[:]
        if len(players) <= 1:
            await ctx.send("{} is the only person left standing and has won! They exchange their markers for {}$".format(self.bot.get_user(players[0]), round(pokergame["users"][players[0]]["markers"]/3)))
            wa = pokergame["users"][players[0]]["markers"]
            bank[players[0]]["money"] += round(wa/3)
            pokergame = {}
            players = []
            puser = []
            pokergame["users"] = {}
            pokergame["pot"] = 0
            await save()
        else:
            await ctx.send("Next round starting...")
            await startpoker(ctx)

    async def killoff(self, ctx):
        """removes players with too few markers"""
        global players
        for z in players:
            if pokergame["users"][z]["markers"] < 20:
                players.remove(z)
                await ctx.send("{} doesn't have enough markers to keep on playing!".format(self.bot.get_user(z)))

    async def pokerwin(self, ctx):
        """checks which hand is the highest"""
        a = [pokergame["users"][puser[0]]["result"], puser[0], pokergame["users"][puser[0]]["result2"]]
        for z in puser:
            if pokergame["users"][z]["result"] > a[0]:
                a = [pokergame["users"][z]["result"], z, pokergame["users"][z]["result2"]]
            elif pokergame["users"][z]["result"] == a[0]:
                if pokergame["users"][z]["result2"] > a[2]:
                    a = [pokergame["users"][z]["result"], z, pokergame["users"][z]["result2"]]
        await ctx.send("{} has won the round and got {} markers".format(self.bot.get_user(a[1]), pokergame["pot"]))
        pokergame["users"][a[1]]["markers"] += pokergame["pot"]
        pokergame["pot"] = 0


    async def countc(self, ctx):
        """calculates each card's value"""
        for z in puser:
            pokergame["users"][z]["hand"]["pair"] = 0
            pokergame["users"][z]["hand"]["straight"] = 0
            pokergame["users"][z]["hand"]["flush"] = 0
            pokergame["users"][z]["result"] = 0
            bleh = pokergame["users"][z]["ucards"] + pokergame["table"]
            pokergame["users"][z]["hand"]["card"] = []
            pokergame["users"][z]["hand"]["suit"] = []
            for n in range(0,7):
                card,of,suit = bleh[n].split(" ")
                for k in cardnums:
                    if card == k:
                        card = cardnumsdict[k]
                for k in suits:
                    if suit == k:
                        suit = suitsdict[k]
                pokergame["users"][z]["hand"]["card"].append(card)
                pokergame["users"][z]["hand"]["suit"].append(suit)

    async def pair(self, ctx):
        """looks for pairs in hand"""
        for z in puser:
            pokergame["users"][z]["hand"]["pair"] = 0
            pokergame["users"][z]["hand"]["ToaK"] = 0
            pokergame["users"][z]["hand"]["FoaK"] = 0
            paircards = pokergame["users"][z]["hand"]["card"][:]
            for a in paircards:
                x = pokergame["users"][z]["hand"]["card"].count(a)
                paircards.remove(a)
                if x == 4:
                    pokergame["users"][z]["hand"]["FoaK"] = 1
                elif x == 3:
                    pokergame["users"][z]["hand"]["ToaK"] = 1
                elif x == 2 and pokergame["users"][z]["hand"]["pair"] == 1:
                    pokergame["users"][z]["hand"]["pair"] = 2
                elif x == 2:
                    pokergame["users"][z]["hand"]["pair"] = 1

    async def straight(self, ctx):
        """checks for straight"""
        for z in puser:
            pokergame["users"][z]["hand"]["straight"] = 0
            pokergame["users"][z]["hand"]["card"].sort
            if pokergame["users"][z]["hand"]["card"][6] == 14:
                pokergame["users"][z]["hand"]["card"].append(1)
            pokergame["users"][z]["hand"]["card"].sort
            for a in range(1,7):
                if pokergame["users"][z]["hand"]["card"][a-1] + 1 == pokergame["users"][z]["hand"]["card"][a]:
                    if pokergame["users"][z]["hand"]["card"][a] + 1 == pokergame["users"][z]["hand"]["card"][a+1]:
                        if pokergame["users"][z]["hand"]["card"][a+1] + 1 == pokergame["users"][z]["hand"]["card"][a+2]:
                            if pokergame["users"][z]["hand"]["card"][a+2] + 1 == pokergame["users"][z]["hand"]["card"][a+3]:
                                if pokergame["users"][z]["hand"]["card"][a+3] + 1 == pokergame["users"][z]["hand"]["card"][a+4]:
                                    pokergame["users"][z]["hand"]["straight"] = 1
    async def flush(self, ctx):
        """checks for flush"""
        for z in puser:
            pokergame["users"][z]["hand"]["flush"] = 0
            for a in pokergame["users"][z]["hand"]["suit"]:
                x = pokergame["users"][z]["hand"]["suit"].count(a)
                if x >= 5:
                    pokergame["users"][z]["hand"]["flush"] = 1

    async def updatemsg(self, ctx):
        """updates poker embed"""
        global mes
        global mes2
        global mes3
        global mes4
        embed = discord.Embed(title="Poker", color=0xb40a78)
        embed.add_field(name="Pot", value="{}".format(pokergame["pot"]))
        embed.add_field(name="Current bet", value="{}".format(pokergame["globalbet"]))
        for z in players:
            embed.add_field(name="{}".format(self.bot.get_user(z)), value="Markers: {}  Bet: {}".format(pokergame["users"][z]["markers"], pokergame["users"][z]["bet"]))
        if pokergame["carderino"] == 1:
            embed.add_field(name="Community cards", value="{},   {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2] ))
        elif pokergame["carderino"] == 2:
            embed.add_field(name="Community cards", value="{},   {},   {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3]))
        elif pokergame["carderino"] == 3:
            embed.add_field(name="Community cards", value="{},   {},   {},  {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
        embed.add_field(name="Response", value="{}".format(pmessage))
        return await mes.edit(embed = embed)

    async def startpoker(self, ctx):
        """deals cards and resets bets and pot"""
        pokergame["cards"] = []
        pokergame["table"] = []
        pokergame["globalbet"] = 0
        for a in cardnums:
            for b in suits:
                pokergame["cards"].append("{} of {}".format(a,b))
        for n in range(1,6):
            c = random.choice(pokergame["cards"])
            pokergame["table"].append(c)
            pokergame["cards"].remove(c)
        for n in pokergame["users"]:
            for x in range(1,3):
                c = random.choice(pokergame["cards"])
                pokergame["cards"].remove(c)
                pokergame["users"][n]["ucards"].append(c)
        for n in players:
            a = n
            await self.bot.get_user(n).send("You have {} and {}".format(pokergame["users"][a]["ucards"][0],pokergame["users"][a]["ucards"][1]))
        for i in puser:
            pokergame["pot"] +=20
            pokergame["users"][i]["markers"] -=20
        await ctx.send("20 Markers from every participant has been put in the pot")
        global mes4
        return await mes4.edit(content = "It's {}'s turn. use -fold, -raise or -call ".format(self.bot.get_user(puser[0])))
        await updatemsg(ctx)

async def save():
    with open('bank.json', 'w') as f:
        f.write(repr(bank))


def setup(bot):
    bot.add_cog(poker(bot))
