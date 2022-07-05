import logging
import os
import subprocess

from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(move)

def move_file_to_cloud(update: Update, context: CallbackContext):
    logger.info('executing move shell script')

    subprocess.call(["bash", "bot/plugins/move.sh"], shell=False)

    update.message.reply_text('shell脚本执行完毕')

updater.add_handler(CommandHandler('move', move_file_to_cloud), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
