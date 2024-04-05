# Modules
import os
import random
from discord import Intents, Member, File, Embed, utils
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
MESSAGE: Final[int] = int(os.getenv("MESSAGE_ID"))

# Command identifier
bot = commands.Bot(command_prefix='!', intents=Intents.all())

# Deletes default command "help"
bot.remove_command('help')

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


# Adds role to user
@bot.event
async def on_raw_reaction_add(payload):
    # Fetch message
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

    if message.id == MESSAGE:
        member: Member = payload.member
        guild = member.guild
        emoji = payload.emoji.name

        if emoji == '🎨':
            role = utils.get(guild.roles, name="Frontend-dev")
            role_names = ("Backend-dev", "Mobile-dev", "Data-analyst")
            roles_to_remove = tuple(utils.get(guild.roles, name=n)
                                    for n in role_names)
            emojis = ('🛠️', '📱', '📊')
            await member.remove_roles(*roles_to_remove)
            for e in emojis:
                await message.remove_reaction(e, member)

        elif emoji == '🛠️':
            role = utils.get(guild.roles, name="Backend-dev")
            role_names = ("Frontend-dev", "Mobile-dev", "Data-analyst")
            roles_to_remove = tuple(utils.get(guild.roles, name=n)
                                    for n in role_names)
            emojis = ('🎨', '📱', '📊')

            await member.remove_roles(*roles_to_remove)
            for e in emojis:
                await message.remove_reaction(e, member)

        elif emoji == '📱':
            role = utils.get(guild.roles, name="Mobile-dev")
            role_names = ("Frontend-dev", "Backend-dev", "Data-analyst")
            roles_to_remove = tuple(utils.get(guild.roles, name=n)
                                    for n in role_names)
            emojis = ('🎨', '📊', '🛠️')

            await member.remove_roles(*roles_to_remove)
            for e in emojis:
                await message.remove_reaction(e, member)

        elif emoji == '📊':
            role = utils.get(guild.roles, name="Data-analyst")
            role_names = ("Frontend-dev", "Backend-dev", "Mobile-dev")
            roles_to_remove = tuple(utils.get(guild.roles, name=n)
                                    for n in role_names)
            emojis = ('🎨', '📱', '🛠️')

            await member.remove_roles(*roles_to_remove)
            for e in emojis:
                await message.remove_reaction(e, member)

        await member.add_roles(role)


# Adds role to user
@bot.event
async def on_raw_reaction_remove(payload):

    if MESSAGE == payload.message_id:
        guild = await (bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        if emoji == '🎨':
            role = utils.get(guild.roles, name="Frontend-dev")
            
        elif emoji == '🛠️':
            role = utils.get(guild.roles, name="Backend-dev")
            
        elif emoji == '📱':
            role = utils.get(guild.roles, name="Mobile-dev")
            
        elif emoji == '📊':
            role = utils.get(guild.roles, name="Data-analyst")
        
        member = await(guild.fetch_member(payload.user_id))

        if member is not None:
            await member.remove_roles(role)

# --- Basic commands --- #

# Greet the users
@bot.command()
async def greetings(ctx):
    await ctx.send("¡Hola! :D")


# Farewell the user
@bot.command()
async def farewell(ctx):
    await ctx.send("¡Nos vemos pronto! :)")


# Help (Shows all commands)
@bot.command()
async def help(ctx):
    pass


# Bot joins a voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Necesitas estar conectado en un canal de voz")


# Bot leaves a voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Ya me voy pues :(")
    else:
        ctx.send("No estoy en un canal de voz xd")


# Add roles
@bot.command()
async def roles(ctx):
    # Create embed link
    embed = Embed(title="Sistema de roles",
                  description="¡Hola 👋!\n¿En qué área te desenvuelves más?\n(Selecciona 1)" +
                  "\n🎨 Frontend\n🛠️ Backend\n📱 Móvil\n📊 Ciencia de datos",
                  color=0x0091CF
                  )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🎨')
    await msg.add_reaction('🛠️')
    await msg.add_reaction('📱')
    await msg.add_reaction('📊')


# Game ball-8
@bot.command()
async def ball8(ctx, question):
    answers = ["Obvio microbio", "Tsss se me hace que no",
               "Pue que si, pue que no"]
    answer = random.choice(answers)
    await ctx.send(answer)


if __name__ == "__main__":
    # Init Bot
    bot.run(TOKEN)
