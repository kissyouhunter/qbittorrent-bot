from distutils.file_util import move_file
import logging
import subprocess

from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(__name__)

#subprocess.call(["bash", "./upload.sh"], shell=False)

def move_file_to_cloud(update: Update, context: CallbackContext):
    update.message.reply_text('this is a test python script!')

updater.add_handler(CommandHandler('move', move_file_to_cloud), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
