import os
import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Configuration
BOT_TOKEN = "8688282898:AAGJR1kQ-2CPR29_QEC-LWmWkopEdqhFGBI"
MYID_LOGIN_URL = "http://mytelsupperapp.mytel.com.mm/ReengBackendBiz/mytel/api/checkTokenAuth/v2"

# States
ASK_PHONE, ASK_TOKEN = range(2)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MyID Automation Bot မှ ကြိုဆိုပါတယ်။\nစတင်ရန် /login ကို နှိပ်ပါ။")

async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MyID ဖုန်းနံပါတ် ရိုက်ထည့်ပါ (ဥပမာ - 09660377241)။")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("သင့် Generator ကရတဲ့ Token (သို့မဟုတ်) OTP ကို ရိုက်ထည့်ပေးပါ။")
    return ASK_TOKEN

async def ask_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_token = update.message.text
    phone = context.user_data['phone']
    
    await update.message.reply_text("Token ကို စစ်ဆေးပြီး Login ဝင်နေပါပြီ... ခဏစောင့်ပါ။")
    
    headers = {
        "Host": "mytelsupperapp.mytel.com.mm",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "okhttp/4.9.1"
    }
    
    # ပုံထဲကအတိုင်း Payload ပြင်ဆင်ခြင်း
    payload = {
        "clientType": "Android",
        "platform": "myid",
        "username": phone,
        "thirdPartyToken": user_token,  # User ပေးတဲ့ Token ကို ဒီမှာသုံးမယ်
        "revision": "16227"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(MYID_LOGIN_URL, headers=headers, data=payload, timeout=20.0)
            
            if response.status_code == 200:
                # Login အောင်မြင်ရင်
                await update.message.reply_text("✅ Login အောင်မြင်ပါပြီ။\nယခုမှစ၍

