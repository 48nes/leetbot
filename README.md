# LeetBot

LeetBot is a Discord bot that scrapes Leetcode user profiles and updates progress in real time. It is currently made to be self-hosted, see the [setup section below](https://github.com/48nes/leetbot#how-to-host) for how to host.

## About

LeetBot is written entirely in Python and uses PostgreSQL for database management. The API we used can be found in [this repo](https://github.com/ashdawngary/Leetcode-userapi). 

### Credits

- [Agnes Shan](https://github.com/48nes)
- [Rixuan Zheng](https://github.com/rixuanzheng)
- [Neel Bhalla](https://github.com/ashdawngary)

## Commands and Features

LeetBot's main feature is a live feed of all users' recent Leetcode submissions. The bot is currently set up to check for new submissions every 30 seconds, although this can be adjusted in `bot.py`.

<img src="https://i.imgur.com/Kgg26uK.png" alt="image of the live feed" width="300"/>

The command prefix for LeetBot is currently set to `+`. Below are a list of commands and what the bot will show when executed.

`+help` lists out all current bot commands:

<img src="https://i.imgur.com/7JVLVtY.png" alt="image of the help command" width="300"/>

`+add [username]` allows users to link their Leetcode account to the bot if they do not already have an account linked and if the account given is a valid account

<img src="https://i.imgur.com/yOeyjuy.png" alt="image of user being linked" width="300"/>

`+remove` allows users to unlink their Leetcode account from the bot

<img src="https://i.imgur.com/wdhih3r.png" alt="image of user being unlinked" width="300"/>

`+top`, `+top easy`, `+top medium`, `+top hard` showcases the top ten users in terms of accepted solutions for all problems, only easy problems, only medium problems, and only hard problems

![image of leaderboards](https://i.imgur.com/lpyBcHY.png)

`+my` showcases a user's own stats

<img src="https://i.imgur.com/4sqvdzw.png" alt="image of user's stats" width="300"/>

#### Admin Only Commands

Admin only commands have a command prefix of `++`.

`++remove [username]` will remove a user from the database

<img src="https://i.imgur.com/VCBHjCX.png" alt="image of user being removed" width="300"/>

`++set [channel]` sets the channel for messages to be sent to

<img src="https://i.imgur.com/qT39Epx.png" alt="image of channel being set" width="300"/>

`++stop` will stop the live feed 

<img src="https://i.imgur.com/K90O3ga.png" alt="image of feed being stopped" width="300"/>

## How to Host

Currently, we use [Heroku](https://dashboard.heroku.com/) to run our version of the bot, but any alternative should work as well. This how-to will go over setting up using Heroku.

#### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application
2. In the Build a Bot tab, create a new bot. Where it says `TOKEN`, click copy to get the bot token and save this somewhere.
3. Go to the OAuth2 tab. Under Scopes, choose bot and under Bot Permissions choose Administrator. Copy the URL given under the Scopes section, you can now use this URL to add the bot to your servers.

#### Leetcode Setup

1. Create a dummy account on [Leetcode](https://leetcode.com/) with the same username and password. Save this somewhere.

#### Heroku Setup

1. Fork this repo.
2. Log into [Heroku](https://dashboard.heroku.com/) using your Github account
3. Create a new application by clicking on New and then App
4. In Deploy, set Deployment method to Github and choose the forked repository
5. Under Automatic deploys, enable automatic deploys
6. Go back up to Settings. Under Config Vars, click reveal and add the bot token generated from Discord with `BOT_TOKEN` as the key and the bot token as the value.
7. Add another config var with `ACCOUNT_KEY` as the key and the username/password for your dummy account as the value. 
8. Go back up to Resources. Under Dynos, select worker.
9. Go to [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql) and click Install. Add the database to the Heroku app.
10. The database should now be viewable from the Overview tab, click on the database
11. Go to the Settings tab for the database and View Credentials, save this information somewhere

#### PostgreSQL Setup

1. Download [PostgreSQL](https://www.postgresql.org/download/) locally
2. Launch SQL Shell
3. Follow prompts and enter in the data given from the last step on the Heroku setup
4. Paste the following code into command prompt

```sql
CREATE TABLE IF NOT EXISTS users (
            discord_id BIGINT PRIMARY KEY,
            leetcode_username TEXT NOT NULL,
            num_total INTEGER NOT NULL,
            num_easy INTEGER NOT NULL,
            num_medium INTEGER NOT NULL,
            num_hard INTEGER NOT NULL,
            total_subs INTEGER NOT NULL
        );
```

After following these steps, the bot should run!
