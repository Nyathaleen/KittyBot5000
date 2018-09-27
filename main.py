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
    bot.run("MjYwNzIxMTg1MzAwNDE0NDY0.DnQo9g.BXdbG7PyIT_4qj5txJx2dwS4vyM")

if __name__ == "__main__":
    Main()
