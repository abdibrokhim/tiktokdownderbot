from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,

)

import os
import requests
import logging

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '5538417603:AAGny-20v6DK2bD77wPr5TJv8o1X48T5HZo'
VIDEO_FILE_PATH = 'video/video.mp4'
AUDIO_FILE_PATH = 'audio/audio.mp3'
CHANNEL_LINK = 'https://t.me/prmngr'
CHANNEL_USERNAME = '@prmngr'

_bots = """
???? Bizning Botlar:

    ???? @thesaver_bot
    ???? @insta_downder_bot
    ???? @usellbuybot
    ???? @musicfindmebot (yengi versiya)
    ???? @anonyiobot
    ???? @music_recognizerBot
    ???? @tiktokwatermark_removerBot
    ???? @tiktoknowater_bot (yengi versiya)
    
???? Contact: @abdibrokhim
???? Contact: @contactdevsbot

???? Channel: @prmngr

???? Developer: @abdibrokhim
"""

_ads = """
???? Biz bilan bog\'lanish uchun:

    ???? @contactdevsbot
    ???? @abdibrokhim
    
???? Bizning kanal: @prmngr
???? Reklama: @prmngr
???? Yangiliklar: @prmngr

???? Xullas hamma narsa shetda, krurasila ????: @prmngr
"""

(MAIN,
 TIKTOK,
 TIKTOK_REEL
 ) = range(3)


async def ads_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_ads)


async def bots_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_bots)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('???儭? Kanalga go', url=CHANNEL_LINK)]])

    await update.message.reply_text("Assalomu alaykum, {}!".format(user.first_name))
    await update.message.reply_text(
        "Botga xush kelibsiz\n\nBotdan foydalanish uchun /menu bosing\n\n漎?儭? Kanalimizga obuna bo'ling\n(zarari yo, atak)! 漎?儭?",
        reply_markup=reply_markup)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="???? TikTok", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "???? Pastda menu bor, xolaganizni tanlen\n\n???? Reklama /ads, ???? Botlar /bots",
        reply_markup=reply_markup)

    return MAIN


async def tiktok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="???? Video", ),
        ],
        [
            KeyboardButton(text="???? Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("漎?儭? TikTok videodan suv belgisini chopvoraman, bosing 漎?儭?",
                                    reply_markup=reply_markup)

    return TIKTOK


async def tiktok_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Link keree, davay...",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["????儭? Orqaga"]],
                                        resize_keyboard=True))
    return TIKTOK_REEL


async def tiktok_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await update.message.reply_text(text='???? Qidirvomman...')
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

        querystring = {"url": link, 'hd': '0'}

        headers = {
            "X-RapidAPI-Key": "6a90d6d4efmsh32f9758380f3589p11e571jsn642878f330b1",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        link = response.json()
        # print(link)
        link = link['data']['play']
        print(link)

        try:
            response = requests.get(link)
            with open(VIDEO_FILE_PATH, 'wb') as f:
                f.write(response.content)

            await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'), caption='\n@tiktoknowater_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='Link chopilgan')
    else:
        await update.message.reply_text(text='Link kereee, davay...')

    return TIKTOK


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Beknvoldm")
    await update.message.reply_text("Kere bob qosam be\'malol /start bosurasz, hop!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
        ],
        states={
            MAIN: [
                MessageHandler(filters.Regex(".*TikTok$"), tiktok_handler),
            ],
            TIKTOK: [
                MessageHandler(filters.Regex(".*Video$"), tiktok_reel_handler),
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            TIKTOK_REEL: [
                MessageHandler(filters.Regex(".*Orqaga$"), tiktok_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), tiktok_reel_link_handler)
            ],
        },
        fallbacks=[
            CommandHandler('end', cancel_handler),
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
            CommandHandler('tiktok', tiktok_handler),
            CommandHandler('ads', ads_handler),
            CommandHandler('bots', bots_handler),
        ],
    )
    app.add_handler(conv_handler)

    print("updated...")
    app.run_polling()
