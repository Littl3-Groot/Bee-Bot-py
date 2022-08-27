# Imports de tous les modules nécésaires au bon fonctionnement du bot
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import random

from config import *

# imports des cogs
import cogs.logs as logs
import cogs.arrive as arrive
import cogs.admin as admin
import cogs.commandes_ammusantes as commandes_ammusantes
import cogs.info_commandes as info_commandes
import cogs.easter_egg as easter_egg
import cogs.errors as errors
import cogs.help_command as help_command

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import *

import asyncio
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

# Liste des statuts du bot
status = ["/help", "manger ! 🍦", ]

# Change le statut du bot toute les 5 secondes


@tasks.loop(seconds=60)
async def changestatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(activity=game)

# Affiche dans la console et dans un salon quand le bot est en ligne


@bot.event
async def on_ready():
    print("je suis en ligne !")
    chanel = bot.get_channel(979821289365704704)
    # await chanel.send("je suis en ligne !")
    changestatus.start()

# Commandes pour load / unload / reload les cogs (il faut la permission administrateur)


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, name=None):
    if name:
        bot.load_extension(name)


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, name=None):
    if name:
        bot.unload_extension(name)


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, name=None):
    if name:
        try:
            bot.reload_extension(name)
        except:
            bot.load_extension(name)


# Commande qui affiche le temps de réponse du bot (ping)
@slash.slash(name="ping", guild_ids=[970708155610837024], description="Affiche le temps de réponse du bot.")
async def ping(ctx):
    """Donne le temps de réponse du bot et l'envoie dans un Embed"""
    embed = discord.Embed(title="Pong ! 🏓", description=f'**⌛ Temps :** {round(bot.latency * 1000)}ms ',
                          color=0x5865F2)
    embed.set_footer(text="demandé par : " +
                          f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    await ctx.reply(embed=embed)

# Commande qui affiche la banière de l'utilisateur choisit


@slash.slash(name="banner", guild_ids=[970708155610837024], description="Affiche la bannière de l'utilisateur choisit.", options=[
    create_option(name="user",
                  description="L'utilisateur dont tu veux voir la bannière.", option_type=6, required=True),
])
async def banner(ctx, user: discord.Member):
    """"Récupère la banière de 'user' et l'envoie"""
    if user == None:
        user = ctx.author
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    banner_url = "Cet utilisateur n'a pas de banière."
    # If statement because the user may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.gif?size=1024"
    await ctx.send(f"{banner_url}")


# Ajout de tous les cogs (autre fichers Python, contenant des commandes, logs ...)
bot.add_cog(logs.Plop(bot))
bot.add_cog(arrive.Arriver(bot))
bot.add_cog(commandes_ammusantes.Divers(bot))
bot.add_cog(admin.Admin(bot))
bot.add_cog(info_commandes.Info(bot))
bot.add_cog(easter_egg.Easter(bot))
bot.add_cog(errors.ErrorCog(bot))
bot.add_cog(help_command.Help(bot))
bot.run(TOKEN)
