# TODO: do anything

import disnake
import logging
from sqlite4 import SQLite4
from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.allow_command_deletion = True
command_sync_flags.sync_commands = True
bot = commands.Bot(command_prefix='*', command_sync_flags=command_sync_flags, intents=disnake.Intents.default() | disnake.Intents.message_content)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
database = SQLite4("LiberaDB.db")
database.connect()

database.create_table("config", ["guildId", "categoryId"])

@bot.event
async def on_ready():
    logging.info(f'Bot ready! Logged in as {bot.user.name}.')

#TODO Write help command
@bot.slash_command(name='help',  description='Command usage and explanation')
async def help_slash(inr: disnake.ApplicationCommandInteraction):
    await inr.response.send_message(f'~~~')
    logging.info('nothing')


@bot.slash_command(name='ping', description='Ping')
async def ping_slash(inr: disnake.ApplicationCommandInteraction):
    await inr.response.send_message(f'Pong! Latency is {(bot.latency*1000).__round__(2)}s!')


@bot.command(name='ping')
async def ping_prefix(inr: disnake.CommandInteraction):
    await inr.send(f'Pong! Latency is {(bot.latency*1000).__round__(2)}s!', reference=inr.message, allowed_mentions=disnake.AllowedMentions.none())


@bot.slash_command(name='configure', description='Configure the bot')
async def conf_slash(inr: disnake.ApplicationCommandInteraction, category: disnake.CategoryChannel):
    database.insert("config", {"guildId": inr.guild_id, "categoryId": category.id})
    await inr.response.send_message('<:done:1189216626604769320> Done!')


#TODO Add category to create_voice_channel
#Create control panel text channel
@bot.slash_command(name='create', description='Create a party VC')
async def create_party(inr: disnake.ApplicationCommandInteraction, display_name: str):
    await inr.response.send_message('<:pending:1189216631268843530> Creating a party VC...\n<:desc:1189216629519826975> Administrators or people that have the `ADMINISTRATOR` permission can see party VCs, regardless of its privacy level!')
    categories = database.select("config", columns=['guildId', 'categoryId'], condition=f'guildId = {inr.guild_id}')
    category = categories[0][1]
    await inr.guild.create_voice_channel(name=display_name + ' (Party)', category=inr.guild.get_channel(category))
    await inr.guild.create_voice_channel(name=display_name + ' (Party)', category=inr.guild.get_channel(category))
    await inr.edit_original_message('<:done:1189216626604769320> Done!')


@bot.command(name='gowthr')
async def ee1(inr: disnake.CommandInteraction):
 await inr.send('gowthr was here...', reference=inr.message, allowed_mentions=disnake.AllowedMentions.none())


@bot.command(name='krunged')
async def ee2(inr: disnake.CommandInteraction):
 await inr.send('GET A JUICY CHICKEN SANDWICH TODAY 50% OFF IF YOU USE CODE \"KRUNGED!\" \n\n*Deal has expired*', reference=inr.message, allowed_mentions=disnake.AllowedMentions.none())


bot.run('[BOT TOKEN HERE]')
