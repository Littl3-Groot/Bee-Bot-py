import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import asyncio


def setup(bot):
    bot.add_cog(Admin(bot))


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # SAY
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message):

        await ctx.message.delete()
        await ctx.send(message.format(message))

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000
            )
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await embed.delete()

    # CLEAR
    @commands.command()
    @ commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nombre: int):
        await ctx.channel.purge(limit=nombre + 1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000
            )
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            embed = await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await embed.delete()

    # KICK
    @ commands.command()
    @ commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason="Aucune raison fournie"):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'{user} à été kick du serveur.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000
            )
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            embed = await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await embed.delete()

    # BAN
    @ commands.command()
    @ commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="Aucune raison fournie"):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'{user} à été ban du serveur. <:DanoCBAN:989100225174052904>')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000
            )
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            embed = await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await embed.delete()

    # UNBAN
    @ commands.command()
    @ commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user, *reason):
        reason = "".join(reason)
        username, usersDiscriminator = user.split("#")

        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == username and i.user.discriminator == usersDiscriminator:
                await ctx.guild.unban(i.user, reason=reason)
                await ctx.send(f"{user} à été unban.")
                return
        await ctx.send(f"l'utilisateur {user} n'est pas banni.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000
            )
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            embed = await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await embed.delete()

    # WARN
    @ commands.command()
    @ commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.User, *, reason="Aucune raison fournie."):
        embed = discord.Embed(
            title="Un membre à reçu un avertissement ! ⛔", color=0xfa0000)
        embed.add_field(name="Membre averti : ", value="<@" +
                        str(user.id)+">", inline=True)
        embed.add_field(name="Modérateur :", value="<@" +
                        str(ctx.author.id)+">", inline=True)
        embed.add_field(name="Raison : ", value=reason, inline=False)
        await ctx.send(embed=embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                            'cette commande.', color=0xd00000)
            embed.set_footer(
                text="ce message sera supprimé dans 15 secondes.")
            msg = await ctx.reply(embed=embed)
            await asyncio.sleep(15)
            await ctx.message.delete()
            await msg.delete()
