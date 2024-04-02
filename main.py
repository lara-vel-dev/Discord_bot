# Modules
import os
from discord import Intents, Client, Message
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final

# Import discord token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Command identifier
bot = commands.Bot(command_prefix='!', intents=Intents.all())


# --- Basic commands --- #

# Greet the user
@bot.command()
async def greetings(ctx):
    await ctx.send("Hello there!")


# Init Bot
bot.run(TOKEN)

    