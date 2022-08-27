import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash import cog_ext

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)


class Easter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def beerus(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/972163356913958942/1013089421941284864/948987331296260136.webp")

    @commands.command()
    async def poney(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/972163356913958942/1013089986461040700/919272396085669909.webp")

    @commands.command()
    async def groot(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/972163356913958942/1013089986800783440/918208896433270824.webp")
