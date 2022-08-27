import discord
from discord.ext import commands, tasks

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.utils.manage_components import *
from discord_slash import cog_ext

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commande d'aide du Bot
    @cog_ext.cog_slash(name="help", guild_ids=[970708155610837024], description="Envoie la commande d'aide.")
    async def help(self, ctx):
        """Commande d'aide du Bot, Fait plusieur Embed et affiche un menu déroulant tout ça dans un Embed"""

        user = self.bot.get_user(970707845249130587)

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
                create_select_option(
                    "Menu principal", value="Accueil", emoji="🏠"),
                create_select_option("Information / Serveur",
                                     value="Bot", emoji="🤖"),
                create_select_option(
                    "Modération", value="Modération", emoji="🔨"),
                create_select_option("Fun", value="Fun", emoji="😄")
            ],
            placeholder="Choisis une catégorie !",
            min_values=1,  # the minimum number of options a user must select
            max_values=1  # the maximum number of options a user can select
        )
        fait_choix = await ctx.send(embed=embed1, components=[create_actionrow(select)])

        def check(self, m):
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
        choice_ctx = await wait_for_component(bot, components=select, check=check)

        liste_embed = [embed1, embedBot, embedFun, embedMod
                       ]
        liste_values = ["0", "1", "2", "3"]

        for i in range(len(liste_embed)):
            if choice_ctx.values[0] == liste_values[i]:
                await choice_ctx.edit_origin(content=" ", embed=liste_embed[i])
