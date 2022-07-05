import logging
import os
import subprocess
from config import config
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(__name__)
od_name = config.rclone.name
up_path = config.rclone.up_path
source = '/Downloads'


def move_file_to_cloud(update: Update, context: CallbackContext):
    cmd = 'rclone moveto -v -P \"{}\" \"{}\":\"{}\"'.format(source, od_name, up_path)

    os.system(cmd)

    update.message.reply_text('上传完毕')


updater.add_handler(CommandHandler('move', move_file_to_cloud), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
