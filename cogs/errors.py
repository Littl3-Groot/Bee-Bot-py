import discord
from discord.ext import commands
import asyncio
import random


bot = commands.Bot(command_prefix="!")


class ErrorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(error, commands.CommandNotFound):
                embed_erreur = discord.Embed(
                    title=f"<:x_:985826783159021628> Erreur !", description=f"La commande ``{ctx.message.content}`` n'existe pas. Veuillez réitérer votre demande.", color=0xD00000)
                embed_erreur.set_footer(
                    text="ce message sera supprimé dans 15 secondes.")
                msg = await ctx.reply(embed=embed_erreur)
                await asyncio.sleep(15)
                await ctx.message.delete()
                await msg.delete()
            elif isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    description='⚠️ ┃ Tu n\'as pas les permissions nécessaires pour effectuer '
                                'cette commande.', color=0xd00000
                )
                embed.set_footer(
                    text="ce message sera supprimé dans 15 secondes.")
                msg = await ctx.reply(embed=embed)
                await asyncio.sleep(15)
                await ctx.message.delete()
                await msg.delete()
            else:
                await ctx.send(f"{error}")
        except Exception as error:
            await ctx.send(f"{error}")
