import discord
from discord.ext import commands
import asyncio
import random
import ast
from os import listdir
from os.path import isfile, join

bot = commands.Bot(command_prefix = "-", case_insensitive=True)
bot.remove_command("help")
async def loadCogs():
    for extension in [f.replace(".py", "") for f in listdir("cogs") if isfile(join("cogs", f))]:
        try:
            if not "__init__" in extension:
                print("Loading {}".format(extension))
                bot.load_extension("cogs."+extension)
        except:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

@bot.event
async def on_ready():
    await loadCogs()
    print("Bot ready")



def Main():
    with open('important.txt', "r") as f:
        token =  ast.literal_eval(f.read())
    bot.run(token)

if __name__ == "__main__":
    Main()
