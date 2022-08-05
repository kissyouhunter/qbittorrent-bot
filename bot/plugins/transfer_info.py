import logging

# noinspection PyPackageRequirements
from telegram import Update, BotCommand, ParseMode
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from bot.updater import updater
from bot.qbtinstance import qb
from utils import Permissions
from utils import u
from utils import kb

logger = logging.getLogger(__name__)


TEXT = """<b>当前速度</b>
▲ {current_upload_speed}/s
▼ {current_download_speed}/s

<b>全局速度限制</b>
▲ {global_up_limit}
▼ {global_down_limit}

<b>备用速度限制</b>
• alt speed: {alt_speed_status}
▲ {alt_speed_down}
▼ {alt_speed_up}

<b>上传/下载的总流量</b>
▲ {session_total_upload}
▼ {session_total_download}
• 分享率: {session_share_rateo}

<b>列队状态</b>
• 最大活动数: 下载 {queueing_max_active_downloads}, 上传 {queueing_max_active_uploads}, \
全部 {queueing_max_active_torrents}
• 慢速任务是否计入限制内? {queueing_count_slow_torrents}
• 下载速度阈值: {queueing_slow_torrent_down_threshold} kb/s
• 上传速度阈值: {queueing_slow_torrent_up_threshold} kb/s

<b>做种限制</b>
• 当分享率达到后停止或删除任务? {max_ratio_enabled} (max rateo: {max_ratio})
• 当做种时间到后停止或删除任务? {max_seeding_time_enabled} (时间: {max_seeding_time} 分钟, \
停止或删除任务)"""


def get_speed_text():
    fdict = {}

    transfer_info = qb.global_transfer_info
    fdict['current_download_speed'] = u.get_human_readable(transfer_info['dl_info_speed'])
    fdict['current_upload_speed'] = u.get_human_readable(transfer_info['up_info_speed'])

    fdict['session_total_upload'] = u.get_human_readable(transfer_info['up_info_data'])
    fdict['session_total_download'] = u.get_human_readable(transfer_info['dl_info_data'])
    if transfer_info['dl_info_data'] > 0:
        fdict['session_share_rateo'] = round(transfer_info['up_info_data']/transfer_info['dl_info_data'], 2)
    else:
        fdict['session_share_rateo'] = 0

    preferences = qb.preferences()

    fdict['global_down_limit'] = u.get_human_readable(preferences['dl_limit']) if preferences['dl_limit'] else 'none'
    fdict['global_up_limit'] = u.get_human_readable(preferences['up_limit']) if preferences['up_limit'] else 'none'

    fdict['alt_speed_status'] = 'on' if qb.get_alternative_speed_status() else 'off'
    fdict['alt_speed_down'] = u.get_human_readable(preferences['alt_dl_limit'], 0) if preferences[
                                                                                          'alt_dl_limit'] > -1 else 'none'
    fdict['alt_speed_up'] = u.get_human_readable(preferences['alt_up_limit'], 0) if preferences[
                                                                                        'alt_up_limit'] > -1 else 'none'

    fdict['queueing_max_active_downloads'] = preferences['max_active_downloads']
    fdict['queueing_max_active_uploads'] = preferences['max_active_uploads']
    fdict['queueing_max_active_torrents'] = preferences['max_active_torrents']
    fdict['queueing_count_slow_torrents'] = 'no' if preferences['dont_count_slow_torrents'] else 'yes'
    fdict['queueing_slow_torrent_down_threshold'] = preferences['slow_torrent_dl_rate_threshold']
    fdict['queueing_slow_torrent_up_threshold'] = preferences['slow_torrent_ul_rate_threshold']
    fdict['queueing_slow_torrent_inactive_timer'] = preferences['slow_torrent_inactive_timer']

    fdict['max_ratio_enabled'] = "yes" if preferences['max_ratio_enabled'] else "no"
    fdict['max_ratio'] = preferences['max_ratio']
    fdict['max_seeding_time_enabled'] = "yes" if preferences['max_seeding_time_enabled'] else "no"
    fdict['max_seeding_time'] = preferences['max_seeding_time']
    fdict['max_ratio_act'] = "pause" if preferences['max_ratio_act'] == 0 else "remove"  # 0 = pause them, 1 = remove them

    return TEXT.format(**fdict)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
def on_speed_command(update: Update, context: CallbackContext):
    logger.info('/transferinfo from %s', update.effective_user.first_name)

    text = get_speed_text()

    update.message.reply_html(text, reply_markup=kb.REFRESH_TRANSFER_INFO)


@u.check_permissions(required_permission=Permissions.READ)
@u.failwithmessage
@u.ignore_not_modified_exception
def on_refresh_button_speed(update: Update, context: CallbackContext):
    logger.info('transfer info: refresh button')

    text = get_speed_text()

    update.callback_query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=kb.REFRESH_TRANSFER_INFO
    )
    update.callback_query.answer('已刷新')


updater.add_handler(CommandHandler(['transferinfo', 'ti', 'speed'], on_speed_command), bot_command=BotCommand("transferinfo", "显示当前速度、列队状态、做种设置"))
updater.add_handler(CallbackQueryHandler(on_refresh_button_speed, pattern=r'^refreshtransferinfo$'))
