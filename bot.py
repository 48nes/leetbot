####################
import os

# Obtain bot token from Discord Developer Site
import discord
from discord import Embed, User, Member, TextChannel
from discord.ext import commands, tasks
from discord.ext.commands import Context
from datetime import datetime
import requests

# PostgreSQL file
import tables
from tables import *
from leetmodel import *

####################
BOT_TOKEN = os.getenv("BOT_TOKEN")
# ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")

username = "urmom12345"
password = "urmom12345"
model = leetmodel(username, password)

# Creates the instances, uses "+" to activate commands
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='+', intents=intents)

bot.remove_command('help')

# channel configuration
channel = -1


# bot commands
@bot.command(aliases=['help', 'add', 'remove', 'top', 'my', '+remove', '+set', '+stop'])
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

        user = ctx.message.author
        profilepic = user.avatar_url

        maybeLeetcode = check_discord(user.id)

        if maybeLeetcode != "":
            registered_username = ''.join(maybeLeetcode)
            desc = "You are already registered under [" + registered_username + "](https://leetcode.com/" \
                   + registered_username + "/)."
            embed: Embed = discord.Embed(title="Already Registered", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        if check_leetcode(message) != "":
            desc = "Username [" + message + "](https://leetcode.com/" + message + "/) is already registered."
            embed: Embed = discord.Embed(title="Already Registered", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        request = requests.get('http://leetcode.com/' + message + '/')
        # user exists on leetcode
        if request.status_code == 200:

            userData = model.getUserData(message)

            total = userData['submitStats']['acSubmissionNum'][0]['count']
            easy = userData['submitStats']['acSubmissionNum'][1]['count']
            medium = userData['submitStats']['acSubmissionNum'][2]['count']
            hard = userData['submitStats']['acSubmissionNum'][3]['count']

            total_subs = userData['submitStats']['acSubmissionNum'][0]['submissions']

            insert_into_table(user.id, message, total, easy, medium, hard, total_subs)

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
        leetcode_username = ''.join(check_discord(user.id))

        if check_discord(user.id) == "":
            desc = "You do not have an account."
            embed: Embed = discord.Embed(title="Nothing to Remove", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        remove_from_table(user.id)

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
        await ctx.message.channel.send('Command is still WIP')
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

        if not check_leetcode(message):
            desc = "Account is not registered."
            embed: Embed = discord.Embed(title="Nothing to Remove", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        remove_by_leetcode(message)

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
    elif ctx.invoked_with == '+stop':
        if not ctx.message.author.guild_permissions.administrator:
            desc = "Channel setting is an admin only permission."
            embed: Embed = discord.Embed(title="Permission Denied", description=desc, color=15442752)

            await ctx.message.channel.send(embed=embed)
            return

        channel = -1
        desc = "Notifications successfully disabled."
        embed: Embed = discord.Embed(title="Feed Disabled", description=desc, color=15442752)

        await ctx.message.channel.send(embed=embed)


@tasks.loop(seconds=30)
async def send_message():
    rows = select_all()
    new_submissions = []
    for row in rows:
        leetcode_user = ''.join(row[0])
        prev_total = int(row[1])
        userData = model.getUserData(leetcode_user)

        current_total = userData['submitStats']['acSubmissionNum'][0]['submissions']
        print(current_total)
        print(prev_total)

        if current_total > prev_total:
            userSubs = model.getRecentSubs(leetcode_user)
            num_new_submissions = current_total - prev_total
            for x in range(num_new_submissions):
                new_submissions.insert(0, [leetcode_user, userSubs[x]['title'], userSubs[x]['lang'],
                                           userSubs[x]['titleSlug'], userSubs[x]['statusDisplay']])
        total = userData['submitStats']['acSubmissionNum'][0]['count']
        easy = userData['submitStats']['acSubmissionNum'][1]['count']
        medium = userData['submitStats']['acSubmissionNum'][2]['count']
        hard = userData['submitStats']['acSubmissionNum'][3]['count']

        update_table(leetcode_user, total, easy, medium, hard, current_total)

    if channel != -1:
        for submission in new_submissions:
            desc = "" + ''.join(submission[0]) + " has submitted an answer for [" + ''.join(submission[1]) \
                   + "](https://leetcode.com/problems/" + ''.join(submission[3]) \
                   + ") in " + ''.join(submission[2]) + "."

            status = ''.join(submission[4])            
            print(status)
            if status == "Accepted":
                embed: Embed = discord.Embed(title="Accepted", description=desc, color=5025616)
            else:
                embed: Embed = discord.Embed(title=status, description=desc, color=15277667)
            await bot.get_channel(channel).send(embed=embed)
    

send_message.start()

# Runs the bot given bot token ID
bot.run(BOT_TOKEN)
