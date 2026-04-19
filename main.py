import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, ContextTypes, MessageHandler, filters

# --- Configuration ---
BOT_TOKEN = "8688282898:AAGJR1kQ-2CPR29_QEC-LWmWkopEdqhFGBI" 
GAME_BASE_URL = "http://fishmya.ugame.vn/"

# States
ASK_PHONE, ASK_PASSWORD, LOGGED_IN = range(3)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MyID Game Bot မှ ကြိုဆိုပါတယ်။\nLogin ဝင်ရန် /login ကို နှိပ်ပါ။")
    return ConversationHandler.END

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MyID ဖုန်းနံပါတ် ရိုက်ပါ။", reply_markup=ReplyKeyboardRemove())
    return ASK_PHONE

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text.strip()
    await update.message.reply_text("Password ရိုက်ပါ။")
    return ASK_PASSWORD

async def do_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_url = f"{GAME_BASE_URL}?uuid=demo&mcuid=demo&mcapp=myid"
    kb = [[InlineKeyboardButton("Play Game 🎮", web_app=WebAppInfo(url=game_url))]]
    await update.message.reply_text("Login အောင်မြင်ပါတယ်။", reply_markup=InlineKeyboardMarkup(kb))
    return LOGGED_IN

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("login", login_start)],
        states={
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_password)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_login)],
            LOGGED_IN: [MessageHandler(filters.ALL, login_start)]
        },
        fallbacks=[CommandHandler("start", start)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()

