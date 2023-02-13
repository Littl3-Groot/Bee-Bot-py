import discord
from discord.ext import commands
from discord import File
import DiscordUtils

from easy_pil import Editor, load_image_async, Font

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
        channel = self.bot.get_channel(1021051176147501096)

        #image quand une personne rejoin le serveur.
        background = Editor("image_arrive3.png")
        profile_image = await load_image_async(str(member.avatar_url))

        profile = Editor(profile_image).resize((200, 200)).circle_image()
        poppins = Font.poppins(size= 50, variant="bold")
        poppins_small = Font.poppins(size= 20, variant="light")

        background.paste(profile, (400, 90))
        background.ellipse((400, 90), 200, 200, outline ="white", stroke_width=5)

        background.text((500, 345), f"BIENVENUE", color="white", font=poppins, align="center")
        background.text((500, 410), f"{member.name}#{member.discriminator}", color="white", font=poppins, align="center")
       
        file = File(fp=background.image_bytes, filename="pic1.jpg")
        await channel.send(file=file)
        #inviter = await self.tracker.fetch_inviter(member)
        # inviter is the member who invited
        #await channel.send(f"__**Bienvenue à toi**__ {member.mention}  sur le serveur de Im Beerus ! <:beeyop:1051253222477668514>")

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
