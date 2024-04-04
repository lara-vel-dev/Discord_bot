# Modules
import os
from discord import Intents, Member, File
from discord.ext import commands
from dotenv import load_dotenv
from easy_pil import Editor, load_image_async, Font
from typing import Final

load_dotenv()

# Import discord token
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Import id's
WELCOME_ID: Final[int] = int(os.getenv("WELCOME_CHANNEL_ID"))
GOODBYE_ID: Final[int] = int(os.getenv("FAREWELL_CHANNEL_ID"))

# Command identifier
bot = commands.Bot(command_prefix='!', intents=Intents.all())

# --- Bot events --- #

# When the bot is ready to use
@bot.event
async def on_ready():
    print("I'm ready!!")

# Sends message when a user joins the server
@bot.event
async def on_member_join(member: Member):
    channel = member.guild.system_channel
    backgroung = Editor("1.png")
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((290, 290)).circle_image()
    poppins = Font.poppins(size=25, variant="bold")

    backgroung.paste(profile, (380, 155))
    backgroung.text((525, 475), f"{member.name}#{member.discriminator}",
                    color="white", font=poppins, align="center")
    backgroung.ellipse((380, 155), 290, 290, outline="white", stroke_width=5)

    file = File(fp=backgroung.image_bytes, filename="1.png")
    await channel.send(f"Hola {member.mention}! Bienvenidx a Danielandia")
    await channel.send(file=file)

# Sends message when a user leaves the server
@bot.event
async def on_member_remove(member: Member):
    channel = bot.get_channel(GOODBYE_ID)
    backgroung = Editor("sad-g.png")
    file = File(fp=backgroung.image_bytes, filename="sad-g.png")
    await channel.send(f"{member.name} es una pena que te vayas :(")
    await channel.send(file=file)

# --- Basic commands --- #

# Greet the users
@bot.command()
async def greetings(ctx):
    await ctx.send("Hello there!")


# Farewell the user
@bot.command()
async def farewell(ctx):
    await ctx.send("See you soon!")


if __name__ == "__main__":
    # Init Bot
    bot.run(TOKEN)
