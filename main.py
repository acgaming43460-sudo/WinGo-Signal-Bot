import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError, Forbidden, BadRequest

# ================= CONFIGURATION =================
BOT_TOKEN = os.environ.get('BOT_TOKEN') # Render se aayega
BOT_USERNAME = "@PrimeSignalZzzBot"
CHANNEL_ID = "@primesignalzzzofficial"
ADMIN_IDS = [8986058067]

BOT_NAME = "WinGo Signal"
VERSION = "5.1 Fixed"
# ================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_sessions = {}

class PredictionSession:
    def __init__(self):
        self.color = None
        self.number = None
        self.size = None
        self.timeframe = None

    def is_complete(self) -> bool:
        return all([self.color, self.number, self.size, self.timeframe])

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def get_color_emoji(color: str) -> str:
    return {"Green": "🟢", "Red": "🔴", "Violet": "🟣"}.get(color, "⚪")

def format_wingo_message(data: dict) -> str:
    """Tere diye hue format me exact message"""
    return (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        " 🚀 WINGO SIGNAL 🚀\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 SIGNAL DETAILS\n\n"
        f"{get_color_emoji(data['color'])} COLOR ➜ {data['color'].upper()}\n"
        f"🔢 NUMBER ➜ {data['number']}\n"
        f"📊 SIZE ➜ {data['size'].upper()}\n"
        f"⏳ PERIOD ➜ {data['timeframe']}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🕒 {datetime.now().strftime('%I:%M:%S %p')}\n"
        f"📅 {datetime.now().strftime('%d/%m/%Y')}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ Precision Entry\n"
        "🎯 Stay Disciplined\n"
        "🍀 Good Luck\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        " ⚡ WinGo Signal ⚡\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("⛔ Access Denied")
        return

    user_sessions[user_id] = PredictionSession()

    keyboard = [[
        InlineKeyboardButton("🟢 GREEN", callback_data="col_Green"),
        InlineKeyboardButton("🔴 RED", callback_data="col_Red"),
        InlineKeyboardButton("🟣 VIOLET", callback_data="col_Violet")
    ]]

    await update.message.reply_text(
        "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
        " ⚡ START WINGO ⚡\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "🎯 <b>STEP 1/4 ➜ SELECT COLOR</b>\n\n"
        "Choose signal color:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if not is_admin(user_id):
        await query.answer("Access Denied", show_alert=True)
        return

    await query.answer()

    if user_id not in user_sessions:
        user_sessions[user_id] = PredictionSession()

    session = user_sessions[user_id]

    try:
        if data.startswith("col_"):
            session.color = data.split("_")[1]
            keyboard = [
                [InlineKeyboardButton("0", callback_data="num_0"),
                 InlineKeyboardButton("1", callback_data="num_1"),
                 InlineKeyboardButton("2", callback_data="num_2"),
                 InlineKeyboardButton("3", callback_data="num_3"),
                 InlineKeyboardButton("4", callback_data="num_4")],
                [InlineKeyboardButton("5", callback_data="num_5"),
                 InlineKeyboardButton("6", callback_data="num_6"),
                 InlineKeyboardButton("7", callback_data="num_7"),
                 InlineKeyboardButton("8", callback_data="num_8"),
                 InlineKeyboardButton("9", callback_data="num_9")]
            ]
            await query.edit_message_text(
                "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
                " 🎯 STEP 2/4 ➜ NUMBER\n"
                "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                f"{get_color_emoji(session.color)} Color: <b>{session.color}</b>\n\n"
                "Select number:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.HTML
            )

        elif data.startswith("num_"):
            session.number = data.split("_")[1]
            keyboard = [[
                InlineKeyboardButton("📈 BIG", callback_data="size_Big"),
                InlineKeyboardButton("📉 SMALL", callback_data="size_Small")
            ]]
            await query.edit_message_text(
                "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
                " 🎯 STEP 3/4 ➜ SIZE\n"
                "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                f"{get_color_emoji(session.color)} Color: <b>{session.color}</b>\n"
                f"🔢 Number: <b>{session.number}</b>\n\n"
                "Select size:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.HTML
            )

        elif data.startswith("size_"):
            session.size = data.split("_")[1]
            keyboard = [[
                InlineKeyboardButton("30 SEC", callback_data="time_30sec"),
                InlineKeyboardButton("3 MIN", callback_data="time_3min"),
                InlineKeyboardButton("5 MIN", callback_data="time_5min")
            ]]
            await query.edit_message_text(
                "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
                " 🎯 STEP 4/4 ➜ PERIOD\n"
                "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                f"{get_color_emoji(session.color)} Color: <b>{session.color}</b>\n"
                f"🔢 Number: <b>{session.number}</b>\n"
                f"📊 Size: <b>{session.size}</b>\n\n"
                "Select period:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.HTML
            )

        elif data.startswith("time_"):
            session.timeframe = data.split("_")[1].upper().replace("SEC", " SEC").replace("MIN", " MIN")

            if not session.is_complete():
                await query.edit_message_text("❌ Incomplete")
                return

            msg_text = format_wingo_message({
                'color': session.color,
                'number': session.number,
                'size': session.size,
                'timeframe': session.timeframe
            })

            try:
                sent = await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=msg_text,
                    parse_mode=ParseMode.HTML
                )

                keyboard = [[InlineKeyboardButton("⚡ NEW SIGNAL ⚡", callback_data="new_signal")]]

                await query.edit_message_text(
                    "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
                    " ✅ SIGNAL SENT ✅\n"
                    "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                    f"📤 Channel: <code>{CHANNEL_ID}</code>\n"
                    f"🆔 ID: <code>{sent.message_id}</code>\n"
                    f"⚡ Time: {datetime.now().strftime('%I:%M:%S %p')}\n\n"
                    f"Press below for next signal 👇",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=ParseMode.HTML
                )
                user_sessions.pop(user_id, None)

            except Forbidden:
                await query.edit_message_text(
                    "❌ <b>BROADCAST FAILED</b>\n\n"
                    f"Bot not admin in {CHANNEL_ID}"
                )
            except BadRequest as e:
                await query.edit_message_text(f"❌ Error: {str(e)}")

        elif data == "new_signal":
            user_sessions[user_id] = PredictionSession()
            keyboard = [[
                InlineKeyboardButton("🟢 GREEN", callback_data="col_Green"),
                InlineKeyboardButton("🔴 RED", callback_data="col_Red"),
                InlineKeyboardButton("🟣 VIOLET", callback_data="col_Violet")
            ]]
            await query.edit_message_text(
                "╭━━━━━━━━━━━━━━━━━━━━━━╮\n"
                " ⚡ START WINGO ⚡\n"
                "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
                "🎯 <b>STEP 1/4 ➜ SELECT COLOR</b>\n\n"
                "Choose signal color:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.HTML
            )

    except Exception as e:
        logger.exception(f"Error: {e}")
        await query.edit_message_text(f"⚠️ Error occurred")

# ===== RENDER KEEPALIVE - PORT 8080 =====
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return f"{BOT_NAME} v{VERSION} - Online ✅"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()
# ========================================

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    logger.info(f"{BOT_NAME} v{VERSION} - Ready")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
