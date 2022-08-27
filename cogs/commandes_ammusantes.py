import discord
from discord.ext import commands
import asyncio
import random
import string
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash import cog_ext

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)

# Symboles pour le mot de passe généré alléatoirement
characters = list(string.ascii_letters + string.digits +
                  "!@#$%^&*()" + "1234567890")

# Toutes les fonctions nécéssaire au bon fonctionnement du Bot


def generate_random_password(longueur):
    """Génère un mot de passe aléatoire d'une longueur choisit par l'utilisateur."""
    random.shuffle(characters)

    # picking random characters from the list
    password = []
    for i in range(longueur):
        password.append(random.choice(characters))

    # shuffling the resultant password
    random.shuffle(password)

    # converting the list to string
    # printing the list
    password = ("".join(password))
    return password


def test_bissextile(annee):
    """Retourne True (vrai) si l'année correspond à une année bissextile. Sinon elle retourne False (faux)"""
    annee = annee % 4 == 0 and annee % 100 != 0 or annee % 400 == 0
    return annee


def somme_entier(nombre):
    """Retourne la somme des n premiers entiers"""
    somme = 0
    total = 0

    while somme < nombre:
        somme += 1
        total = total + somme
    return total


def vieillisement(prix, annee, pourcentage):
    """Retourne le nombre d'années où le prix aura diminué de moitié"""

    pourcentage_de_vieillisement = 1 - pourcentage / 100
    prix_de_depart = prix

    while prix > prix_de_depart / 2:
        prix = prix * pourcentage_de_vieillisement
        annee = annee + 1

    return annee


def compare(mot1, mot2):
    """Retourne l'ordre du mot1 par rapport à mot2 dans le dico"""
    resultat = "au même niveau que"
    i = 0
    while resultat == "au même niveau que" and i < len(mot1) and i < len(mot2):
        if mot1[i] < mot2[i]:
            resultat = "avant"
        elif mot1[i] > mot2[i]:
            resultat = "après"
        i += 1
    if len(mot1) != len(mot2):
        if i == len(mot1):
            resultat = "avant"
        if i == len(mot2):
            resultat = "après"
    return resultat


def decversbin(valeurdecimal):
    """Traduit une valeur decimal en une valeur binaire """
    valeurbinaire = 0
    ord = 0
    while valeurdecimal != 0:
        reste = valeurdecimal % 2
        p = 10 ** ord
        valeurbinaire = valeurbinaire + reste * p
        ord = ord + 1
        valeurdecimal = valeurdecimal // 2
    return valeurbinaire


def binversdec(binaire):
    """Traduit une valeur binaire en une valeur decimal"""
    binaire = str(binaire)
    n = len(binaire)
    valeurdecimal = 0
    for i in range(n):
        valeurdecimal = valeurdecimal + int(binaire[n - 1 - i]) * 2 ** i
    return valeurdecimal


# Table de conversion pour l'hexadecimal
conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                    13: 'D', 14: 'E', 15: 'F'}


def decimalToHexadecimal(valeurdecimal):
    """Traduit une valeur decimal en une valeur hexadecimal"""
    valeurhexadecimal = ''
    while valeurdecimal > 0:
        remainder = valeurdecimal % 16
        valeurhexadecimal = conversion_table[remainder] + valeurhexadecimal
        valeurdecimal = valeurdecimal // 16

    return valeurhexadecimal


def euroToFrancs(valeurEuro):
    """Convertis des euros en Francs français"""
    valeurFrancs = valeurEuro * 6.5596
    valeurFrancs = round(valeurFrancs, 2)
    return valeurFrancs


def setup(bot):
    bot.add_cog(Divers(bot))


class Divers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="serveur", guild_ids=[970708155610837024], description="Permet de voir les infromation du serveur")
    async def serveur(self, ctx):
        """Affiche les information du serveur"""

        serveur = ctx.guild
        numberOfTextChannels = len(serveur.text_channels)
        numberOfVoiceChannels = len(serveur.voice_channels)
        numberOfPerson = serveur.member_count
        serverName = serveur.name
        serverIcon = serveur.icon_url
        serverId = serveur.id
        serveurOwner = serveur.owner_id
        banner = ctx.guild.banner_url
        date_creation = serveur.created_at.strftime(
            "%c")
        all_emotes = [emoji for emoji in ctx.guild.emojis]
        emojis = ''.join(
            [str(i) for i in all_emotes])
        boost = ctx.guild.premium_subscription_count

        embed = discord.Embed(color=0x5865f2)
        embed.set_author(name=serverName, icon_url=serverIcon)
        embed.set_thumbnail(url=serverIcon)
        embed.add_field(name="👥┃Membres : ", value="``" +
                        str(numberOfPerson) + "``", inline=False)

        levels = ['Niveau 0', 'Niveau 1', 'Niveau 2', 'Niveau 3']
        if 0 < boost <= 2:
            i = 1
        elif 2 < boost <= 13:
            i = 2
        elif 13 < boost <= 1000:
            i = 3
        else:
            i = 0

        embed.add_field(name="💬┃Textuelles :", value="``" +
                        str(numberOfTextChannels) + "``", inline=True)

        embed.add_field(name="🔊┃ Vocaux :", value="``" +
                        str(numberOfVoiceChannels) + "``", inline=True)

        embed.add_field(name="📂┃Catégories :", value="``" + str(len(
            serveur.categories)) + "``", inline=True)

        embed.add_field(name="📅┃Créé le : ", value="``" +
                        str(date_creation) + "``", inline=True)

        embed.add_field(name="🆔┃ID serveur :", value="``" +
                        str(serverId) + "``", inline=True)

        embed.add_field(name="👑┃Propriétaire :", value="<@" +
                        str(serveurOwner) + ">", inline=True)

        embed.add_field(name=f"💎┃Nombre de boost:",
                        value="``" + str(boost) + "`` "f'{levels[i]}', inline=False)
        #embed_emotes = discord.Embed(color=0x5865f2)

        # embed_emotes.add_field(name=f"Liste des émojis [{len(all_emotes)}] :",
        #                       value=emojis, inline=False)

        embed.set_image(url=banner)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        # await ctx.reply(embed=embed_emotes)

    @cog_ext.cog_slash(name="seuil", guild_ids=[970708155610837024], description="Permet de savoir en quel année le prix de votre objet aura chutter de moitié.", options=[
        create_option(name="prix",
                      description="Le prix de l'objet.", option_type=4, required=True),
        create_option(name="annee",
                      description="L'année d'achat.", option_type=4, required=True),
        create_option(name="pourcentage",
                      description="Le taux de baisse du prix en %.", option_type=4, required=True),
    ])
    async def seuil(self, ctx, prix: float, annee: int, pourcentage: int):
        """Envoie un message qui retourne l'année où le prix aura diminué de moitié"""
        annee = vieillisement(prix, annee, pourcentage)
        embed = discord.Embed(
            description=f'En **{annee}** le prix aura baissé de moitié !', color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="francs", guild_ids=[970708155610837024], description="Convertir des Euros en Francs.", options=[
        create_option(name="valeureuro",
                      description="La valeur en euro que vous voulez convetir.", option_type=4, required=True),
    ])
    async def francs(self, ctx, valeureuro: int):
        """Récupère une valeur en euro, appelle la fonction qui convertis en Francs et l'envoie dans un salon sous forme d'Embed."""
        valeurFrancs = euroToFrancs(valeureuro)
        embed = discord.Embed(
            description=f'**{valeureuro}** € c\'est ' + f'**{valeurFrancs}** Francs français ! ', color=0x5865f2)
        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="bissextile", guild_ids=[970708155610837024], description="Dit si l'année marquée est bissextile ou pas.", options=[
        create_option(name="annee",
                      description="L'année que vous voulez vérifer", option_type=4, required=True),
    ])
    async def bissextile(self, ctx, annee: int):
        """Récupère l'année choisit par l'utilisateur et envoie dans un salon sous forme d'Embed si elle est Bisextille ou non """
        if test_bissextile(annee):
            embed = discord.Embed(title="Bissextile !", color=0x5865f2)
        else:
            embed = discord.Embed(title="Pas bissextile !", color=0x5865f2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="dico", guild_ids=[970708155610837024], description="Donne l'ordre des mots dans le dictionaire.", options=[
        create_option(name="mot1",
                      description="Mot numéro 1", option_type=3, required=True),
        create_option(name="mot2",
                      description="Mot numéro 2", option_type=3, required=True),
    ])
    async def dico(self, ctx, mot1: str, mot2: str):
        """Retourne si le mot1 est avant ou après le mot2 dans le dictionaire."""
        resultat = compare(mot1, mot2)
        embed = discord.Embed(
            description=f'Le mot **{mot1}** est ``' + f'{resultat}' +
            "`` le mot **" + f'{mot2}' + "** dans le dictionnaire.",
            color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="decimal", guild_ids=[970708155610837024], description="Converti un nombre binaire en decimal.", options=[
        create_option(name="valeurbinaire",
                      description="Nombre binaire", option_type=4, required=True),
    ])
    async def decimal(self, ctx, valeurbinaire: int):
        """Récupère une valeur binaire saisie par l'utilisateur, la convertie en decimal et envoie la valeur sous forme d'Embed dans un salon."""
        valeurdecimal = binversdec(valeurbinaire)
        embed = discord.Embed(title=" Conversion en decimal :",
                              description=f'{valeurbinaire} <:fleche:1012636976874278952> ' +
                              f'{valeurdecimal}',
                              color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="binaire", guild_ids=[970708155610837024], description="Converti un nombre decimal en binaire.", options=[
        create_option(name="valeurdecimal",
                      description="Nombre décimal", option_type=4, required=True),
    ])
    async def binaire(self, ctx, valeurdecimal: int):
        """Récupère une valeur decimal saisie par l'utilisateur, la convertie en binaire et envoie la valeur sous forme d'Embed dans un salon."""
        valeurbinaire = decversbin(valeurdecimal)
        embed = discord.Embed(title=" Conversion en binaire",
                              description=f'{valeurdecimal} <:fleche:1012636976874278952> ' +
                              f'{valeurbinaire}',
                              color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="hexa", guild_ids=[970708155610837024], description="Converti un nombre decimal en hexadecimal.", options=[
        create_option(name="valeurdecimal",
                      description="Nombre décimal", option_type=4, required=True),
    ])
    async def hexa(self, ctx, valeurdecimal: int):
        """Récupère une valeur decimal saisie par l'utilisateur, la convertie en hexadecimal et envoie la valeur sous forme d'Embed dans un salon."""
        valeurhexadecimal = decimalToHexadecimal(valeurdecimal)
        embed = discord.Embed(title=" Decimal → Hexadecimal ",
                              description=f'{valeurdecimal} <:fleche:1012636976874278952> #' +
                              f'{valeurhexadecimal}',
                              color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    # roulette pas FINI
    # @cog_ext.cog_slash(name="roulette", guild_ids=[970708155610837024], description="Lance un roulette russe.")
    # async def roulette(self, ctx):
        """Lance une roulette"""
    #    await ctx.send("La roulette commencera dans 10 secondes. Envoyer \"moi\" dans ce salon pour y participer !")

    #    joueurs = []

    #    def checkRoulette(message):
    #        return message.channel == ctx.message.channel and message.author not in joueurs and message.content == 'moi'

    #    try:
    #        while True:
    #            participation = await self.bot.wait_for("message", timeout=10, check=checkRoulette)
    #            joueurs.append(participation.author)
    #            await ctx.send(
    #                f"**{participation.author.mention}** participe à la roulette russe ! Le tirage commence dans 10 secondes.")
    #    except:
    #        print("démarrage du tirage")

    #    malus = ["ban", "kick", "mute", "soft ban", "role personnel", "gage"]

    #    message = await ctx.send("Le tirage commence dans 3 secondes !")
    #    await asyncio.sleep(1)
    #    await message.edit(content="Le tirage commence dans 2 secondes !")
    #    await asyncio.sleep(1)
    #    await message.edit(content="Le tirage commence dans 1 secondes !")
    #    await asyncio.sleep(1)
    #    loser = random.choice(joueurs)
    #    prix = random.choice(malus)
    #    await message.edit(content=f"La personne qui a gagner un {prix} est ...")
    #    await asyncio.sleep(2)
    #    await message.edit(content=f"La personne qui a gagner un {prix} est {loser.mention}")

    @cog_ext.cog_slash(name="mdp", guild_ids=[970708155610837024], description="Donne un mot de passe sécurisé au hasard.", options=[
        create_option(name="longueur",
                      description="La longueur du mot de passe (longueur original = 12)", option_type=4, required=False),
    ])
    async def mdp(self, ctx, longueur=12):
        """Récupère la longueur du mot de passe souhaiter par l'utilisateur, le crée et l'envoie dans ses messages privés."""
        mot = generate_random_password(longueur)
        embed = discord.Embed(
            description=f'Votre mot de passe est : ``{mot}``', color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                         f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        try:
            await ctx.author.send(embed=embed)
            await ctx.send("Votre mot de passe vous à été envoyé par message privé.")

        except:
            await ctx.send("je ne peux pas vous envoyer de message", hidden=True)

    @cog_ext.cog_slash(name="userinfo", guild_ids=[970708155610837024], description="Affiche les informations d'un utilisateur choisit.", options=[
        create_option(name="member",
                      description="L'utilisateur dont tu veux voir les informations.", option_type=6, required=True),
    ])
    async def userinfo(self, ctx, member: discord.Member):
        """Récupère l'utilisateur choisit et envoie les informations le concernant."""
        roles = [role for role in member.roles]

        embed = discord.Embed(color=member.color)
        embed.set_author(
            name=f'Information de - {member}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="demandé par : " +
                         f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID', value=member.id, inline=False)
        embed.add_field(name="Pseudo :",
                        value=member.display_name, inline=False)

        embed.add_field(name="Date création du compte", value=member.created_at.strftime(
            "%c"), inline=False)
        embed.add_field(name="Rejoin le : ", value=member.joined_at.strftime(
            "%c"), inline=False)

        embed.add_field(name=f'Rôles {len(roles)} :', value=", ".join(
            [role.mention for role in roles]), inline=False)
        embed.add_field(name="Top role :",
                        value=member.top_role.mention, inline=False)

        embed.add_field(name="Bot", value=member.bot, inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="pdp", guild_ids=[970708155610837024], description="Affiche la photo de profil d'un utilisateur choisit.", options=[
        create_option(name="member",
                      description="L'utilisateur dont tu veux voir la photo de profil.", option_type=6, required=True),
    ])
    async def pdp(self, ctx, member: discord.Member):
        """Renvoie la photo de profil de l'utilisateur choisit."""
        await ctx.send(f'{ctx.author.mention} : Voici la photo de profil de **{member.name}** :\n {member.avatar_url}')

    @cog_ext.cog_slash(name="youtube", guild_ids=[970708155610837024], description="Affiche le lien de la chaîne YouTube d'im Beerus.")
    async def youtube(self, ctx):
        """Renvoie le lien de la chaîne YouTube"""
        embed = discord.Embed(color=0xf00020)

        embed.add_field(
            name='YouTube', value=f"Voici la chaîne YouTube **d'Im Beerus** : [Le lien](https://www.youtube.com/c/ImBeerus)", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="twitch", guild_ids=[970708155610837024], description="Affiche le lien de la chaine Twitch d'im Beerus.")
    async def twitch(self, ctx):
        """Renvoie le lien de la chaîne Twitch"""
        embed = discord.Embed(color=0x6441a5)

        embed.add_field(
            name='Twitch', value=f"Voici la chaîne Twitch **d'Im Beerus** : [Le lien](https://www.twitch.tv/im_beerus)", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="don", guild_ids=[970708155610837024], description="Affiche le lien pour faire des dons à Denver.")
    async def don(self, ctx):
        """Renvoie le lien pour faire des dons"""
        embed = discord.Embed(color=0xffd700)

        embed.add_field(
            name='Don 💰', value=f"Voici le lien pour faire un don à **Beerus** : [Le lien](https://streamlabs.com/imbeerus/tip)", inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="dé", guild_ids=[970708155610837024], description="Lance un dé", options=[
        create_option(
            name="tricher",
            description="Tricher pour sortir toujours le même nombre (4)",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="Oui",
                    value="y"
                ),
                create_choice(
                    name="Non",
                    value="n"
                )
            ]
        ),
        create_option(name="minimum",
                      description="Le nombre le plus bas que le dé peux donner.", option_type=4, required=False),
        create_option(name="maximum",
                      description="Le nombre le plus haut que le dé peux donner.", option_type=4, required=False)
    ])
    async def dé(self, ctx, tricher, minimum=1, maximum=6):
        """Lance un dé"""
        await ctx.send("Je lance le dé...")
        num = random.randint(minimum, maximum)
        if tricher == "y":
            num = 4
        await ctx.send(f"**{num}** 🎲!")

    @cog_ext.cog_slash(name="hack", guild_ids=[970708155610837024], description="Lance un hack sur l'utilisateur choisit.", options=[
        create_option(name="user",
                      description="L'utilisateur que tu veux hacker.", option_type=6, required=True),
    ])
    async def hack(self, ctx, user: discord.User):
        """Lance un (troll) hack sur l'user choisit"""
        hacking = ["🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥",
                   "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"
                   ]
        i = 0
        message = await ctx.send(f"14NC3M3N7 DU H4CK <:DanoPeur:989100230840553517> :\n {hacking[i]}")

        for item in hacking:
            await message.edit(content=f"14NC3M3N7 DU H4CK <:DanoPeur:989100230840553517> :\n {item}")
            await asyncio.sleep(0.6)

        await message.edit(
            content=f"jE sUiS jUsTe Un BoT pAs Un HaCkEuR ! tU eS mécHaNt à vOuLoIr HaCkEr cE PaUVRe {user.mention}")

    # @cog_ext.cog_slash(name="planning", guild_ids=[970708155610837024], description="Affiche le planning des lives de Danver.")
    # async def planning(self, ctx):
    #    """Renvoie le planing des streams"""
    #    embed = discord.Embed(
    #        color=0xa06cd5, title="Planing des lives de Danver !")
    #    embed.set_image(
    #        url="https://cdn.discordapp.com/attachments/972163356913958942/985803183270006814/PLANNING.png")
    #    await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="streamer", guild_ids=[970708155610837024], description="Affiche les informations concernant Im Beerus.")
    async def streamer(self, ctx):
        """Renvoie certaines informations sur le streamer"""
        embed = discord.Embed(color=0x5865f2)
        embed.set_author(
            name="Im Beerus", icon_url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")

        embed.add_field(name="Réseaux sociaux : ",
                        value="<:twitch:987815349451907173> Twitch : [clique ici](https://www.twitch.tv/im_beerus)\n <:youtube:987815288894554202> Youtube: [clique ici](https://www.youtube.com/c/ImBeerus)\n ", inline=True)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="remerciements", guild_ids=[970708155610837024], description="Affiche les remerciements et les credits.")
    async def remerciements(self, ctx):
        """Envoie les remerciments"""
        embed = discord.Embed(title="__Remerciements :__", color=0xa06cd5)
        embed.set_author(
            name="Bee'Bot", icon_url="https://cdn.discordapp.com/avatars/970707845249130587/9c4130ae252db8fdb9a8b3d9e1d9863f.webp?size=1024")
        embed.add_field(name="Librairies : ",
                        value="[discord.py](https://discordpy.readthedocs.io/en/stable/)\n[discord_slash](https://pypi.org/project/discord-py-slash-command/)\n[random](https://docs.python.org/fr/3/library/random.html)\n[asyncio](https://docs.python.org/fr/3/library/asyncio.html)", inline=True)
        embed.add_field(name="Développeur : ",
                        value="<@339451806709055489>", inline=True)

        embed.set_footer(text=" Developpeur : Im Little Groot",
                         icon_url='https://images-ext-2.discordapp.net/external/-lgvQlDkxHESfYb2GaSj_R1-OF1tIftUjbE8O5Be-5k/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/339451806709055489/a_29c854cacd0437ac5091a1793447cbfe.gif')
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="amour", guild_ids=[970708155610837024], description="Envoie de l'amour à l'utilisateur choisit.", options=[
        create_option(name="user",
                      description="L'utilisateur à qui tu veux envoyer de l'amour !", option_type=6, required=True),
    ])
    async def amour(self, ctx, user):
        """Envoie de l'amour à l'utilisateur choisit."""
        await ctx.send(f"{user.mention}, **{ctx.author}** vous envoie de l'amour ! ❤️")

    @cog_ext.cog_slash(name="staff", guild_ids=[970708155610837024], description="Affiche les membres du Staff.")
    async def staff(self, ctx):
        """Renvoie certaines informations sur le streamer"""
        embed = discord.Embed(color=0x5865f2)
        embed.set_author(
            name="Im Beerus", icon_url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")

        embed.add_field(name="Réseaux sociaux : ",
                        value="<:twitch:987815349451907173> Twitch : [clique ici](https://www.twitch.tv/im_beerus)\n <:youtube:987815288894554202> Youtube: [clique ici](https://www.youtube.com/c/ImBeerus)\n ", inline=True)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
