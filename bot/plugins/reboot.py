import logging
import os
import sys
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext

from bot.updater import updater

logger = logging.getLogger(__name__)


def reboot_bot(update: Update, context: CallbackContext):
    logger.info('/help from %s', update.message.from_user.first_name)

    update.message.reply_html('bot正在重启')
    python = sys.executable
    os.execl(python, python, "-u", *sys.argv)

updater.add_handler(CommandHandler('reboot', reboot_bot), bot_command=BotCommand("reboot", "重启bot"))