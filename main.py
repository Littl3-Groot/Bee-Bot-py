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
    await chanel.send("je suis en ligne !")
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

# Commande d'aide du Bot


@slash.slash(name="help", guild_ids=[970708155610837024], description="Envoie la commande d'aide.")
async def help(ctx):
    """Commande d'aide du Bot, Fait plusieur Embed et affiche un menu déroulant tout ça dans un Embed"""
    serveur = ctx.guild
    user = bot.get_user(970707845249130587)

    # Embed de base Accueil
    embed1 = discord.Embed(
        description=f"Bienvenue dans le message d'aide de {user.mention}, vous pourez voir ici toutes les commandes disponibles.\n\n **Commandes** : \n> - Vous pouvez retrouver toutes les commandes dispognible via le bot avec le menu déroulant ci-dessous.\n> - Pour plus d'information sur chaque commande vous avez à disposition ``/infocommande``.",
        color=0x5865F2,
    )

    embed1.add_field(name="Quelques liens utiles :",
                     value="[Chaine Youtube](https://www.youtube.com/channel/UCqEQpsMTf7WDWLGMIBHzoMg) | [Chaine twitch](https://www.twitch.tv/denverledanosaure) | [Serveur discord](https://discord.gg/4kxj4aJkdn)",
                     inline=False
                     )

    embed1.set_author(name="Bee'Bot",
                      icon_url=user.avatar_url)
    embed1.set_footer(
        text="ce message sera supprimé dans 60 secondes.")

    select = create_select(
        options=[
            create_select_option("Menu principal", value="Accueil", emoji="🏠"),
            create_select_option("Information / Serveur",
                                 value="Bot", emoji="🤖"),
            create_select_option("Modération", value="Modération", emoji="🔨"),
            create_select_option("Fun", value="Fun", emoji="😄")
        ],
        placeholder="Choisis une catégorie !",
        min_values=1,  # the minimum number of options a user must select
        max_values=1  # the maximum number of options a user can select
    )
    fait_choix = await ctx.send(embed=embed1, components=[create_actionrow(select)])

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

    # Embed des commandes concernant le Bot
    embedBot = discord.Embed(title="🤖 - Information générales et du Serveur",
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``!help``: Permet de voir la liste de toutes les commandes dispognible sur le serveur.\n> ``/serveur``: Affiche les information du serveur.",
                             color=0x5865F2,
                             )
    # Embed des commandes concernant la Modération
    embedMod = discord.Embed(title="🔨 Modération - Commandes de modération",
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``!say`` : Permet de parler en utilisant le bot.\n> ``!clear`` : Suprimme le nombre de message demandé.\n> ``!kick`` : Permet de renvoyer une personne du serveur.\n> ``!ban`` : Permet de banir définitivement une personne du serveur.\n> ``!unban`` : Permet de débanir une personne du serveur.\n> ``!warn`` : Permet de sanctionner une personne du serveur.",
                             color=0x5865F2,
                             )
    # Embed des commandes Funs
    embedFun = discord.Embed(title="😄 Fun - Commandes pour s'ammuser",
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``/seuil``: Permet de savoir en quel année le prix de votre objet aura chutter de moitié.\n> ``/francs``: Permet de convertir des Euros en Francs.\n> ``/bisextille`` : Vous permet de savoir si un année est bisextille ou non.\n> ``/dico`` : Permet de savoir quel mot est avant l'autre dans le dictionnaire.\n> ``/decimal`` : Converti un nombre Binaire en nombre décimal.\n> ``/binaire :`` Converti un nombre decimal en binaire.\n> ``/hexa`` : Converti un nombre décimal en hexadecimal.\n> ``!roulette`` : Lance une roulette russe.\n> ``/mdp`` : Vous envoie un message contenant un mot de passe du nombre de caractères que vous souhaiter (lim = 4000) et aléatoire.\n> ``/pdp`` : Renvoie la photo de profil du membre que vous voulez.\n> ``/userinfo`` : Renvoie les information sur l'utilisateur que vous souhaiter",
                             color=0x5865F2,
                             )

    try:
        choice_ctx = await wait_for_component(bot, components=select, check=check)

        if choice_ctx.values[0] == "Accueil":
            await choice_ctx.edit_origin(content=" ", embed=embed1)
        elif choice_ctx.values[0] == "Bot":
            await choice_ctx.edit_origin(content=" ", embed=embedBot)
        elif choice_ctx.values[0] == "Modération":
            await choice_ctx.edit_origin(content=" ", embed=embedMod)
        elif choice_ctx.values[0] == "Fun":
            await choice_ctx.edit_origin(content=" ", embed=embedFun)

    except:
        return


# Ajout de tous les cogs (autre fichers Python, contenant des commandes, logs ...)
bot.add_cog(logs.Plop(bot))
bot.add_cog(arrive.Arriver(bot))
bot.add_cog(commandes_ammusantes.Divers(bot))
bot.add_cog(admin.Admin(bot))
bot.add_cog(info_commandes.Info(bot))
bot.add_cog(easter_egg.Easter(bot))
bot.add_cog(errors.ErrorCog(bot))
bot.run(TOKEN)
