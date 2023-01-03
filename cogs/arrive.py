import discord
from discord.ext import commands
import DiscordUtils

bot = commands.Bot(command_prefix="!")


def setup(bot):
    bot.add_cog(Arriver(bot))


class Arriver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)

    # Arrivé
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(753283325984243763)
        inviter = await self.tracker.fetch_inviter(member)
        # inviter is the member who invited
        await channel.send(f"__**Bienvenue à toi**__ {member.mention}  sur le serveur de Im Beerus ! <:beeyop:1051253222477668514>")

    # Départ
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(972922901781164102)
        # inviter is the member who invited
        embed = discord.Embed(
            title=f"{member} viens de quitter le serveur.", color=0x5865f2)

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/972218791188648066/988555995754139678/au_revoir.png")
        await channel.send(embed=embed)
