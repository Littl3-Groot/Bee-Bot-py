import discord
from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)

commandes = {
    "seuil": "6",
    "francs": "7",
    "bisextille": "8",
    "dico": "9",
    "decimal": "10",
    "binaire": "11",
    "hexa": "12",
    "roulette": "13",
    "mdp": "14",
    "pdp": "15",
    "userinfo": "16",
    "serveur": "17",
    "help": "18",
    "youtube": "19",
    "twitch": "20",
    "don": "21",
    "dé": "22",
    "hack": "23",
    "planning": "24",
    "streammer": "25",
    "remerciements": "26",
    "amour": "27",
    "infocommandes": "28",
    "banner": "29",
    "ping": "30"
}


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="infocommandes", guild_ids=[970708155610837024, 753278912011698247], description="Donne plus d'information sur la commande que vous avez chosie.", options=[
        # ptet factoriser ça
        create_option(
        name="nomcommande",
        description="Le nom de la commande dont vous voulez avoir plus d'informations.",
        option_type=3,
        required=True,
        choices=[create_choice(name=nom, value=valeur) for nom, valeur in commandes.items()]
    )])

    async def infocommandes(self, ctx, nomcommande):
        """Envoie des informations sur la commande choisie"""
        embedkick = discord.Embed(title="Commande Kick :",
                                  description="Sert à renvoyer un membre du serveur. *(utilisable seulmement sur un serveur Discord)*", color=0xa06cd5)
        embedkick.add_field(name="Utilisation : ",
                            value="``!kick <utilisateur> <raison>``", inline=False)
        embedkick.add_field(
            name="Exemple :", value="!kick <@339451806709055489> Ne respecte pas les règles.", inline=False)
        embedkick.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedban = discord.Embed(title="Commande Ban :",
                                 description="Sert à Bannir un membre du serveur. *(utilisable seulement sur un serveur Discord)*", color=0xa06cd5)
        embedban.add_field(name="Utilisation : ",
                           value="``!ban <utilisateur> <raison>``", inline=False)
        embedban.add_field(
            name="Exemple :", value="!ban <@339451806709055489> Ne respecte pas les règles.", inline=False)
        embedban.set_footer(text="demandé par : " +
                            f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedunban = discord.Embed(title="Commande Unban :",
                                   description="Sert à Débannir un membre du serveur. *(utilisable seulement sur un serveur Discord)*", color=0xa06cd5)
        embedunban.add_field(name="Utilisation : ",
                             value="``!unban <utilisateur> <raison>``", inline=False)
        embedunban.add_field(
            name="Exemple :", value="!unban <@339451806709055489> Ne respecte pas les règles.", inline=False)
        embedunban.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedsay = discord.Embed(title="Commande Say :",
                                 description="Sert à parler en utilisant le bot.", color=0x5865f2)
        embedsay.add_field(name="Utilisation : ",
                           value="``!say <phrase ou mot à dire>``", inline=False)
        embedsay.add_field(
            name="Exemple :", value="!say J'aime les exponentiels.", inline=False)
        embedsay.set_footer(text="demandé par : " +
                            f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedwarn = discord.Embed(title="Commande Warn :",
                                  description="Sert à avertir un utilisateur. *(utilisable seulement sur un serveur Discord)*", color=0xa06cd5)
        embedwarn.add_field(name="Utilisation : ",
                            value="``!warn <utilisateur> <raison>``", inline=False)
        embedwarn.add_field(
            name="Exemple :", value="!warn <@339451806709055489> Ne respecte pas les règles.", inline=False)
        embedwarn.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedclear = discord.Embed(title="Commande Clear :",
                                   description="Sert à effacer le nomrbe de messages que vous voulez. *(utilisable seulement sur un serveur Discord)*", color=0xa06cd5)
        embedclear.add_field(name="Utilisation : ",
                             value="``!clear <nombre de messages à supprimer>``", inline=False)
        embedclear.add_field(
            name="Exemple :", value="!clear 10", inline=False)
        embedclear.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedseuil = discord.Embed(title="Commande Seuil :",
                                   description="Permet de savoir en quel année le prix de votre objet aura chutter de moitié.", color=0xa06cd5)
        embedseuil.add_field(name="Utilisation : ",
                             value="``/seuil <prix> <année> <taux de baisse en %>``", inline=False)
        embedseuil.add_field(
            name="Exemple :", value="/seuil 10000 2000 10", inline=False)
        embedseuil.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedfrancs = discord.Embed(title="Commande Francs :",
                                    description="Permet de convertir des Euros en Francs.", color=0xa06cd5)
        embedfrancs.add_field(name="Utilisation : ",
                              value="``/francs <Nombre d'euros>``", inline=False)
        embedfrancs.add_field(
            name="Exemple :", value="/francs 10", inline=False)
        embedfrancs.set_footer(text="demandé par : " +
                               f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedbisextille = discord.Embed(title="Commande Bisextille :",
                                        description="Vous permet de savoir si un année est bisextille ou non.", color=0xa06cd5)
        embedbisextille.add_field(name="Utilisation : ",
                                  value="``/bisextille <année>``", inline=False)
        embedbisextille.add_field(
            name="Exemple :", value="/bisextille 2005", inline=False)
        embedbisextille.set_footer(text="demandé par : " +
                                   f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embeddico = discord.Embed(title="Commande Dico  :",
                                  description="Permet de savoir quel mot est avant l'autre dans le dictionnaire.", color=0xa06cd5)
        embeddico.add_field(name="Utilisation : ",
                            value="``/dico <mot1> <mot2>``", inline=False)
        embeddico.add_field(
            name="Exemple :", value="/dico groot denver", inline=False)
        embeddico.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embeddecimal = discord.Embed(title="Commande Decimal  :",
                                     description="Converti un nombre Binaire en nombre décimal.", color=0xa06cd5)
        embeddecimal.add_field(name="Utilisation : ",
                               value="``/decimal <nombre binaire>``", inline=False)
        embeddecimal.add_field(
            name="Exemple :", value="/decimal 1010", inline=False)
        embeddecimal.set_footer(text="demandé par : " +
                                f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedbinaire = discord.Embed(title="Commande Binaire :",
                                     description="Converti un nombre Decimal en nombre Binaire.", color=0xa06cd5)
        embedbinaire.add_field(name="Utilisation : ",
                               value="``/binaire <nombre decimal>``", inline=False)
        embedbinaire.add_field(
            name="Exemple :", value="/binaire 10", inline=False)
        embedbinaire.set_footer(text="demandé par : " +
                                f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedhexa = discord.Embed(title="Commande Hexa :",
                                  description="Converti un nombre Decimal en nombre Hexadecimal.", color=0xa06cd5)
        embedhexa.add_field(name="Utilisation : ",
                            value="``/hexa <nombre decimal>``", inline=False)
        embedhexa.add_field(
            name="Exemple :", value="/hexa 10", inline=False)
        embedhexa.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedroulette = discord.Embed(title="BIENTOT...", color=0xa06cd5)
        # embedroulette.add_field(name="Utilisation : ",
        #                        value="``!roulette``", inline=False)
        # embedroulette.add_field(
        #    name="Exemple :", value="!roulette", inline=False)
        # embedroulette.set_footer(text="demandé par : " +
        #                         f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedmdp = discord.Embed(title="Commande Mot de passe :",
                                 description="Vous envoie un message contenant un mot de passe du nombre de caractères que vous souhaiter (lim = 4000) et aléatoire.", color=0xa06cd5)
        embedmdp.add_field(name="Utilisation : ",
                           value="``/mdp <nombre de caractères>``", inline=False)
        embedmdp.add_field(
            name="Exemple :", value="/mdp 12", inline=False)
        embedmdp.set_footer(text="demandé par : " +
                            f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedpdp = discord.Embed(title="Commande Photo de profil :",
                                 description="Renvoie la photo de profil du membre que vous voulez.", color=0xa06cd5)
        embedpdp.add_field(name="Utilisation : ",
                           value="``/pdp <utilisateur>``", inline=False)
        embedpdp.add_field(
            name="Exemple :", value="/pdp <@339451806709055489>", inline=False)
        embedpdp.set_footer(text="demandé par : " +
                            f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embeduserinfo = discord.Embed(title="Commande Userinfo :",
                                      description="Renvoie les information sur l'utilisateur que vous souhaiter.", color=0xa06cd5)
        embeduserinfo.add_field(name="Utilisation : ",
                                value="``/userinfo <utilisateur>``", inline=False)
        embeduserinfo.add_field(
            name="Exemple :", value="/userinfo <@339451806709055489>", inline=False)
        embeduserinfo.set_footer(text="demandé par : " +
                                 f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedserveur = discord.Embed(title="Commande Serveur :",
                                     description="Affiche les information du serveur.", color=0xa06cd5)
        embedserveur.add_field(name="Utilisation : ",
                               value="``/serveur``", inline=False)
        embedserveur.set_footer(text="demandé par : " +
                                f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedhelp = discord.Embed(title="Commande Help :",
                                  description="Permet de voir la liste de toutes les commandes dispognible sur le serveur.", color=0xa06cd5)
        embedhelp.add_field(name="Utilisation : ",
                            value="``!help``", inline=False)
        embedhelp.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedyoutube = discord.Embed(
            title="Commande Youtube :", description="Envoie le lien de la chaîne YouTube d'Im Beerus.", color=0xa06cd5)
        embedyoutube.add_field(name="Utilisation :", value="``/youtube``")
        embedyoutube.set_footer(text="demandé par : " +
                                f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedtwitch = discord.Embed(
            title="Commande Twitch :", description="Envoie le lien de la chaîne Twitch d'Im Beerus.", color=0xa06cd5)
        embedtwitch.add_field(name="Utilisation :", value="``/twitch``")
        embedtwitch.set_footer(text="demandé par : " +
                               f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embeddon = discord.Embed(
            title="Commande Don :", description="Envoie le lien pour soutenir Im Beerus.", color=0xa06cd5)
        embeddon.add_field(name="Utilisation :", value="/don")
        embeddon.set_footer(text="demandé par : " +
                            f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedde = discord.Embed(
            title="Commande Dé :", description="Démarre le lancement d'un dé.", color=0xa06cd5)
        embedde.add_field(
            name="Utilisation :", value="``/dé <tricher(oui ou nan)> <valeur minimal> <valeur maximal>``")
        embedde.add_field(
            name="Exemple :", value="/dé Non 10 100", inline=False)
        embedde.set_footer(text="demandé par : " +
                           f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedhack = discord.Embed(
            title="Commande Hack :", description="Lance un hack sur l'utilisateur choisit.", color=0xa06cd5)
        embedhack.add_field(name="Utilisation :",
                            value="``/hack <utilisateur>``")
        embedhack.add_field(
            name="Exemple :", value="/hack Im Little Groot", inline=False)
        embedhack.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedplaning = discord.Embed(title="BIENTÔT...", color=0xa06cd5)
        embedplaning.set_footer(text="demandé par : " +
                                f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedstreamer = discord.Embed(
            title="Commande Streamer :", description="Affiche des informations sur le streamer Im Beerus.", color=0xa06cd5)
        embedstreamer.add_field(name="Utilisation", value="``/streamer``")
        embedstreamer.set_footer(text="demandé par : " +
                                 f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedremerciments = discord.Embed(
            title="Commande Remerciements", description="Affiche les remerciments : librairies développeur, toutes les personnes qui ont étés utile à la création de Bee'Bot.", color=0x000000)
        embedremerciments.add_field(
            name="Utilisation :", value="``/remerciments``")
        embedremerciments.set_footer(text="demandé par : " +
                                     f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedamour = discord.Embed(
            title="Commande Amour :", description="Envoie de l'amour à la personnes choisi.", color=0xa06cd5)
        embedamour.add_field(name="Utilisation :",
                             value="``/amour <utilisateur>``")
        embedamour.add_field(name="Exemple :", value="/amour Im Beerus")
        embedamour.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedinfocommandes = discord.Embed(
            description="Bah... c'est la commande que tu utilise tu devrais avoirs comprit son fonctionnement...", color=0xa06cd5)
        embedinfocommandes.set_footer(text="demandé par : " +
                                      f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedbanner = discord.Embed(
            title="Commande Banner :", description="renvoies la bannière d'un utilisateur s'il en a une.", color=0xa06cd5)
        embedbanner.add_field(name="Utilisation :",
                              value="``/banner <utilisateur>``")
        embedbanner.add_field(name="Exemple :", value="/banner dyabolo")
        embedbanner.set_footer(text="demandé par : " +
                               f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embedping = discord.Embed(
            title="Commande Ping :", description="**PONG** ! plus sérieusement, envoie le temps de réponse du bot en \"ms\" ", color=0xa06cd5)
        embedping.add_field(name="Utilisation :", value="``/ping``")
        embedping.set_footer(text="demandé par : " +
                             f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        liste_embed = [embedkick, embedban, embedunban, embedsay, embedwarn, embedclear, embedseuil, embedfrancs, embedbisextille,
                       embeddico, embeddecimal, embedbinaire, embedhexa, embedroulette, embedmdp, embedpdp, embeduserinfo, embedserveur,
                       embedhelp, embedyoutube, embedtwitch, embeddon, embedde, embedhack, embedplaning, embedstreamer, embedremerciments,
                       embedamour, embedinfocommandes, embedbanner, embedping
                       ]
        liste_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8",
                        "9", "10", "11", "12", "13", "14", "15", "16",
                        "17", "18", "19", "20", "21", "22", "23", "24",
                        "25", "26", "27", "28", "29", "30"]

        for i in range(len(liste_embed)):
            if nomcommande == liste_values[i]:
                await ctx.send(embed=liste_embed[i])
