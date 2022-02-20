from setup.keep_alive import keep_alive
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
import os
from discord.utils import get
from discord.ext import commands, tasks

from imports.commands import *

intents = discord.Intents.all()
bot = commands.Bot(intents = intents, command_prefix = '__')
slash = SlashCommand(bot, sync_commands=True)
# bot = commands.Bot('!')

params = {
	'bot': bot,
	'discord': discord,
	'slash': slash,
	'get': get,
	'tasks': tasks,
	'create_permission': create_permission,
	'SlashCommandPermissionType': SlashCommandPermissionType,
}

init_bot_commands(params)


keep_alive()
bot.run(os.getenv("token"))
