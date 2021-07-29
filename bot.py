####################
import os

# Obtain bot token from Discord Developer Site
import discord
from discord import Embed, User, Member, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Context
from datetime import datetime
import requests

import psycopg2 as sql
from psycopg2 import OperationalError

DATABASE_URL = os.environ['DATABASE_URL']

conn = sql.connect(DATABASE_URL, sslmode='require')

####################
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Creates the instances, uses "+" to activate commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='+', intents=intents)

bot.remove_command('help')

# channel configuration
channel = -1


# bot commands
@bot.command(aliases=['help', 'add', 'remove', 'top', 'my', '+remove', '+set'])
async def on_message(ctx: Context, message=""):
    if ctx.invoked_with == 'help':
        # embed message
        desc = "LeetBot uses `+` as a command prefix. Below are commands supported by LeetBot."
        embed: Embed = discord.Embed(description=desc, color=15442752)
        embed.set_author(name="LeetBot Commands", icon_url="https://leetcode.com/static/images/LeetCode_logo_rvs.png")
        embed.add_field(name="View Commands", value="`+help`", inline=False)
        embed.add_field(name="Connecting your LeetCode account", value="`+add [username]`", inline=False)
        embed.add_field(name="Removing your LeetCode account", value="`+remove`", inline=False)
        embed.add_field(name="View server leaderboard", value="`+top`", inline=False)
        embed.add_field(name="View your profile", value="`+my`", inline=False)
        embed.add_field(name="Remove a LeetCode account [MOD ONLY]", value="`++remove [username]`", inline=False)
        embed.add_field(name="Set server for LeetCode feed [MOD ONLY]", value="`++set [channel]`", inline=False)
        embed.add_field(name="Need more help?",
                        value="[Github](https://github.com/48nes/) . [Discord](https://github.com/48nes/)",
                        inline=False)

        await ctx.message.channel.send(embed=embed)
    elif ctx.invoked_with == 'add':
        # error message when no username is given
        if len(message) == 0:
            desc = "No username was given."
            embed: Embed = discord.Embed(title="User Not Found", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        # TODO: check if discord user already has a linked account

        user = ctx.message.author
        profilepic = user.avatar_url

        request = requests.get('http://leetcode.com/' + message + '/')
        # user exists on leetcode
        if request.status_code == 200:
            # TODO: add leetcode username, discord username, most recently solved, total solved -> db
            now = datetime.now()
            currentTime = now.strftime("%d-%m-%y %H:%M")

            desc = "User [" + message + "](https://leetcode.com/" + message + "/) successfully added."

            embed: Embed = discord.Embed(title="Subscribed!", description=desc, color=15442752)
            embed.set_footer(text=currentTime, icon_url=profilepic)

            await ctx.message.channel.send(embed=embed)
        else:
            desc = "LeetBot was unable to find user " + message
            embed: Embed = discord.Embed(title="User Not Found", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)

    elif ctx.invoked_with == 'remove':
        user = ctx.message.author
        profilepic = user.avatar_url
        leetcode_username = "placeholder"

        # TODO: discord user not registered

        # TODO: remove from db

        # success embed message
        now = datetime.now()
        currentTime = now.strftime("%d-%m-%y %H:%M")

        desc = "User [" + leetcode_username + "](https://leetcode.com/" \
               + leetcode_username + "/) successfully removed."
        embed: Embed = discord.Embed(title="Unsubscribed", description=desc, color=15442752)
        embed.set_footer(text=currentTime, icon_url=profilepic)

        await ctx.message.channel.send(embed=embed)
    elif ctx.invoked_with == 'top':
        # TODO: get the top from db
        # TODO: embed message
        await ctx.message.channel.send('this command is still a massive wip lol')
    elif ctx.invoked_with == 'my':
        # TODO: discord user is not registered

        # TODO: embed message with:
        # - total problems solved
        # - total easy
        # - total medium
        # - total hard
        await ctx.message.channel.send('this command is still a massive wip lol')
    elif ctx.invoked_with == '+remove':
        user = ctx.message.author
        profilepic = user.avatar_url

        if not ctx.message.author.guild_permissions.administrator:
            desc = "Channel setting is an admin only permission."
            embed: Embed = discord.Embed(title="Permission Denied", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        if len(message) == 0:
            desc = "No username was given."
            embed: Embed = discord.Embed(title="User Not Found", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        # TODO: user not registered

        # TODO: remove user from db
        now = datetime.now()
        currentTime = now.strftime("%d-%m-%y %H:%M")

        desc = "User [" + message + "](https://leetcode.com/" + message + "/) successfully removed."

        embed: Embed = discord.Embed(title="Unsubscribed", description=desc, color=15442752)
        embed.set_footer(text=currentTime, icon_url=profilepic)

        await ctx.message.channel.send(embed=embed)
    elif ctx.invoked_with == '+set':
        if not ctx.message.author.guild_permissions.administrator:
            desc = "Channel setting is an admin only permission."
            embed: Embed = discord.Embed(title="Permission Denied", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        channels_list = ctx.message.channel_mentions

        for c in channels_list:
            if not c.type == discord.ChannelType.text:
                channels_list.remove(c)

        if len(channels_list) == 0:
            desc = "Please mention a valid channel in the server."
            embed: Embed = discord.Embed(title="Channel Not Found", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
        else:
            new_channel: TextChannel = ctx.message.channel_mentions[0]
            global channel
            channel = new_channel.id
            desc = "Channel successfully set to " + new_channel.mention + "."
            embed: Embed = discord.Embed(title="Channel Updated", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)


# TODO: auto scrape monkaS\
@tasks.loop(seconds=5)
async def sendmessage():
    # do nothing
    if channel != -1:
        # TODO: cycle thru everyone and print out any changes :cursed:
        await bot.get_channel(channel).send("hello")

sendmessage.start()


def connect(db_name, user_, password_, host_ip, port_):
    connection = None
    try:
        connection = sql.connect(
            database=db_name,
            user=user_,
            password=password_,
            host=host_ip,
            port=port_
        )
        print("Connection successful.")
    except OperationalError as e:
        print(f"Error '{e}' has occurred.")
    return connection


def query(connection, query_db):
    connection.autocommit = True

    try:
        connection.cursor().execute(query_db)
        print("Query executed.")
    except OperationalError as e:
        print(f"Error '{e}' has occurred.")


# Runs the bot given bot token ID
bot.run(BOT_TOKEN)
