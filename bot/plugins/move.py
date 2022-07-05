import logging
import os
import subprocess

from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(__name__)

def move_file_to_cloud(update: Update, context: CallbackContext):
    #subprocess.call(["bash", "./move.sh"], shell=False)
    os.system('/bin/bash -c "bash /app/bot/plugins/move.sh"')

    update.message.reply_text('shell脚本执行完毕')

updater.add_handler(CommandHandler('move', move_file_to_cloud), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
