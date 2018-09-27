import discord
from discord.ext import commands
import asyncio
import random
import ast

async def xembed(title, desc):
    return discord.Embed(title=title, description=desc, color=0xb40a78)

class misc:
    def __init__(self, bot):
        self.bot = bot
        with open('bank.json', "r") as f:
            self.bank =  ast.literal_eval(f.read())

    @commands.command()
    async def help(self, ctx, page:int = 1):
        if page < 4:
            if page == 1:
                embed = discord.Embed(title="Basic commands", description="Use -'help 2' to se the next page", colour=0xb40a78)
                embed.add_field(name="Help", value="-help (page). help brings up this page, but you already know that")
                embed.add_field(name="roll", value="-roll (sides).  Rolls dice, randomly picking a number between 1 and the number of sides")
                embed.add_field(name="flip", value="-flip [times].  flips a coin the amount of times input")
                embed.add_field(name="kitty", value="-Kitty (question).  Kitty will answer your yes/no question!")
                embed.add_field(name="CtF", value="-ctf (value).  Converts celsius to fahrenheit")
                embed.add_field(name="FtC", value="-ftc (value). Converts fahrenheit to celsius")
                embed.add_field(name="toCM", value="-tocm (foot) (inch).  Converts feet and inches to centimetres")
                embed.add_field(name="toFoot", value="-tofoot (cm). Converts centimetres into feet and inches. Might be slightly inaccurate")
                embed.add_field(name="prime", value="prime (number). Prime factorisation of input number")
                embed.add_field(name="info", value="-info.  brings up info about the bot")
                embed.add_field(name="cat", value="-cat. sends a random picture of a cat")
                embed.add_field(name="dog", value="dog.  sends a random picture of a dog")
            elif page == 2:
                embed = discord.Embed(title="Currency and jobs", description="Use -'help 3' to se the next page", colour=0xb40a78)
                embed.add_field(name="register", value="-register. Registers a bank account. Required for most commands to work")
                embed.add_field(name="Balance, profile", value="-bal.  Checks the balance of your bank account and shows your current job")
                embed.add_field(name="work", value="-work. Your primary way of earning money. 10 minute cooldown")
                embed.add_field(name="jobs", value="-jobs.  Shows a list of all available jobs")
                embed.add_field(name="getjob", value="-getjob (job name).  Gets you the job if your power level is high enough")
                embed.add_field(name="shop", value="-shop.  Brings up the shop window")
                embed.add_field(name="buy", value="-buy (item name) (quantity).  buys an item from the shop. Item name has to be lower case")
                embed.add_field(name="inventory, inv", value="-inv.  Shows all items in your inventory")
                embed.add_field(name="use", value="-use (item) (quantity).  Uses the item and increases your power level")
            elif page == 3:
                embed = discord.Embed(title="Poker", description="This is the final page", colour=0xb40a78)
                embed.add_field(name="pHost", value="-phost (money).  Hosts a game of poker")
                embed.add_field(name="pJoin", value="-pjoin (money).  Joins hosted game of poker")
                embed.add_field(name="endpoker", value="-endpoker.  Ends ongoing game of poker")
                embed.add_field(name="pStart", value="-pstart.  Starts the hosted game of poker")
                embed.add_field(name="bump", value="-bump.  Bumps the poker embed")
                embed.add_field(name="fold", value="-fold.  Fold cards and excludes you from rest of round")
                embed.add_field(name="raise", value="-raise (amount).  Raise the bet by the amount input. Forces others to act")
                embed.add_field(name="call", value="-call.  Match the highest bet")
                embed.add_field(name="check", value="-check.  Check when you don't want to raise")
                embed.add_field(name="quit", value="-quit.  Leave the ongoing game of poker and exchange your markers.")
            await ctx.send(embed = embed)
        else:
            ctx.send("There aren't that many pages yet!")

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, *, side:int=10):
        """
        Rolls dice, randomly picking a number between 1 and the number of sides
        -Dice (sides)
        """
        await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "You rolled a {}-sided die and got {}".format(side, random.randint(1,side))))

    @commands.command()
    async def flip(self, ctx, *, arg:int=0):
        """Flips a coin
            -flip (times to flip)
        """
        if arg <= 1:
            a = random.randint(1,2)
            if a == 1:
               a = "Heads"
            else:
               a = "Tails"
            await ctx.send(embed = await xembed("{},".format(ctx.author.display_name),"The coin landed on {}".format(a)))
        else:
            heads = 0
            tails = 0
            for x in range(1, arg+1):
                a = random.randint(1,2)
                if a == 1:
                   heads +=1
                else:
                   tails +=1
            await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "The coin landed on heads {} times and tails {} times".format(heads, tails)))


    @commands.command()
    async def kitty(self, ctx,*,args):
        """Kitty will answer your yes/no question! """
        list = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "You absolute arse", "Yes", "That depends on if you want to live", "Maybe", "Pfft, no way", "Not so certain", "Error 666, not allowed to answer", "Err.. yes?", "Feed me and I'll tell you", "My very reliable sources say no", "There is no way in hell", "With a bit of luck","As an expert on these things I must say meow", "I really think so", "I really don't think so", "Why would you ask me??", "If I was Naya I would say yes but I'm not so I'll say no", "There is an 89 percent chance of it being yes", "Why not?", "Of course!", "No chance!", "Are you out of your damn mind?", "When pigs fly", "I might be able to answer your question in the next patch", "Damn straight.","To find the answer you seek you must enter the Matrix", "If you saw a snake would you poke it?", "I see you need my superior expertise, **No.**", "Hells to the YEAH!", "Why in the  nine hells?", "Full steam ahead", "Why? just WHY?", "I'm down", "Nein." ,"You're on your own to figure this out", "Positive", "I don't see why not", "Did someone say [Thunderfury, Blessed Blade of the Windseeker]?", "Never in this universe,", "I got 99 problems but your question ain't one", "As lord Satan wishes", "If Naya has banned someone within a year, yes", "Not even my creator could answer that", "The idea is bad and you have to be punished", "Sorry, not a fan", "Are you on crack or something?", "Keeanu Reaves approves :thumbsup:", "It would cause the slow withering of my soul.. if I had one"]
        await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), random.choice(list)))

    @commands.command()
    async def ctf(self, ctx, float:float):
        """Converts celsius to fahrenheit"""
        await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{} degrees celsius is {} degrees fahrenheit".format(float, float*1.8+32)))

    @commands.command()
    async def ftc(self, ctx, stuff:float):
        """Converts fahrenheit to celsius"""
        await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{} degrees fahrenheit is {} degrees celsius".format(stuff, round((stuff-32)/1.8,1))))

    @commands.command()
    async def spam(self, ctx, message, times:int):
        """Sends a message multiple times"""
        if times < 6:
            for n in range(1, times + 1):
                await ctx.send(message)

    @commands.command()
    async def tocm(self, ctx, foot:float, inch:float):
        """Converts feet and inches into centimetres """
        a = round(foot*30.48 + inch*2.54, 1)
        await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{}'{}'' is {}cm".format(foot, inch, a)))

    @commands.command()
    async def tofoot(self, ctx, m:float):
        """Converts centimetres into feet and inches"""
        a = m//30.48
        b = round((m *0.39 - a*12), 1)
        await ctx.send(embed = await xembed(ctx.author.display_name , "{}cm is approximately {}'{}''".format(m,int(a),int(b))))

    @commands.command()
    async def prime(self, ctx, x:int):
        """Prime factorisation of number """
        n = x
        a = 2
        prime = []
        while a * a <= n:
            if n % a:
                a += 1
            else:
                n //= a
                prime.append(a)
        if n > 1:
            prime.append(n)
        embed = discord.Embed(title="{},".format(ctx.author.display_name), color=0xb40a78)
        boop = str(prime)
        embed.add_field(name="prime factorisation of {}:".format(x), value=boop[1:-1])
        await ctx.send(embed = embed)

    @commands.command()
    async def info(self, ctx):
        """Information about the bot """
        embed = discord.Embed(title="KittyBot5000", description="Cutest bot you'll ever meet :3", color=0xb40a78)
        embed.add_field(name="Author", value="Nyathaleen#3995")
        embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
        embed.add_field(name="Favourite food:", value="Sushi, obviously")
        await ctx.send(embed = embed)

    @commands.command()
    async def cat(self, ctx):
        """Posts a random picture of a cat """
        cats = ["https://tinyurl.com/ycdl7uyn", "https://tinyurl.com/ycr4sndw", "https://tinyurl.com/y9ecyc9z", "https://tinyurl.com/ycfcng7m", "https://tinyurl.com/y8dhab79", "https://tinyurl.com/y8txcamq", "https://tinyurl.com/y8n7crm8", "https://tinyurl.com/yabt3vwn","https://tinyurl.com/y8ya3oq3", "https://tinyurl.com/yb48en2d", "https://tinyurl.com/ya2s4uhg", "https://tinyurl.com/y9hyerw7", "https://tinyurl.com/yb6mxo84", "https://tinyurl.com/yaamphrs", "https://tinyurl.com/yamc97d2", "https://tinyurl.com/y9ozfao7", "https://tinyurl.com/y8pld4x4", "https://tinyurl.com/y8s7o55u", "https://tinyurl.com/ybwl8adc", "https://tinyurl.com/y7pgm23x", "https://tinyurl.com/y8yxrnrl", "https://tinyurl.com/y9z5zbvf", "https://tinyurl.com/y9t5vjgu","https://tinyurl.com/ybtmgqv4", "https://tinyurl.com/ybg2bayo", "https://tinyurl.com/ycl3wygm", "https://tinyurl.com/yboyu4fm", "https://tinyurl.com/yau56888", "https://tinyurl.com/ybrqn2ku", "https://tinyurl.com/yay7ndky", "https://tinyurl.com/y7umg6qw" ]
        embed = discord.Embed(title="{},".format(ctx.author.display_name), description="Have a picture of a cat", color=0xb40a78)
        embed.set_image(url=random.choice(cats))
        await ctx.send(embed = embed)
        await ctx.send("<:awmycat:490840141812727818>")

    @commands.command(aliases=["doggo"])
    async def dog(self, ctx):
        """Posts a random picture of a dog"""
        dogs = ["https://tinyurl.com/ybc29gfa", "https://tinyurl.com/yajfx5fb", "https://tinyurl.com/yc6yluar", "https://tinyurl.com/y7emz3bw", "https://tinyurl.com/ya2lketb", "https://tinyurl.com/ybtbjdss", "https://tinyurl.com/ybsoyxud", "https://tinyurl.com/y73k57an", "https://tinyurl.com/ybr26wch", "https://tinyurl.com/y9qrghok", "https://tinyurl.com/ycutvvw6", "https://tinyurl.com/yaowqors", "https://tinyurl.com/yatgbmkv", "https://tinyurl.com/yddr5qh6", "https://tinyurl.com/y8gxs7e2", "https://tinyurl.com/ybu2mhbe", "https://tinyurl.com/ybf62f7j", "https://tinyurl.com/ybjb42j9", "https://tinyurl.com/y7f3u857", "https://tinyurl.com/ycdlwqt6", "https://tinyurl.com/ybh4kfeq", "https://tinyurl.com/yaozz8dg", "https://tinyurl.com/ybxgsp7k", "https://tinyurl.com/ycrkwj9k", "https://tinyurl.com/yc6fy7t5", "https://tinyurl.com/yc5atout", "https://tinyurl.com/y9lqjwez", "https://tinyurl.com/ycjd39pq", "https://tinyurl.com/y98pbkgz"]
        embed = discord.Embed(title="{},".format(ctx.author.display_name), description="Enjoy your doggos", color=0xb40a78)
        embed.set_image(url=random.choice(dogs))
        await ctx.send(embed = embed)

    @commands.command()
    async def slots(self, ctx, num:int = 100):
        if self.bank[ctx.message.author.id]["money"] >= num:
            wl = ""
            amount = num
            slots = ['heart', 'black_heart', 'green_heart', 'purple_heart', 'blue_heart', 'seven']
            slotsies = [random.choice(slots), random.choice(slots), random.choice(slots), random.choice(slots)]
            slotOutput = '|\t:{}:\t|\t:{}:\t|\t:{}:\t|\t:{}:\t|\n'.format(slotsies[0], slotsies[1], slotsies[2], slotsies[3])
            fuck = 0
            for n in range(len(slotsies)):
                if slotsies[n] != "seven":
                    fuck = 1
            if fuck == 0:
                wl = "win"
                amount *=2
            else:
                wl = "lose"
            if wl == "win":
                self.bank[ctx.message.author.id]["money"] += amount
            else:
                self.bank[ctx.message.author.id]["money"] -= amount
            embed = discord.Embed(title="", description ="You {} {}$".format(wl, amount), color=0xb40a78)
            embed.add_field(name="Results", value="{}".format(slotOutput))
            await ctx.send(embed = embed)
        else:
            await ctx.send("You don't have enough money mate, time to stop gambling")


async def save():
    with open('bank.json', 'w') as f:
        f.write(repr(obj.bank))


def setup(bot):
    global obj
    obj = misc(bot)
    bot.add_cog(obj)
