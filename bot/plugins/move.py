import sys
sys.path.append('/app/bot/plugins')
import logging
import os
import subprocess

from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(__name__)

#subprocess.call(["bash", "./upload.sh"], shell=False)

def move_file_to_cloud(update: Update, context: CallbackContext):
    update.message.reply_text('this is a test msg!')
    
    file_name = '/app/bot/plugins/move.sh'

    #os.system('/bin/bash -c "bash /app/bot/plugins/move.sh"')

    subprocess.call(["bash", "/app/bot/plugins/move.sh"], shell=False)

    #update.subprocess.call(['bash', '/app/bot/plugins/move.sh'], shell=False)

updater.add_handler(CommandHandler('move', move_file_to_cloud), bot_command=BotCommand("move", "移动文件或文件夹到网盘"))
