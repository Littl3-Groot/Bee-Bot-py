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
        channel = self.bot.get_channel(753283325984243763)

        #Background de l'image_arrive
        background = Editor("image_arrive.jpg")

        #Stocke la pdp du membre
        profile_image = await load_image_async(str(member.avatar_url))

        #Resize la pdp en un cercle 200px par 200px
        profile = Editor(profile_image).resize((200, 200)).circle_image()
        
        #Ajouts des Font
        poppins = Font.poppins(size= 50, variant="bold")
        poppins_small = Font.poppins(size= 20, variant="light")
        
        #Placement du cercle de la pdp 
        background.paste(profile, (400, 90))

        #Ajout du "cercle" autour de la pdp
        background.ellipse((400, 90), 200, 200, outline ="white", stroke_width=5)

        #Placement des textes, couleur, font, et alignement
        background.text((485, 345), f"BIENVENUE", color="white", font=poppins, align="center")
        background.text((500, 405), f"{member.name}#{member.discriminator}", color="white", font=poppins, align="center")
       
        file = File(fp=background.image_bytes, filename="pic1.jpg")
        await channel.send(file=file)

        #inviter = await self.tracker.fetch_inviter(member)
        # inviter is the member who invited
        await channel.send(f"__**Bienvenue à toi**__ {member.mention}  sur le serveur de Im Beerus ! <:beeyop:1051253222477668514>")

    # Départ
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(972922901781164102)

        #Background de l'image_arrive
        background = Editor("image_depart.jpg")

        #Stocke la pdp du membre
        profile_image = await load_image_async(str(member.avatar_url))

        #Resize la pdp en un cercle 200px par 200px
        profile = Editor(profile_image).resize((200, 200)).circle_image()
        
        #Ajouts des fonts
        poppins = Font.poppins(size= 50, variant="bold")
        poppins_small = Font.poppins(size= 20, variant="light")
        
        #Placement du cercle de la pdp 
        background.paste(profile, (400, 90))

        #Ajout du "cercle" autour de la pdp
        background.ellipse((400, 90), 200, 200, outline ="white", stroke_width=5)

        #Placement des textes, couleur, font, et alignement
        background.text((485, 345), f"À BIENTÔT", color="white", font=poppins, align="center")
        background.text((500, 405), f"{member.name}#{member.discriminator}", color="white", font=poppins, align="center")
       
        file = File(fp=background.image_bytes, filename="pic1.jpg")
        await channel.send(file=file)
