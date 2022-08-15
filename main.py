# Imports de tous les modules nécésaires au bon fonctionnement du bot
import discord
from discord.ext import commands, tasks

import random

from config import *

# imports des cogs
import cogs.logs as logs
import cogs.arrive as arrive
import cogs.admin as admin
import cogs.commandes_ammusantes as commandes_ammusantes
import cogs.info_commandes as info_commandes
import cogs.easter_egg as easter_egg

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
# from discord_slash.model import SlashCommandPermissionType
# from discord.ext.commands import MissingPermissions


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
status = ["Lords mobile ⚔️", "Mythic Heroes 💎",
          "Regarder Beerus sur Youtube", "manger ! 🍦", "s'auto programmer 👨‍💻"]

# Change le statut du bot toute les 5 secondes


@tasks.loop(seconds=5)
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


# Commande d'aide du Bot
@bot.command(invoke_without_command=True)
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
    action_row = create_actionrow(select)

    await ctx.send(embed=embed1, components=[action_row])

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

    while True:
        try:
            select_interaction = await bot.wait_for("select_option")

            if select_interaction.values[0] == "Accueil":
                await select_interaction.edit_origin(content=" ", embed=embed1)
            elif select_interaction.values[0] == "Bot":
                await select_interaction.edit_origin(content=" ", embed=embedBot)
            elif select_interaction.values[0] == "Modération":
                await select_interaction.edit_origin(content=" ", embed=embedMod)
            elif select_interaction.values[0] == "Fun":
                await select_interaction.edit_origin(content=" ", embed=embedFun)

        except:
            return

# Gère l'erreure où il ne trouve pas la commande demandé par l'utilisateur.


@bot.event
async def on_command_error(ctx, error):
    """Quand une commande n'est pas trouvée, cela renvoie un message d'erreur et supprime le message de l'utilisateur et du bot dans les 15 secondes après l'envoie du message d'erreur."""
    if isinstance(error, commands.CommandNotFound):
        embed_erreur = discord.Embed(
            title=f"<:x_:985826783159021628> Erreur !", description=f"La commande ``{ctx.message.content}`` n'existe pas. Veuillez réitérer votre demande.", color=0xD00000)
        embed_erreur.set_footer(
            text="ce message sera supprimé dans 15 secondes.")
        embed = await ctx.reply(embed=embed_erreur)
        await asyncio.sleep(15)
        await ctx.message.delete()
        await embed.delete()


@slash.slash(name="test", guild_ids=[970708155610837024], description="Affiche la bannière de l'utilisateur choisit.")
async def test(ctx):

    select = create_select(
        options=[
            create_select_option("Lab Coat", value="coat", emoji="🥼"),
            create_select_option("Test Tube", value="tube", emoji="🧪"),
            create_select_option("Petri Dish", value="dish", emoji="🧫")
        ],
        placeholder="Choose your option",
        min_values=1,  # the minimum number of options a user must select
        max_values=2  # the maximum number of options a user can select
    )
    action_row = create_actionrow(select)

    await ctx.send(components=[action_row])


# Ajout de tous les cogs (autre fichers Python, contenant des commandes, logs ...)
bot.add_cog(logs.Plop(bot))
bot.add_cog(arrive.Arriver(bot))
bot.add_cog(commandes_ammusantes.Divers(bot))
bot.add_cog(admin.Admin(bot))
bot.add_cog(info_commandes.Info(bot))
bot.add_cog(easter_egg.Easter(bot))
bot.run(TOKEN)
