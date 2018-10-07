import discord
from discord.ext import commands
import asyncio
import random
import ast

shopdict = { "cheese": 10, "vegetables": 30, "burger": 50, "wine" : 150, "pizza": 300, "catnip": 400, "yarn": 700, "laser pointer":1000}
shopdictbonus = { "cheese": 0, "vegetables": 0.3, "burger": 1, "wine" : 4.5, "pizza": 12, "catnip": 20, "yarn": 42, "laser pointer":70}
#Bonus increase 0.1% per item
shoplist = ["cheese", "vegetables", "burger", "wine", "pizza", "catnip", "yarn", "laser pointer"]

salary = {"unemployed":10, "plumber":30, "dishwasher":60, "hairdresser":140, "teacher":300, "engineer":660, "doctor":1400}
# 200% plus 20 per job
jobdict = {"plumber":10, "dishwasher":50, "hairdresser":250, "teacher":1000, "engineer":4000, "doctor":16000}
# 400% increase
joblist = ["plumber", "dishwasher", "hairdresser", "teacher", "engineer", "doctor"]

flav = {
"unemployed":["You clean your neighbours house and he gives you {}$", "You mow your grandpa's lawn and he pays you {}$", "You babysit your friend's niece and earn {}$", "You win a bet with your friends and they owe you {}$", "You search your grandparents' sofa and find {}$", "You win a local eating contest and win {}$", "You steal money from a homeless guy and get {}$", "You tried prostitution but did poorly and only got {}$", "You ask your mom for money and she gave you {}$", "You pretend to be homeless and the kind give you {}$", "You pull out your tooth and put it under your pillow and next morning you find {}$", "You fill in for the cashier at your father's store and earn {}$"],

"plumber":["You spend all day drinking tea and eating biscuts instead of fixing the old lady's toilet, but she enjoyed the company so she gave you {}$", "You install new urinals at a theatre and earn {}$", "You unclog five drains in one day! You get rewarded {}$", "You spend all day fixing the pipes that someone tried to tap water from, you earn a mere {}$", "You pretend like you didn't screw up someone's piping and still got {}$", "Your neighbour has problems with hot water, you fix it and he gives you {}", "You take the day off to go an adventure only to find that your princess is in another castle. Thank god you found a chest containing {}$"],

"dishwasher":["You mop the floors all day and earn {}$", "A fire started in the kitchen today! Since you put it out your boss rewards you with {}$", "You singlehandedly unload all food deliveries and earn {}$", "You hang out with your co-workers after work and win a low stakes game of poker. You win {}$", "So that gender studies degree not working out for you? Said your manager after you failed at washing dishes, which is your job. He still gave you {}$ though", "You compete with your co-workers on who can wash the most dishes in a day. You lost but still earned {}$", "You play guitar on your lunch break and you get tipped {}$!", "You use your dishwashing skills and earn an extra {}$ on your spare time", "On your way home you find a lost wallet with {}$ in it", "On a stroll through the neighbourhood you meet a couple of kids listening to hip-hop music. You challenge them to a breakdancing battle and you win {}$!"],

"hairdresser":["A celebrity comes into the salon and ask for a haircut! You earn {}$", "Someone tried to cut their own hair! You give them a proper haircut for {}$", "You get your mother a fresh haircut. She gives you {}$ for your pristine work", "A customer asked to have their hair dyed lime green. You earn {}$ and spend all day laughing at it", "Your boss rewards you {}$ for the amount of haircuts you did in one day, amazing", "You give free haircuts to homeless people and a man was so impressed with your work that he gave you {}$", "You host a movie night with your girls and they give you {}$ for all the work you put in", "You give a customer a really cool hair carving and he tips you {}$", "You win {}$ as a prize for the most colourful haircut of the month"],

"teacher":["You teach maths for moody teenagers that won't pay attention. You earn {}$", "A student challenges you on a quiz. Of course you win and get {}$", "You stand in for a sick teacher and the students have the most fun they've ever had! You earn {}$", "You teach your students about democracy but no one pays attention. You earn {}$", "The principal observes the lesson and he rewards you {}$ because of you outstanding work", "A bully stole a student's lunch money! You take it from him and keep the {}$ for yourself", "You win {}$ in a sick gangsta rap battle against your students", "A student bribes you {}$ to tell him the answers on his homework", "You teach your students about atomic orbitals and earn {}$", "You set yourself on fire in a failed chemistry experiment. Your students thought it was so cool they payed you {}$", "You watch Gattaca with your students during chemistry", "You educate senoir citizens on the subject of homosexuality. You earn {}$"],

"engineer":["You work as a mechanical engineer and create Descolé's mech. Descolé cheats you and only pays you 10% of your agreement, which is still a fair {}$.", "You work as an electrical engineer. You don't do anything useful but the people around you give you {}$ for the spectacle you created when you caught fire.", "You work as a civil engineer and construct an elaborate tower out of Jenga bricks. Unfortunately a clumsy person walked past you and knocked the whole thing down. He gives you {}$ in compensation.", "You work as an aerospace engineer and help a noob get to space in Kerbal Space Program. He pays you {}$ for your trouble.", "You work in materials science engineering for a day. You discover a new element and win a Nobel Prize for {}$.", "You work in software engineering and help develop KittyBot for a day and Naya pays you {}$ in gratitude.", "You work in bioengineering and create GMO. Despite the controversy you are paid {}$ for your work.",
 "You work in nuclear engineering and threaten the US government with a nuclear attack. They pay you a ransom of {}$ in order to prevent a nuclear attack. ~~Who am I kidding, Trump would just nuke you.~~", "Today you learned not to make fun of engineers in other departments. Earn {}$ for your daily tasks and a fresh bruise from your co-worker's spanner."],

"doctor":["A man comes in drunk out of his mind thinking you're his parent, he gives you {}$ and apologises for stealing your cat", "A patient comes in with a really bad sunburn. You treat her and earn {}$", "A man comes in with a metal tube in his ass. You take it out and earn {}$", "A patient questioned your capabilities as a doctor. You told them not to worry since you had watched a YouTube tutorial. You earned {}$", "You won {}$ in the monthly poker tournament", "A patient with demntia started asking where he was mid-sentence and then instantly left. You still got payed {}$ though", "A young man came in and asked why his medicine didn't work. Turns out he tried to drink the eardrops! You earned {}$", "Your boss rewarded you {}$ for having the most satisfied patients", "A patient came in convinced that he was jesus and had to be escorted out. He dropped his wallet which contained an entire {}$!",
 "A young girl came in trying to convince me that she was allergic to water. She payed you {}$ to tell her mother it was true"]


}

def save():
    with open('bank.json', 'w') as f:
        f.write(repr(bank))

def load():
    global bank
    with open('bank.json', "r") as f:
        bank =  ast.literal_eval(f.read())

class jobs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, ctx):
        """A way of earning money """
        load()
        id = ctx.message.author.id
        if id not in bank:
            await ctx.channel.send(embed = await xembed(ctx.author.display_name,"Get a bank account"))
        if "job" in bank[id]:
            j = bank[id]["job"]
            a = random.randint(salary[j],salary[j]*2)
            bank[id]["money"] += a
            await ctx.channel.send(embed = await xembed(ctx.author.display_name, random.choice(flav[bank[id]["job"]]).format(a)))
            save()
        else:
            bank[id]["job"] = "unemployed"

    @commands.command()
    async def register(self, ctx):
        """Register a bank account """
        load()
        id = ctx.message.author.id
        if id not in bank:
            bank[id] = {}
            bank[id]["money"] = 100
            bank[id]["inv"] = {}
            bank[id]["job"] = "unemployed"
            bank[id]["power"] = 0
            await ctx.send(embed = await xembed(ctx.author.display_name, "Thank you for registering a bank account"))
        else:
            await ctx.send(embed = await xembed(ctx.author.display_name, "You already have an account registered"))
        save()

    @commands.command(aliases=["balance","bal"])
    async def profile(self, ctx):
        """Check the balance of your bank account and your current job"""
        load()
        id = ctx.message.author.id
        if id in bank:
            await ctx.send(embed = await xembed(ctx.author.display_name,"You have {}$ on your bank account and your current job is {}".format(bank[id]["money"], bank[id]["job"])))
        else:
            await ctx.send(embed = await xembed(ctx.author.display_name, "You do not have a bank account"))


    @commands.command()
    async def shop(self, ctx):
        """Opens the shop window"""
        embed = discord.Embed(title="Shop:", description="Use -buy' and the item name to buy" ,color=0xb40a78)
        for n in shoplist:
            embed.add_field(name="{}".format(n), value="{}$".format(shopdict[n]))
        await ctx.send(embed = embed)

    @commands.command()
    async def buy(self, ctx, arg, num:int = 1):
        """Buys an item from the shop"""
        load()
        arg = arg.lower()
        id = ctx.message.author.id
        if arg.lower() in shopdict:
            if bank[id]["money"] < shopdict[arg]*num:
                embed = await xembed(ctx.author.display_name, "You don't have enough money for this item", )
                ctx.send(embed = embed)
            else:
                if arg not in bank[id]["inv"]:
                    bank[id]["inv"][arg] = 0
                bank[id]["inv"][arg] += 1*num
                bank[id]["money"] -= shopdict[arg]*num
                await ctx.send(embed = await xembed(ctx.author.display_name, "Thank you {} for purchasing {} {}".format(ctx.author.display_name, num, arg)))
        else:
            await ctx.send(embed = await xembed(ctx.author.display_name, "Sorry, our shop does not sell {}".format(arg)))
        save()

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx):
        """opens your inventory"""
        load()
        id = ctx.message.author.id
        embed = discord.Embed(title=ctx.author.display_name, description="Your inventory:",color=0xb40a78 )
        for n in shoplist:
            if n in bank[id]["inv"]:
                embed.add_field(name="{}".format(n), value="{}".format(bank[id]["inv"][n]))

        await ctx.send(embed = embed)


    @commands.command()
    async def use(self, ctx, item, num:int = 1):
        """Uses item in your inventory"""
        load()
        item = item.lower()
        id = ctx.message.author.id
        if item in bank[id]["inv"]:
            if bank[id]["inv"][item] >= 1*num:
                bank[id]["inv"][item] -= 1*num
                if "power" not in bank[id]:
                    bank[id]["power"] = 0
                bank[id]["power"] += (shopdict[item]*num)/10 + shopdict[item]/5
                await ctx.send(embed = await xembed(ctx.message.author.display_name, "You used {} {} and your power level has increased to {}".format(num, item, bank[id]["power"])))
        else:
            await ctx.send(embed = await xembed(ctx.message.author.display_name, "You don't own any of those"))
            save()

    @commands.command()
    async def jobs(self, ctx):
        """lists available jobs"""
        load()
        id = ctx.message.author.id
        embed = discord.Embed(title=ctx.author.display_name, description="Here are the possible jobs", color=0xb40a78)
        for n in joblist:
            embed.add_field(name="{}".format(n), value="Power level needed {}".format(jobdict[n]))
        await ctx.send(embed = embed)
        await ctx.send("Your current power level: {}".format(bank[id]["power"]))




    @commands.command()
    async def getjob(self, ctx, job):
        """get a job"""
        load()
        id = ctx.message.author.id
        if "job" not in bank[id]:
            bank[id]["job"] = "unemployed"
        if job in jobdict:
            if jobdict[job] <= bank[id]["power"]:
                bank[id]["job"] = job
                await ctx.send(embed = await xembed(ctx.message.author.display_name, "Congratulations you're hired! Your new job is: {}".format(job)))
            else:
                await ctx.send(embed = await xembed(ctx.message.author.display_name,"{} requires {} power and you only have {}!".format(job, jobdict[job], bank[id]["power"])))
        else:
            await ctx.send(embed = await xembed(ctx.message.author.display_name,"{} is not an available job".format(job)))
        save()


    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = float(str(error).split('You are on cooldown. Try again in ')[1].rstrip('s'))
            min = time//60
            sec = (time%60)
            await ctx.send(embed = await xembed(ctx.author.display_name, "You've been spending too much time at work! Come back in {} minutes and {} seconds".format(int(min), int(sec))))





async def xembed(title, desc):
    return discord.Embed(title=title, description=desc, color=0xb40a78)

def setup(bot):
    bot.add_cog(jobs(bot))
