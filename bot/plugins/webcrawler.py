import logging
import os
import sys
import subprocess
from config import config
from telegram.ext import Filters, MessageHandler, CommandHandler, CallbackContext
import re
from html import escape
import hashlib

# noinspection PyPackageRequirements
from typing import Optional

from telegram import Update, BotCommand, ParseMode, User, Bot
import bencoding

from bot.qbtinstance import qb
from bot.updater import updater
from utils import u
from utils import kb
from utils import Permissions

logger = logging.getLogger(__name__)

def notify_addition(current_chat_id: int, bot: Bot, user: User, torrent_description: str):
    if not config.notifications.added_torrents:
        return

    target_chat_id = config.notifications.added_torrents
    if target_chat_id != current_chat_id:  # do not send if the target chat is the current chat
        return

    text = f"User {escape(user.full_name)} [<code>{user.id}</code>] added a torrent: " \
           f"<code>{escape(torrent_description)}</code>"
    bot.send_message(
        target_chat_id,
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


def get_qbt_request_kwargs() -> dict:
    kwargs = dict()
    if config.qbittorrent.added_torrents_tag:
        # string with tags separated by ",", but since it's only one tehre's no need to join
        kwargs["tags"] = config.qbittorrent.added_torrents_tag
    if config.qbittorrent.added_torrents_category:
        kwargs["category"] = config.qbittorrent.added_torrents_category

    return kwargs
    
def call_qB_DownLoad(magnet_link):
    kwargs = get_qbt_request_kwargs()
    qb.download_from_link(magnet_link, **kwargs)
    # always returns an empty json:
    # https://python-qbittorrent.readthedocs.io/en/latest/modules/api.html#qbittorrent.client.Client.download_from_link
    try:
        torrent_hash = u.hash_from_magnet(magnet_link)
        logger.info('torrent hash from regex: %s', torrent_hash)
    except:
        print('torrent_hash/ logger.info出错了')
    update.message.reply_html(
        '磁力链接已添加',
        reply_markup=kb.short_markup(torrent_hash),
        quote=True
    )
    try:
        notify_addition(update.effective_chat.id, context.bot, update.effective_user, torrent_hash)
    except:
        print('notify_addition出错了')

def get_dytt():# 电影天堂
    if os.path.exists(f'downloads.json'): 
        print('下载缓存文件存在！')

    else:
        dl = {'下载链接':'电影名字'}
        with open(f'downloads.json', "w", encoding="utf-8") as k:
            json.dump(dl, k, indent=4)
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }
    url2 = f"https://www.dydytt.net/index2.htm"
    r = requests.get(url2,headers=head)
    r.encoding = 'gbk'
    et = etree.HTML(r.text)
    re = et.xpath('//div[@class="co_content2"]/ul')
    for mv_url in re:
        title = mv_url.xpath('./a/text()')
        url1 = mv_url.xpath('./a/@href')
        qb = {}
        for i in range(1,16):
            url = f'https://www.dydytt.net' + url1[i]
            #print(title[i],url)
            r = requests.get(url, headers=head)
            r.encoding = 'gbk'
            r=r.text
            rer = r[r.find(f'href="magnet') + 12:]
            dl = 'magnet'+rer[:rer.find(f'"')]
            name = r[r.find(f'磁力链') + 5:]
            name = name[:name.find(f'<')]
            qb[dl] = name
        break
    with open(f'downloads.json', encoding="utf-8") as g:
        dyhc = json.load(g)
    for i in qb:
        if i in dyhc:
            print('{qb[i]}已下载过,跳过')
        else:
            call_qB_DownLoad(i)
            with open(f'downloads.json', 'r+') as f:
                dl = json.load(f)
                dl[i] = qb[i] 
                f.seek(0)
                json.dump(dl, f, indent=4)
                f.truncate()

updater.add_handler(CommandHandler('qb', get_dytt), bot_command=BotCommand("qb", "爬取电影天堂15部电影"))
