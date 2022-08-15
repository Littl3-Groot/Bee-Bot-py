import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix="!")


def setup(bot):
    bot.add_cog(Plop(bot))


class Plop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # LOGS MESSAGES
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        serveur = message.guild
        channel = self.bot.get_channel(972922901781164102)

        if message.author == self.bot.user:
            return

        embed = discord.Embed(
            description=f"🗑️ Le message de {message.author.mention} dans {message.channel.mention} à été supprimé.",
            timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xD00000)

        embed.set_author(name=message.author.name,
                         icon_url=message.author.avatar_url)
        embed.add_field(
            name="Message :", value=f'```{message.content}```', inline=False)
        embed.set_footer(text=f'{serveur.name}', icon_url=serveur.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.author == self.bot.user:
            return

        serveur = before.guild
        channel = self.bot.get_channel(972922901781164102)
        embed = discord.Embed(description=f'✏️ **[Message]({before.jump_url}) envoyé par {before.author.mention} à été modifié dans le salon {before.channel.mention}**',
                              timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xFF9F40)

        embed.set_author(name=before.author.name,
                         icon_url=before.author.avatar_url)
        embed.add_field(
            name="Avant :", value=f'```{before.content}```', inline=False)
        embed.add_field(
            name="Après :", value=f' ```{after.content}```', inline=False)
        embed.set_footer(text=f'{serveur.name}', icon_url=serveur.icon_url)
        await channel.send(embed=embed)

    # LOGS MEMBERS
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        serveur = before.guild
        channel = serveur.get_channel(972922901781164102)

        if len(before.roles) > len(after.roles):
            role = next(
                role for role in before.roles if role not in after.roles)
            embed = discord.Embed(description=f':writing_hand: **{before.mention} à été mis à jour.**',
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xFF9F40)

            embed.add_field(
                name="Rôle retiré :", value=f'<:x_:985826783159021628> {role.mention}', inline=False)
        elif len(after.roles) > len(before.roles):
            role = next(
                role for role in after.roles if role not in before.roles)
            embed = discord.Embed(description=f':writing_hand: **{before.mention} à été mis à jour.**',
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xFF9F40)

            embed.add_field(
                name="Rôle ajouté :", value=f'<:valid:985826652678393867> {role.mention}', inline=False)

        elif before.nick != after.nick:
            embed = discord.Embed(
                description=f":writing_hand: **le surnom de {before.mention} à été changé.**", timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xFF9F40)

            embed.add_field(
                name="Nouveau pseudo :", value=f'```{after.nick}```', inline=False)
        else:
            return
        embed.set_thumbnail(url=before.avatar_url)
        embed.set_author(name=before.name,
                         icon_url=before.avatar_url)
        embed.set_footer(text=f'{serveur.name}', icon_url=serveur.icon_url)

        await channel.send(embed=embed)

    # LOGS MEMBERS PHOTO DE PROFIL
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        channel = self.bot.get_channel(972922901781164102)

        if before.avatar_url != after.avatar_url:
            embed = discord.Embed(description=f':writing_hand: **{before.mention} a mis à jour sa photo de profil !**',
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xFF9F40)

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            await channel.send(embed=embed)

    # LOGS SERVEUR
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        serveur = channel.guild
        chanel = self.bot.get_channel(972922901781164102)

        embed = discord.Embed(
            description=f'🏡 **Salon supprimé : **``{channel.name}``', timestamp=datetime.datetime.now(datetime.timezone.utc), color=0xD00000)

        embed.set_author(name=serveur.name,
                         icon_url=serveur.icon_url)
        embed.set_footer(text=f'{serveur.name}')

        await chanel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        serveur = channel.guild
        chanel = self.bot.get_channel(972922901781164102)

        embed = discord.Embed(description=f'🏡 **Salon créé : **``{channel.name}``',
                              timestamp=datetime.datetime.now(datetime.timezone.utc), color=0x40B21A)

        embed.set_author(name=serveur.name,
                         icon_url=serveur.icon_url)
        embed.set_footer(text=f'{serveur.name}')

        await chanel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        serveur = before.guild
        chanel = self.bot.get_channel(972922901781164102)

        if before.name != after.name:
            embed = discord.Embed(
                description=f'🏡 **Salon mis à jour : **``{before.name}``', timestamp=datetime.datetime.now(datetime.timezone.utc), color=0x5865F2)

            embed.add_field(name="Ancien nom :",
                            value=before.name, inline=True)
            embed.add_field(name="Nouveau nom :",
                            value=after.name, inline=True)
            embed.set_author(name=serveur.name,
                             icon_url=serveur.icon_url)
            embed.set_footer(text=f'{serveur.name}')

            await chanel.send(embed=embed)
