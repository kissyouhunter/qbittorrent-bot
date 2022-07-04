import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters

from bot.updater import updater
from utils import u
from utils import Permissions

logger = logging.getLogger(__name__)


HELP_MESSAGE = """<b>Commands</b>:

<i>READ commands</i>
• /start or /help: 显示帮助信息
• /available_filters: 显示命令列表（通过不同状态显示种子）
• /overview: 显示下载/上传的种子的状态
• /filter or /f <code>[substring]</code>: filter by substring (filters from the full list)
• /settings or /s: 显示目前设置列表
• /transferinfo: 显示目前的速度、排队情况和分享率
• /atm: 显示目前自动种子管理设置
• /atmyes or /atmno: 列出 是/否 在自动种子管理中
• /json: 输出所有的种子到json文件
• /version: 获取qbittorrent和API的版本

<i>WRITE commands</i>
• <code>.torrent</code> document: add torrent by file
• magnet url: add a torrent by magnet url

<i>EDIT commands</i>
• /altdown: change the alternative max download speed from a keyboard
• /altdown <code>[kb/s]</code>: change the alternative max download speed
• /altup <code>[kb/s]</code>: change the alternative max upload speed
• /pauseall: pause all torrents
• /resumeall: resume all torrents
• /set <code>[setting] [new value]</code>: change a setting
• <code>+tag</code> or <code>-tag</code>: reply to a torrent info message with "<code>+some tags</code>" or \
"<code>-some tags</code>" to add/remove tags. Multiple tags can be passed, separated by a comma \
(tags can have white spaces)

<i>ADMIN commands</i>
• /permissions: get the current permissions configuration
• /pset <code>[key] [val]</code>: change the value of a permission key
• /freespace: get the current free space from qbittorrent's download drive

<i>FREE commands</i>
• /rmkb: remove the keyboard, if any"""


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_help(update: Update, context: CallbackContext):
    logger.info('/help from %s', update.message.from_user.first_name)

    update.message.reply_html(HELP_MESSAGE)


updater.add_handler(CommandHandler('help', on_help), bot_command=BotCommand("help", "show the help message"))
updater.add_handler(MessageHandler(Filters.regex(r'^\/start$'), on_help))
