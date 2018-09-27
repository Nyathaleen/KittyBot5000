import discord
from discord.ext import commands
import asyncio
import random
import ast



bot = commands.Bot(command_prefix = "-", case_insensitive=True)
bot.remove_command("help")
@bot.event
async def on_ready():
    global bank
    with open('bank.json', "r") as f:
          bank =  ast.literal_eval(f.read())
    await bot.change_presence(activity=discord.Game(name="with Naya"))
    print("Bot is online and connected to Discord")

async def xembed(title, desc):
    return discord.Embed(title=title, description=desc, color=0xb40a78)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print("{} sent '{}' in {}, {} ".format(message.author, message.content, message.channel, message.guild))

@bot.event
async def on_typing(channel, user, when):
    print(user, "is typing.." )

@bot.command()
async def help(ctx, page:int = 1):
    if page < 4:
        if page == 1:
            helpvar = 1
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
            helpmes = await ctx.send(embed = embed)
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
            helpmes = await ctx.send(embed = embed)
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
            helpmes = await ctx.send(embed = embed)
    else:
        ctx.send("There aren't tha many pages yet!")


@bot.command(aliases=["dice"])
async def roll(ctx, *, side:int=10):
    """
    Rolls dice, randomly picking a number between 1 and the number of sides
    -Dice (sides)
    """
    await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "You rolled a {}-sided die and got {}".format(side, random.randint(1,side))))

@bot.command()
async def flip(ctx, *, arg:int=0):
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


@bot.command()
async def kitty(ctx,*,args):
    """Kitty will answer your yes/no question! """
    list = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", "Most likely", "You absolute arse", "Yes", "That depends on if you want to live", "Maybe", "Pfft, no way", "Not so certain", "Error 666, not allowed to answer", "Err.. yes?", "Feed me and I'll tell you", "My very reliable sources say no", "There is no way in hell", "With a bit of luck","As an expert on these things I must say meow", "I really think so", "I really don't think so", "Why would you ask me??", "If I was Naya I would say yes but I'm not so I'll say no", "There is an 89 percent chance of it being yes", "Why not?", "Of course!", "No chance!", "Are you out of your damn mind?", "When pigs fly", "I might be able to answer your question in the next patch", "Damn straight.","To find the answer you seek you must enter the Matrix", "If you saw a snake would you poke it?", "I see you need my superior expertise, **No.**", "Hells to the YEAH!", "Why in the  nine hells?", "Full steam ahead", "Why? just WHY?", "I'm down", "Nein." ,"You're on your own to figure this out", "Positive", "I don't see why not", "Did someone say [Thunderfury, Blessed Blade of the Windseeker]?", "Never in this universe,", "I got 99 problems but your question ain't one", "As lord Satan wishes", "If Naya has banned someone within a year, yes", "Not even my creator could answer that", "The idea is bad and you have to be punished", "Sorry, not a fan", "Are you on crack or something?", "Keeanu Reaves approves :thumbsup:", "It would cause the slow withering of my soul.. if I had one"]
    await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), random.choice(list)))

@bot.command()
async def ctf(ctx, float:float):
    """Converts celsius to fahrenheit"""
    await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{} degrees celsius is {} degrees fahrenheit".format(float, float*1.8+32)))

@bot.command()
async def ftc(ctx, stuff:float):
    """Converts fahrenheit to celsius"""
    await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{} degrees fahrenheit is {} degrees celsius".format(stuff, round((stuff-32)/1.8,1))))

@bot.command()
async def spam(ctx, message, times:int):
    """Sends a message multiple times"""
    if times < 6:
        for n in range(1, times + 1):
            await ctx.send(message)

@bot.command()
async def tocm(ctx, foot:float, inch:float):
    """Converts feet and inches into centimetres """
    a = round(foot*30.48 + inch*2.54, 1)
    await ctx.send(embed = await xembed("{},".format(ctx.author.display_name), "{}'{}'' is {}cm".format(foot, inch, a)))

@bot.command()
async def tofoot(ctx, m:float):
    """Converts centimetres into feet and inches"""
    a = m//30.48
    b = round((m *0.39 - a*12), 1)
    await ctx.send(embed = await xembed(ctx.author.display_name , "{}cm is {}'{}''".format(m,int(a),int(b))))

@bot.command()
async def prime(ctx, x:int):
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

@bot.command()
async def info(ctx):
    """Information about the bot """
    embed = discord.Embed(title="KittyBot5000", description="Cutest bot you'll ever meet :3", color=0xb40a78)
    embed.add_field(name="Author", value="Nyathaleen#3995")
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Favourite food:", value="Sushi, obviously")

    await ctx.send(embed = embed)

@bot.command()
async def cat(ctx):
    """Posts a random picture of a cat """
    cats = ["https://tinyurl.com/ycdl7uyn", "https://tinyurl.com/ycr4sndw", "https://tinyurl.com/y9ecyc9z", "https://tinyurl.com/ycfcng7m", "https://tinyurl.com/y8dhab79", "https://tinyurl.com/y8txcamq", "https://tinyurl.com/y8n7crm8", "https://tinyurl.com/yabt3vwn","https://tinyurl.com/y8ya3oq3", "https://tinyurl.com/yb48en2d", "https://tinyurl.com/ya2s4uhg", "https://tinyurl.com/y9hyerw7", "https://tinyurl.com/yb6mxo84", "https://tinyurl.com/yaamphrs", "https://tinyurl.com/yamc97d2", "https://tinyurl.com/y9ozfao7", "https://tinyurl.com/y8pld4x4", "https://tinyurl.com/y8s7o55u", "https://tinyurl.com/ybwl8adc", "https://tinyurl.com/y7pgm23x", "https://tinyurl.com/y8yxrnrl", "https://tinyurl.com/y9z5zbvf", "https://tinyurl.com/y9t5vjgu","https://tinyurl.com/ybtmgqv4", "https://tinyurl.com/ybg2bayo", "https://tinyurl.com/ycl3wygm", "https://tinyurl.com/yboyu4fm", "https://tinyurl.com/yau56888", "https://tinyurl.com/ybrqn2ku", "https://tinyurl.com/yay7ndky", "https://tinyurl.com/y7umg6qw" ]
    embed = discord.Embed(title="{},".format(ctx.author.display_name), description="Have a picture of a cat", color=0xb40a78)
    embed.set_image(url=random.choice(cats))
    await ctx.send(embed = embed)
    await ctx.send("<:awmycat:490840141812727818>")

@bot.command(aliases=["doggo"])
async def dog(ctx):
    """Posts a random picture of a dog"""
    dogs = ["https://tinyurl.com/ybc29gfa", "https://tinyurl.com/yajfx5fb", "https://tinyurl.com/yc6yluar", "https://tinyurl.com/y7emz3bw", "https://tinyurl.com/ya2lketb", "https://tinyurl.com/ybtbjdss", "https://tinyurl.com/ybsoyxud", "https://tinyurl.com/y73k57an", "https://tinyurl.com/ybr26wch", "https://tinyurl.com/y9qrghok", "https://tinyurl.com/ycutvvw6", "https://tinyurl.com/yaowqors", "https://tinyurl.com/yatgbmkv", "https://tinyurl.com/yddr5qh6", "https://tinyurl.com/y8gxs7e2", "https://tinyurl.com/ybu2mhbe", "https://tinyurl.com/ybf62f7j", "https://tinyurl.com/ybjb42j9", "https://tinyurl.com/y7f3u857", "https://tinyurl.com/ycdlwqt6", "https://tinyurl.com/ybh4kfeq", "https://tinyurl.com/yaozz8dg", "https://tinyurl.com/ybxgsp7k", "https://tinyurl.com/ycrkwj9k", "https://tinyurl.com/yc6fy7t5", "https://tinyurl.com/yc5atout", "https://tinyurl.com/y9lqjwez", "https://tinyurl.com/ycjd39pq", "https://tinyurl.com/y98pbkgz"]
    embed = discord.Embed(title="{},".format(ctx.author.display_name), description="Enjoy your doggos", color=0xb40a78)
    embed.set_image(url=random.choice(dogs))
    await ctx.send(embed = embed)


@bot.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def work(ctx):
    """A way of earning money """
    id = ctx.message.author.id
    if id not in bank:
        await ctx.channel.send(embed = await xembed(ctx.author.display_name,"Get a bank account"))
    if "job" in bank[id]:
        j = bank[id]["job"]
        a = random.randint(salary[j],salary[j]*2)
        bank[id]["money"] += a
        await ctx.channel.send(embed = await xembed(ctx.author.display_name, random.choice(flav[bank[id]["job"]]).format(a)))
        await save()
    else:
        bank[id]["job"] = "unemployed"


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
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        time = float(str(error).split('You are on cooldown. Try again in ')[1].rstrip('s'))
        min = time//60
        sec = (time%60)
        await ctx.send(embed = await xembed(ctx.author.display_name, "You've been spending too much time at work! Come back in {} minutes and {} seconds".format(int(min), int(sec))))

@bot.command()
async def register(ctx):
    """Register a bank account """
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
    await save()

@bot.command(aliases=["balance","bal"])
async def profile(ctx):
    """Check the balance of your bank account and your current job"""
    id = ctx.message.author.id
    if id in bank:
        await ctx.send(embed = await xembed(ctx.author.display_name,"You have {}$ on your bank account and your current job is {}".format(bank[id]["money"], bank[id]["job"])))
    else:
        await ctx.send(embed = await xembed(ctx.author.display_name, "You do not have a bank account"))

async def save():
    with open('bank.json', 'w') as f:
        f.write(repr(bank))

shopdict = { "cheese": 10, "vegetables": 30, "burger": 50, "wine" : 150, "pizza": 300, "catnip": 400, "yarn": 700, "laser pointer":1000}
shopdictbonus = { "cheese": 0, "vegetables": 0.3, "burger": 1, "wine" : 4.5, "pizza": 12, "catnip": 20, "yarn": 42, "laser pointer":70}
#Bonus increase 0.1% per item
shoplist = ["cheese", "vegetables", "burger", "wine", "pizza", "catnip", "yarn", "laser pointer"]

salary = {"unemployed":10, "plumber":30, "dishwasher":60, "hairdresser":140, "teacher":300, "engineer":660, "doctor":1400}
# 200% plus 20 per job
jobdict = {"plumber":10, "dishwasher":50, "hairdresser":250, "teacher":1000, "engineer":4000, "doctor":16000}
# 400% increase
joblist = ["plumber", "dishwasher", "hairdresser", "teacher", "engineer", "doctor"]

@bot.command()
async def shop(ctx):
    """Opens the shop window"""
    embed = discord.Embed(title="Shop:", description="Use -buy' and the item name to buy" ,color=0xb40a78)
    for n in shoplist:
        embed.add_field(name="{}".format(n), value="{}$".format(shopdict[n]))
    await ctx.send(embed = embed)

@bot.command()
async def buy(ctx, arg, num:int = 1):
    """Buys an item from the shop"""
    id = ctx.message.author.id
    if arg in shopdict:
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
    await save()

@bot.command(aliases=["inv"])
async def inventory(ctx):
    """opens your inventory"""
    id = ctx.message.author.id
    embed = discord.Embed(title=ctx.author.display_name, description="Your inventory:",color=0xb40a78 )
    for n in shoplist:
        if n in bank[id]["inv"]:
            embed.add_field(name="{}".format(n), value="{}".format(bank[id]["inv"][n]))

    await ctx.send(embed = embed)


@bot.command()
async def use(ctx, item, num:int = 1):
    """Uses item in your inventory"""
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
        await save()

@bot.command()
async def jobs(ctx):
    """lists available jobs"""
    id = ctx.message.author.id
    embed = discord.Embed(title=ctx.author.display_name, description="Here are the possible jobs", color=0xb40a78)
    for n in joblist:
        embed.add_field(name="{}".format(n), value="Power level needed {}".format(jobdict[n]))
    await ctx.send(embed = embed)
    await ctx.send("Your current power level: {}".format(bank[id]["power"]))




@bot.command()
async def getjob(ctx, job):
    """get a job"""
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
    await save()




suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
cardnums = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
pokergame = {}
pokergame["users"] = {}
pokergame["pot"] = 0
players = []
puser = []
@bot.command()
async def phost(ctx, monies:int = 100):
    """host game of poker"""
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

@bot.command()
async def pjoin(ctx, monies:int = 100):
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

@bot.command()
async def endpoker(ctx):
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
        await ctx.send("The poker game has been ended manually")
    else:
        await ctx.send("You're not a part of the poker game you can't end it!")

@bot.command()
async def bump(ctx):
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


@bot.command()
async def pstart(ctx):
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

async def updatemsg(ctx):
    """updates poker embed"""
    global mes
    global mes2
    global mes3
    global mes4
    embed = discord.Embed(title="Poker", color=0xb40a78)
    embed.add_field(name="Pot", value="{}".format(pokergame["pot"]))
    embed.add_field(name="Current bet", value="{}".format(pokergame["globalbet"]))
    for z in players:
        embed.add_field(name="{}".format(bot.get_user(z)), value="Markers: {}  Bet: {}".format(pokergame["users"][z]["markers"], pokergame["users"][z]["bet"]))
    if pokergame["carderino"] == 1:
        embed.add_field(name="Community cards", value="{},   {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2] ))
    elif pokergame["carderino"] == 2:
        embed.add_field(name="Community cards", value="{},   {},   {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3]))
    elif pokergame["carderino"] == 3:
        embed.add_field(name="Community cards", value="{},   {},   {},  {} and  {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
    embed.add_field(name="Response", value="{}".format(pmessage))
    return await mes.edit(embed = embed)

async def startpoker(ctx):
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
    for n in puser:
        a = n
        await bot.get_user(n).send("You have {} and {}".format(pokergame["users"][a]["ucards"][0],pokergame["users"][a]["ucards"][1]))
    for i in puser:
        pokergame["pot"] +=20
        pokergame["users"][i]["markers"] -=20
    await ctx.send("20 Markers from every participant has been put in the pot")
    global mes4
    return await mes4.edit(content = "It's {}'s turn. use -fold, -raise or -call ".format(bot.get_user(puser[0])))
    await updatemsg(ctx)

@bot.command()
async def fold(ctx):
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


@bot.command(name='raise')
async def rais(ctx, num:int):
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

@bot.command()
async def quit(ctx):
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

@bot.command()
async def check(ctx):
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

@bot.command()
async def call(ctx):
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

async def nextturn(ctx, arg):
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
        return await mes4.edit(content = "It's {}'s turn. use -fold, -check, -raise or -call ".format(bot.get_user(puser[c])))
        await updatemsg(ctx)
    else:
        checkval = 0
        for z in range(len(puser)):
            if pokergame["users"][puser[z]]["check"] == 0 and pokergame["carderino"] < 3:
                pokergame["users"][puser[z]]["turn"] = "yes"
                checkval = 1
                if checkval > 0:
                    return await mes4.edit(content = "Waiting for {} to re-raise, fold or check".format(bot.get_user(puser[z])))
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

async def flop(ctx):
    """reveal first three communitycards"""
    pokergame["users"][puser[0]]["turn"] = "yes"
    return await mes4.edit(content = "It's {}'s turn!".format(bot.get_user(puser[0])))
    await updatemsg(ctx)
async def turn(ctx):
    """reveal fourth communitycard"""
    pokergame["users"][puser[0]]["turn"] = "yes"
    return await mes4.edit(content = "It's {}'s turn!".format(bot.get_user(puser[0])))
    await updatemsg(ctx)
async def river(ctx):
    """reveal final communitycard"""
    pokergame["users"][puser[0]]["turn"] = "yes"
    return await mes4.edit(content = "It's {}'s turn!".format(bot.get_user(puser[0])))
    await updatemsg(ctx)

async def reveal(ctx):
    """calculates the values of everyone's hands"""
    await countc()
    await straight()
    await flush()
    await pair()
    await ctx.send("On the table is {},  {},  {},  {},  and {}".format(pokergame["table"][0], pokergame["table"][1], pokergame["table"][2], pokergame["table"][3], pokergame["table"][4]))
    for z in puser:
        pokergame["users"][z]["result2"] = 0
        await ctx.send("{} had {} and {}".format(bot.get_user(z), pokergame["users"][z]["ucards"][0],pokergame["users"][z]["ucards"][1] ))
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

async def pokerend(ctx):
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
        await ctx.send("{} is the only person left standing and has won! They exchange their markers for {}$".format(bot.get_user(players[0]), round(pokergame["users"][players[0]]["markers"]/3)))
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

async def killoff(ctx):
    """removes players with too few markers"""
    global players
    for z in players:
        if pokergame["users"][z]["markers"] < 20:
            players.remove(z)
            await ctx.send("{} doesn't have enough markers to keep on playing!".format(bot.get_user(z)))

async def pokerwin(ctx):
    """checks which hand is the highest"""
    a = [pokergame["users"][puser[0]]["result"], puser[0], pokergame["users"][puser[0]]["result2"]]
    for z in puser:
        if pokergame["users"][z]["result"] > a[0]:
            a = [pokergame["users"][z]["result"], z, pokergame["users"][z]["result2"]]
        elif pokergame["users"][z]["result"] == a[0]:
            if pokergame["users"][z]["result2"] > a[2]:
                a = [pokergame["users"][z]["result"], z, pokergame["users"][z]["result2"]]
    await ctx.send("{} has won the round and got {} markers".format(bot.get_user(a[1]), pokergame["pot"]))
    pokergame["users"][a[1]]["markers"] += pokergame["pot"]
    pokergame["pot"] = 0


async def countc():
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
            if card == "Two":
                card = 2
            elif card == "Three":
                card = 3
            elif card == "Four":
                card = 4
            elif card == "Five":
                card = 5
            elif card == "Six":
                card = 6
            elif card == "Seven":
                card = 7
            elif card == "Eight":
                card = 8
            elif card == "Nine":
                card = 9
            elif card == "Ten":
                card = 10
            elif card == "Jack":
                card = 11
            elif card == "Queen":
                card = 12
            elif card == "King":
                card = 13
            else:
                card = 14
            if suit == "Spades":
                suit = 1
            elif suit== "Clubs":
                suit = 2
            elif suit== "Hearts":
                suit = 3
            elif suit== "Diamonds":
                suit = 4
            pokergame["users"][z]["hand"]["card"].append(card)
            pokergame["users"][z]["hand"]["suit"].append(suit)

async def pair():
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

async def straight():
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
async def flush():
    """checks for flush"""
    for z in puser:
        pokergame["users"][z]["hand"]["flush"] = 0
        for a in pokergame["users"][z]["hand"]["suit"]:
            x = pokergame["users"][z]["hand"]["suit"].count(a)
            if x >= 5:
                pokergame["users"][z]["hand"]["flush"] = 1

@bot.command()
async def slots(ctx, num:int = 100):
    if bank[ctx.message.author.id]["money"] >= num:
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
            bank[ctx.message.author.id]["money"] += amount
        else:
            bank[ctx.message.author.id]["money"] -= amount
        embed = discord.Embed(title="", description ="You {} {}$".format(wl, amount), color=0xb40a78)
        embed.add_field(name="Results", value="{}".format(slotOutput))
        await ctx.send(embed = embed)
    else:
        await ctx.send("You don't have enough money mate, time to stop gambling")












bot.run("MjYwNzIxMTg1MzAwNDE0NDY0.DnQo9g.BXdbG7PyIT_4qj5txJx2dwS4vyM")
