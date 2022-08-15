import discord
from discord.ext import commands
import asyncio
import random
import string
import random
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
    async def denver(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://media.discordapp.net/attachments/819280204907544628/974428697815822356/makeitmeme_K9QNN.png?width=587&height=670")

    @commands.command()
    async def tipsi(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://media.discordapp.net/attachments/819280204907544628/974421556753203270/makeitmeme_3950Z.png?width=690&height=670")

    @commands.command()
    async def dcorp(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/819280204907544628/974424878969155615/makeitmeme_9RR4C.png")

    @commands.command()
    async def poulpie(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://media.discordapp.net/attachments/819280204907544628/974422245818630154/makeitmeme_z8xYd.png?width=1188&height=670")

    @commands.command()
    async def groot(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://media.discordapp.net/attachments/819280204907544628/974421242025218129/makeitmeme_4Z1DT.png?width=679&height=670")

    @commands.command()
    async def sunday(self, ctx):
        await ctx.message.delete()
        await ctx.send("https://media.discordapp.net/attachments/819280204907544628/974428032926371910/makeitmeme_lxg1k.png?width=815&height=670")
