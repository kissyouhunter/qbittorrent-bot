from distutils.file_util import move_file
import logging
import subprocess

from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

#subprocess.call(["bash", "./upload.sh"], shell=False)

print('this is a test python script!')

updater.add_handler(CommandHandler('move', move_file), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
