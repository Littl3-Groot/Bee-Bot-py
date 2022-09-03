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

    # DM
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def mp(self, ctx, user: discord.User, *, message):
        await user.send(f"{message}")
        await ctx.message.delete()
        embed = discord.Embed(description=f'{message}', color=0x00b200)
        embed.set_author(name="Gérant du bot",
                         icon_url="https://cdn.discordapp.com/avatars/970707845249130587/9c4130ae252db8fdb9a8b3d9e1d9863f.webp?size=1024")
        await ctx.send(embed=embed)

    # CLEAR
    @commands.command()
    @ commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, nombre: int):
        await ctx.channel.purge(limit=nombre + 1)

    # KICK
    @ commands.command()
    @ commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User, *, reason="Aucune raison fournie"):
        reason = " ".join(reason)
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f'{user} à été kick du serveur.')

    # BAN
    @ commands.command()
    @ commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User, *, reason="Aucune raison fournie"):
        reason = " ".join(reason)
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f'{user} à été ban du serveur. <:DanoCBAN:989100225174052904>')

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
