# TODO: do anything
import os
import yaml
import disnake
import logging
from sqlite4 import SQLite4
from disnake.ext import commands
from config import Config


def load_config():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\config.yml"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return Config(**config_data)
    else:
        logging.critical('Configuration does not exist. Exiting...')
        exit(-1)


config = load_config()

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.allow_command_deletion = True
command_sync_flags.sync_commands = True
bot = commands.Bot(command_prefix=config.Prefix, command_sync_flags=command_sync_flags,
                   intents=disnake.Intents.default() | disnake.Intents.message_content)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')
database = SQLite4("LiberaDB.db")
database.connect()

database.create_table("config", ["guildId", "categoryId", "createPartyVcId"])


@bot.event
async def on_ready():
    p = disnake.Activity(name=config.Presence['Name'], state=config.Presence['State'], type=config.Presence['Type'])
    await bot.change_presence(status=disnake.Status.online, activity=p)
    logging.info(f'Bot ready! Logged in as {bot.user.name}.')


@bot.event
async def on_voice_state_update(member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
    categories = database.select("config", columns=['guildId', 'createPartyVcId'],
                                 condition=f'guildId = {member.guild.id}')
    vcId = categories[0][1]
    if after.channel.id == vcId:
        categories = database.select("config", columns=['guildId', 'categoryId'],
                                     condition=f'guildId = {member.guild.id}')
        category = categories[0][1]
        vc = await member.guild.create_voice_channel(name=member.name + "'s Party",
                                                     category=member.guild.get_channel(category))
        await vc.send(f"{member.mention} Here you go!")
        await member.move_to(vc, reason='Created party VC')


# TODO: Write help command
@bot.slash_command(name='help', description='Command Explanation')
async def help_slash(inr: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(title="Command Explanation", color=, description='''
    /help \- Command usage and explanation
    \n/about - Gives information about the bot
    \n/ping - Checks the bots latency
    \n/configure - ADMIN USE ONLY enable/disable bot features
    \n/create - Creates a temporary voice channel
    ''')
    await inr.send(embed=embed)
    logging.info('nothing')


@bot.slash_command(name='ping', description='Ping')
async def ping_slash(inr: disnake.ApplicationCommandInteraction):
    await inr.response.send_message(f'Pong! Latency is {(bot.latency * 1000).__round__(2)}s!')


@bot.command(name='ping')
async def ping_prefix(inr: disnake.CommandInteraction):
    await inr.send(f'Pong! Latency is {(bot.latency * 1000).__round__(2)}s!', reference=inr.message,
                   allowed_mentions=disnake.AllowedMentions.none())


@bot.slash_command(name='configure', description='Configure the bot')
async def conf_slash(inr: disnake.ApplicationCommandInteraction, category: disnake.CategoryChannel):
    vc = await category.create_voice_channel(name='Create a Party')
    database.insert("config", {"guildId": inr.guild_id, "categoryId": category.id, "createPartyVcId": vc.id})
    await inr.response.send_message('<:done:1189216626604769320> Done and Done!')


# TODO: Create control panel text channel
@bot.slash_command(name='create', description='Create a party VC')
async def create_party(inr: disnake.ApplicationCommandInteraction, display_name: str):
    await inr.response.send_message(
        '<:pending:1189216631268843530> Creating a party VC...\n<:desc:1189216629519826975> Administrators or people '
        'that have the `ADMINISTRATOR` permission can see party VCs, regardless of its privacy level!')
    categories = database.select("config", columns=['guildId', 'categoryId'], condition=f'guildId = {inr.guild_id}')
    category = categories[0][1]
    vc = await inr.guild.create_voice_channel(name=display_name + ' (Party)', category=inr.guild.get_channel(category))
    await inr.edit_original_message('<:done:1189216626604769320> Done!')


@bot.slash_command(name='about', description='About Liberation')
async def about(inr: disnake.ApplicationCommandInteraction):
    libera = disnake.Embed()
    libera.set_image(url='https://cdn.discordapp.com/attachments/1190294730358145024/1190305545446498355' +
                         '/Liberation_BannerU.png')
    embed = disnake.Embed(title='Liberation', description='Liberation is a bot that you can use to effortlessly '
                                                          'create temporary VCs.')
    embed.add_field('Developers', '**jbcarreon123**\n**Gowthr**', inline=True)
    embed.add_field('Links', 'GitHub: ', inline=True)
    await inr.response.send_message(embeds=[libera, embed])


@bot.command(name='gowthr')
async def ee1(inr: disnake.CommandInteraction):
    await inr.send('gowthr was here...', reference=inr.message, allowed_mentions=disnake.AllowedMentions.none())


@bot.command(name='krunged')
async def ee2(inr: disnake.CommandInteraction):
    await inr.send('GET A JUICY CHICKEN SANDWICH TODAY 50% OFF IF YOU USE CODE \"KRUNGED!\"\\* \n\n\\* *Deal has '
                   'expired*', reference=inr.message, allowed_mentions=disnake.AllowedMentions.none())


bot.run(config.Token)
