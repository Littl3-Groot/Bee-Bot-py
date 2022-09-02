# Imports de tous les modules nécessaires au bon fonctionnement du bot
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import random


# imports des cogs
import cogs.logs as logs
import cogs.arrive as arrive
import cogs.admin as admin
import cogs.commandes_ammusantes as commandes_ammusantes
import cogs.info_commandes as info_commandes
import cogs.easter_egg as easter_egg
import cogs.errors as errors

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.utils.manage_components import *
from discord_slash.model import SlashCommandPermissionType

import asyncio
import os

from dotenv import load_dotenv


from config import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(firebase_config)
databaseApp = firebase_admin.initialize_app(cred, {
    'databaseURL': DatabaseUrl
})


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
status = ["/help", "manger ! 🍦", "V1"]

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


@bot.event
async def on_message(ctx):
    user = ctx.author.id
    member = ctx.author
    ref = db.reference('/users')
    users_ref = ref.child('messages')
    if member.bot == True:
        return
    users_ref.update({
        user: {
            "Message": str(ctx.content)
        }
    })


# ça marche !
#ref = db.reference("/users/beebot/")
#beebot = ref.get()
# print(beebot)
# for users, value in beebot.items():
#    if(value["Première question"] == True):
#        print("Première question validée")


# Commande qui affiche le temps de réponse du bot (ping)


@slash.slash(name="ping", guild_ids=[970708155610837024], description="Affiche le temps de réponse du bot.")
async def ping(ctx):
    """Donne le temps de réponse du bot et l'envoie dans un Embed"""
    user = ctx.author.id
    embed = discord.Embed(title="Pong ! 🏓", description=f'**⌛ Temps :** {round(bot.latency * 1000)}ms ',
                          color=0x5865F2)
    embed.set_footer(text="demandé par : " +
                          f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
    ref = db.reference('/users')
    beebot_ref = ref.child('beebot')
    beebot_ref.update({
        user: {
            "Première question": True
        }
    })
    await ctx.reply(embed=embed)

# Commande qui affiche la banière de l'utilisateur choisit


@slash.slash(name="banner", guild_ids=[970708155610837024], description="Affiche la bannière de l'utilisateur choisit.", options=[
    create_option(name="user",
                  description="L'utilisateur dont tu veux voir la bannière.", option_type=6, required=True),
])
async def banner(ctx, user: discord.Member):
    """"Récupère la banière de 'user' et l'envoie"""
    if user is None:
        user = ctx.author
    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    banner_url = "Cet utilisateur n'a pas de banière."
    # If statement because the user may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.gif?size=1024"
    # ça marche pas très bien pour l'instant, le if marche mais pas pour l'id unique
    #ref = db.reference("/users/beebot/")
    #beebot = ref.get()
    # print(beebot)
    # for users, value in beebot.items():
    #    if(value["Première question"] == True):
    #        print("Première question validée")
    #    else:
    #        return
    await ctx.send(f"{banner_url}")

# @bot.command()
# async def dm_all(ctx, *, args=None):
#    if args != None:
#        members = ctx.guild.members
#        for member in members:
#            try:
#                await member.send(args)
#            except:
#                print("Ne fonctionne pas.")
#
#    else:
#        await ctx.send("Please provide an argument !")
#
#
# @bot.command()
# async def dm(ctx, user_id=None, *, args=None):
#    if user_id != None and args != None:
#        try:
#            target = await bot.fetch_user(user_id)
#            await target.send(args)
#
#            await ctx.channel.send("'" + args + "' sent to: " + target.name)
#
#        except:
#            await ctx.channel.send("Couldn't dm the given user.")
#
#    else:
#        await ctx.channel.send("You didn't provide a user's id and/or a message.")
#

# Commande d'aide du Bot


@slash.slash(name="help", guild_ids=[970708155610837024], description="Envoie la commande d'aide.")
async def help(ctx):
    """Commande d'aide du Bot, Fait plusieur Embed et affiche un menu déroulant tout ça dans un Embed"""
    user = bot.get_user(970707845249130587)
    users = ctx.author.id

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
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``/help``: Permet de voir la liste de toutes les commandes dispognible sur le serveur.\n> ``/serveur``: Affiche les information du serveur. \n> ``/userinfo``: La commande userinfo vous permet d'afficher les informations d'un utilisateur choisit, Date de création du compte, nombre de rôles.... \n> ``/youtube``: envoie le lien de la chaîne YouTube de Beerus. \n> ``/twitch``: envoie le lien de la chaîne Twitch de Beerus. \n> ``/don``: envoie le lien pour faire des dons a Im Beerus. \n> ``/streamer``: Cette commande envoie tout les liens intéressant concernant Beerus. \n> ``/remerciments``: Cette commande affiche tous les remerciement concernant la création de Bee'Bot. . \n> ``/infocommande``: Cette commande vous permet de savoir comment utiliser n'importe quelle commande disponible sur Bee'Bot. \n ``/staff`` : Affiche les membres du staff.",
                             color=0x5865F2,
                             )
    # Embed des commandes concernant la Modération
    embedMod = discord.Embed(title="🔨 Modération - Commandes de modération",
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``!say`` : Permet de parler en utilisant le bot.\n> ``!clear`` : Suprimme le nombre de message demandé.\n> ``!kick`` : Permet de renvoyer une personne du serveur.\n> ``!ban`` : Permet de banir définitivement une personne du serveur.\n> ``!unban`` : Permet de débanir une personne du serveur.\n> ``!warn`` : Permet de sanctionner une personne du serveur.",
                             color=0x5865F2,
                             )
    # Embed des commandes Funs
    embedFun = discord.Embed(title="😄 Fun - Commandes pour s'ammuser",
                             description="- Utilisez ``/infocommande`` pour voir les détails d'une commande.\n\n> ``/seuil``: Permet de savoir en quel année le prix de votre objet aura chutter de moitié.\n> ``/francs``: Permet de convertir des Euros en Francs.\n> ``/bisextille`` : Vous permet de savoir si un année est bisextille ou non.\n> ``/dico`` : Permet de savoir quel mot est avant l'autre dans le dictionnaire.\n> ``/decimal`` : Converti un nombre Binaire en nombre décimal.\n> ``/binaire :`` Converti un nombre decimal en binaire.\n> ``/hexa`` : Converti un nombre décimal en hexadecimal.\n> ``!roulette`` : bientôt.\n> ``/mdp`` : Vous envoie un message contenant un mot de passe du nombre de caractères que vous souhaiter (lim = 4000) et aléatoire.\n> ``/pdp`` : Renvoie la photo de profil du membre que vous voulez.\n> ``/dé`` : Lance un dé entre 1 et 6 de base (vous pouvez changer cette valeur). \n> ``/hack`` : Lance un hacck sur l'utilisateur choisit. \n> ``/amour`` : Envoie de l'amour à l'utilisateur choisit. \n> ``/banner`` : Affiche la banière de l'utilisateur choisit. \n> ``/ping`` : Affiche le temps de réponse du bot.",
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
        await ctx.send("Erreur !")


# Ajout de tous les cogs (autre fichers Python, contenant des commandes, logs ...)
bot.add_cog(logs.Plop(bot))
bot.add_cog(arrive.Arriver(bot))
bot.add_cog(commandes_ammusantes.Divers(bot))
bot.add_cog(admin.Admin(bot))
bot.add_cog(info_commandes.Info(bot))
bot.add_cog(easter_egg.Easter(bot))
bot.add_cog(errors.ErrorCog(bot))
bot.run(TOKEN)
