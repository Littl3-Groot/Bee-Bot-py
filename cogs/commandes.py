import discord
from discord.ext import commands
import asyncio
import random
import string
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)

from fonctions import *


def setup(bot):
    bot.add_cog(Divers(bot))


class Divers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="serveur", guild_ids=[970708155610837024, 753278912011698247],
                   description="Permet de voir les information du serveur")
    async def serveur(self, ctx):
        """Affiche les informations du serveur"""

        serveur = ctx.guild
        numberOfTextChannels = len(serveur.text_channels)
        numberOfVoiceChannels = len(serveur.voice_channels)
        numberOfPerson = serveur.member_count
        serverName = serveur.name
        serverIcon = serveur.icon_url
        serverId = serveur.id
        serveurOwner = serveur.owner_id
        date_creation = serveur.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        all_emotes = [str(emoji) for emoji in ctx.guild.emojis]
        emojis = '\n'.join(all_emotes)
        boost = ctx.guild.premium_subscription_count

        embed = discord.Embed(color=0x5865f2)
        embed.set_author(name=serverName, icon_url=serverIcon)
        embed.set_thumbnail(url=serverIcon)
        embed.add_field(name="👥 Membres: ", value=f"``{numberOfPerson}``", inline=False)
        embed.add_field(name="💬 Textuelles:", value=f"``{numberOfTextChannels}``", inline=True)
        embed.add_field(name="🔊 Vocaux:", value=f"``{numberOfVoiceChannels}``", inline=True)
        embed.add_field(name="📂 Catégories:", value=f"``{len(serveur.categories)}``", inline=True)
        embed.add_field(name="📅 Créé le: ", value=f"``{date_creation}``", inline=True)
        embed.add_field(name="🆔 ID serveur:", value=f"``{serverId}``", inline=True)
        embed.add_field(name="👑 Propriétaire:", value=f"<@{serveurOwner}>", inline=True)
        if ctx.guild.banner:
            embed.set_image(url=str(ctx.guild.banner_url))
        levels = ['Niveau 0', 'Niveau 1', 'Niveau 2', 'Niveau 3']
        i = min(3, boost // 30)
        embed.add_field(name="💎 Nombre de boost:", value=f"``{boost}`` {levels[i]}", inline=False)

        embed.set_footer(text=f"demandé par : {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)


    @cog_ext.cog_slash(name="seuil", guild_ids=[970708155610837024, 753278912011698247],
                       description="Permet de savoir en quel année le prix de votre objet aura chutter de moitié.",
                       options=[
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

    @cog_ext.cog_slash(name="francs", guild_ids=[970708155610837024, 753278912011698247], description="Convertir des Euros en Francs.",
                       options=[
                           create_option(name="valeureuro",
                                         description="La valeur en euro que vous voulez convetir.", option_type=4,
                                         required=True),
    ])

    async def francs(self, ctx, valeureuro: int):
        """Récupère une valeur en euro, appelle la fonction qui convertis en Francs et l'envoie dans un salon sous forme d'Embed."""
        valeurFrancs = euroToFrancs(valeureuro)
        embed = discord.Embed(
            description=f'**{valeureuro}** € c\'est ' + f'**{valeurFrancs}** Francs français ! ', color=0x5865f2)
        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="bissextile", guild_ids=[970708155610837024, 753278912011698247],
                       description="Dit si l'année marquée est bissextile ou pas.", options=[
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

    @cog_ext.cog_slash(name="dico", guild_ids=[970708155610837024, 753278912011698247],
                       description="Donne l'ordre des mots dans le dictionaire.", options=[
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
                        "`` le mot **" + f'{mot2}' +
            "** dans le dictionnaire.",
            color=0x5865F2)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="decimal", guild_ids=[970708155610837024, 753278912011698247],
                       description="Converti un nombre binaire en decimal.", options=[
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

    @cog_ext.cog_slash(name="binaire", guild_ids=[970708155610837024, 753278912011698247],
                       description="Converti un nombre decimal en binaire.", options=[
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

    @cog_ext.cog_slash(name="hexa", guild_ids=[970708155610837024, 753278912011698247],
                       description="Converti un nombre decimal en hexadecimal.", options=[
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

    @cog_ext.cog_slash(name="mdp", guild_ids=[970708155610837024, 753278912011698247],
                       description="Donne un mot de passe sécurisé au hasard.", options=[
        create_option(name="longueur",
                      description="La longueur du mot de passe (longueur original = 12)", option_type=4,
                      required=False),
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
            await ctx.send(
                "Vos mp sont fermés, je ne peux pas vous envoyer de messages. Ouvrez-les puis retentez. [ici pour savoir comment faire](https://tinyurl.com/2eucd2cr)",
                hidden=True)

    @cog_ext.cog_slash(name="userinfo", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche les informations d'un utilisateur choisit.", options=[
        create_option(name="user",
                      description="L'utilisateur dont tu veux voir les informations.", option_type=6,
                      required=True),
    ])
    async def userinfo(self, ctx, user):
        """Récupère l'utilisateur choisit et envoie les informations le concernant."""
        roles = list(user.roles)
        del roles[0]

        embed = discord.Embed(color=user.color)

        embed.set_author(
            name=f'Information de - {user}', icon_url=user.avatar_url)

        embed.set_thumbnail(url=user.avatar_url)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID', value="``" +
                        str(user.id) + "``", inline=False)
        embed.add_field(name="Pseudo :",
                        value="``" + str(user.display_name) + "``", inline=False)

        embed.add_field(name="Date création du compte", value=user.created_at.strftime(
            '``%Y-%m-%d %H:%M:%S %Z%z``'), inline=False)
        embed.add_field(name="Rejoin le : ", value=user.joined_at.strftime(
            '``%Y-%m-%d %H:%M:%S %Z%z``'), inline=False)

        if len(roles) > 0:
            embed.add_field(name=f'Rôles {len(roles)} :', value=", ".join(
                [role.mention for role in roles]), inline=False)

            embed.add_field(name="Top role :",
                            value=user.top_role.mention, inline=False)

        embed.add_field(name="Bot", value="``" +
                        str(user.bot) + "``", inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="pdp", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche la photo de profil d'un utilisateur choisit.", options=[
        create_option(name="member",
                      description="L'utilisateur dont tu veux voir la photo de profil.", option_type=6,
                      required=True),
    ])
    async def pdp(self, ctx, member: discord.User):
        """Renvoie la photo de profil de l'utilisateur choisit."""
        await ctx.send(f'{ctx.author.mention} : Voici la photo de profil de **{member.name}** :\n {member.avatar_url}')

    @cog_ext.cog_slash(name="youtube", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche le lien de la chaîne YouTube d'im Beerus.")
    async def youtube(self, ctx):
        """Renvoie le lien de la chaîne YouTube"""
        embed = discord.Embed(color=0xf00020)

        embed.add_field(name='YouTube',
                        value="Voici la chaîne YouTube **d'Im Beerus** : [Le lien](https://www.youtube.com/c/ImBeerus)",
                        inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="twitch", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche le lien de la chaine Twitch d'im Beerus.")
    async def twitch(self, ctx):
        """Renvoie le lien de la chaîne Twitch"""
        embed = discord.Embed(color=0x6441a5)

        embed.add_field(name='Twitch',
                        value="Voici la chaîne Twitch **d'Im Beerus** : [Le lien](https://www.twitch.tv/im_beerus)",
                        inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="don", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche le lien pour faire des dons à Beerus.")
    async def don(self, ctx):
        """Renvoie le lien pour faire des dons"""
        embed = discord.Embed(color=0xffd700)

        embed.add_field(name='Don 💰',
                        value="Voici le lien pour faire un don à **Beerus** : [Le lien](https://streamlabs.com/imbeerus/tip)",
                        inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="dé", guild_ids=[970708155610837024, 753278912011698247], description="Lance un dé", options=[
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

    @cog_ext.cog_slash(name="hack", guild_ids=[970708155610837024, 753278912011698247],
                       description="Lance un hack sur l'utilisateur choisit.", options=[
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
        message = await ctx.send(f"14NC3M3N7 DU H4CK <:beedead:1051253317323464704> :\n {hacking[i]}")

        for item in hacking:
            await message.edit(content=f"14NC3M3N7 DU H4CK <:beedead:1051253317323464704> :\n {item}")
            await asyncio.sleep(0.6)

        await message.edit(
            content=f"jE sUiS jUsTe Un BoT pAs Un HaCkEuR ! tU eS mécHaNt à vOuLoIr HaCkEr cE PaUVRe {user.mention}")

    @cog_ext.cog_slash(name="streamer", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche les informations concernant Im Beerus.")
    async def streamer(self, ctx):
        """Renvoie certaines informations sur le streamer"""
        embed = discord.Embed(color=0x5865f2)
        embed.set_author(
            name="Im Beerus",
            icon_url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")

        embed.add_field(name="Réseaux sociaux : ",
                        value="<:twitch:987815349451907173> Twitch : [clique ici](https://www.twitch.tv/im_beerus)\n <:youtube:987815288894554202> Youtube: [clique ici](https://www.youtube.com/c/ImBeerus)\n ",
                        inline=True)

        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="remerciements", guild_ids=[970708155610837024, 753278912011698247],
                       description="Affiche les remerciements et les credits.")
    async def remerciements(self, ctx):
        """Envoie les remerciements"""
        embed = discord.Embed(title="__Remerciements :__", color=0xa06cd5)
        embed.set_author(
            name="Bee'Bot",
            icon_url="https://cdn.discordapp.com/avatars/970707845249130587/9c4130ae252db8fdb9a8b3d9e1d9863f.webp?size=1024")
        embed.add_field(name="Librairies et hébergeur: ",
                        value="[discord.py](https://discordpy.readthedocs.io/en/stable/)\n[discord_slash](https://pypi.org/project/discord-py-slash-command/)\n[random](https://docs.python.org/fr/3/library/random.html)\n[asyncio](https://docs.python.org/fr/3/library/asyncio.html) \n[heroku](https://dashboard.heroku.com/apps)",
                        inline=True)
        embed.add_field(name="Développeur : ",
                        value="<@339451806709055489>", inline=True)

        embed.set_footer(text=" Développeur : Im Little Groot",
                         icon_url='https://images-ext-2.discordapp.net/external/-lgvQlDkxHESfYb2GaSj_R1-OF1tIftUjbE8O5Be-5k/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/339451806709055489/a_29c854cacd0437ac5091a1793447cbfe.gif')
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(name="amour", guild_ids=[970708155610837024, 753278912011698247],
                       description="Envoie de l'amour à l'utilisateur choisit.", options=[
        create_option(name="user",
                      description="L'utilisateur à qui tu veux envoyer de l'amour !", option_type=6, required=True),
    ])
    async def amour(self, ctx, user):
        """Envoi de l'amour à l'utilisateur choisit."""
        await ctx.send(f"{user.mention}, **{ctx.author}** vous envoie de l'amour ! <:beelove:1051253178424885338>")

    @cog_ext.cog_slash(name="staff", guild_ids=[970708155610837024, 753278912011698247], description="Affiche les membres du Staff.")
    async def staff(self, ctx):
        """Renvoie la liste du staff"""
        embed = discord.Embed(
            description="Ci-dessous, vous pouvez retrouver la liste du Staff du serveur ``Im Beerus`` vous pouvez les contacter en cas de problème. \n\n *PS : pour les problèmes concernant <@970707845249130587> contacter uniquement <@339451806709055489>.*",
            color=0xa06cd5)
        embed.set_author(
            name="Im Beerus Staff",
            icon_url="https://cdn.discordapp.com/avatars/281079773827039232/a_f516c458e6a1ab14fa95236a45b74e94.gif?size=4096")
        embed.add_field(name="Fondateurs : ",
                        value="<@281079773827039232> et <@339451806709055489>", inline=False)
        embed.add_field(name="Administrateurs :",
                        value="<@240471762960121857> et <@473161105896898607>", inline=False)
        embed.add_field(name="Super modérateur : ",
                        value="<@313136346929692673>", inline=False)
        embed.add_field(name="Modérateur : ",
                        value="<@301968850671632388>", inline=False)
        embed.set_footer(text="demandé par : " +
                              f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
