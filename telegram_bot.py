import os
import json
import logging
import requests
from datetime import datetime, time, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, ConversationHandler
from telegram.constants import ChatAction
import asyncio

# Logging sozlamalarini o'rnatish
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenini o'rnating
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8517360815:AAEchs0SAX-axPg5oo8rko3GCtSCCcjnB2M')

# Foydalanuvchi ma'lumotlarini saqlash (JSON fayldagi)
USER_DATA_FILE = 'user_data.json'

# Namoz vaqtlari
PRAYER_NAMES = {
    'Bomdod': 'Fajr',
    'Peshin': 'Dhuhr',
    'Asr': 'Asr',
    'Shom': 'Maghrib',
    'Xufton': 'Isha'
}

# Conversation handler states
LOCATION_STATE = 1

# Foydalanuvchi ma'lumotlarini yuklash
def load_user_data():
    """Foydalanuvchi ma'lumotlarini JSON fayldan yuklash"""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Foydalanuvchi ma'lumotlarini saqlash
def save_user_data(data):
    """Foydalanuvchi ma'lumotlarini JSON faylga saqlash"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Lokatsiya bo'yicha namoz vaqtlarini olish
async def get_prayer_times(latitude, longitude):
    """API orqali namoz vaqtlarini olish"""
    try:
        # Aladhan API dan foydalanish
        url = f"https://api.aladhan.com/v1/timings/{int(datetime.now().timestamp())}"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'method': 4  # Makkah (Saudi Arabia) - O'zbekiston uchun to'g'ri
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['code'] == 200:
            timings = data['data']['timings']
            return {
                'Bomdod': timings['Fajr'],
                'Peshin': timings['Dhuhr'],
                'Asr': timings['Asr'],
                'Shom': timings['Maghrib'],
                'Xufton': timings['Isha']
            }
    except Exception as e:
        logger.error(f"Namoz vaqtlarini olishda xato: {e}")
    
    return None

# Reverse Geocoding - Koordinatalardan hudud nomini olish
async def get_location_name(latitude, longitude):
    """Koordinatalardan hudud nomini olish (shahar, viloyat)"""
    try:
        # OpenStreetMap Nominatim API dan foydalanish
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'zoom': 10,
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'PrayerTimesBot/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'address' in data:
            address = data['address']
            # Hudud nomini qurish
            city = address.get('city', address.get('town', address.get('village', '')))
            state = address.get('state', '')
            country = address.get('country', '')
            
            # Husnudan so'ng foydalanuvchiga taqdim etish
            location_parts = []
            if city:
                location_parts.append(city)
            if state:
                location_parts.append(state)
            if country:
                location_parts.append(country)
            
            location_name = ', '.join(location_parts) if location_parts else f"{latitude:.4f}, {longitude:.4f}"
            return location_name
    except Exception as e:
        logger.error(f"Hudud nomini olishda xato: {e}")
    
    return f"{latitude:.4f}, {longitude:.4f}"

# /start komandasiga javob berish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot boshlanishida foydalanuvchiga salom berish"""
    user = update.effective_user
    user_id = str(user.id)
    users = load_user_data()
    
    # Yangi foydalanuvchi qo'shish
    if user_id not in users:
        users[user_id] = {
            'first_name': user.first_name,
            'latitude': None,
            'longitude': None,
            'location_name': None,
            'prayer_times': None,
            'registered_date': datetime.now().isoformat()
        }
        save_user_data(users)
    
    keyboard = [
        [KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)],
        [KeyboardButton("❓ Yordam"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    
    welcome_text = f"""
Assalomu alaykum {user.first_name}! 👋

🕌 Bu Namoz Vaqti Botiga xush kelibsiz!

Bu bot sizga:
✅ Kunlik namoz jadvalini yuboradi
✅ Har namoz oldidan eslatadi
✅ Lokatsiyangizga mos namoz vaqtlarini ko'rsatadi

Boshlash uchun lokatsiyangizni yuboring yoki "Yordam" tugmasini bosing.
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Lokatsiyani qabul qilish
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchining lokatsiyasini qabul qilish"""
    try:
        user_id = str(update.effective_user.id)
        
        # Location xabarni tekshirish
        if not update.message or not update.message.location:
            await update.message.reply_text("❌ Lokatsiya olishda xato. Iltimos, qayta yuboring.")
            return
        
        location = update.message.location
        latitude = location.latitude
        longitude = location.longitude
        
        logger.info(f"User {user_id} lokatsiya yuborddi: {latitude}, {longitude}")
        
        await update.message.reply_text(
            "⏳ Joylashuvni aniqlanmoqda va namoz vaqtlari tayyorlanmoqda...",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("📍 Lokatsiyani qayta belgilash", request_location=True)],
                 [KeyboardButton("❓ Yordam"), KeyboardButton("⚙️ Sozlamalar")]],
                resize_keyboard=True
            )
        )
        
        # Hudud nomini olish (async)
        location_name = await get_location_name(latitude, longitude)
        logger.info(f"Hudud nomi: {location_name}")
        
        # Lokatsiyani saqlash
        users = load_user_data()
        if user_id in users:
            users[user_id]['latitude'] = latitude
            users[user_id]['longitude'] = longitude
            users[user_id]['location_name'] = location_name
            save_user_data(users)
            logger.info(f"User {user_id} lokatsiyasi saqlandi: {location_name}")
        
        # Namoz vaqtlarini olish
        prayer_times = await get_prayer_times(latitude, longitude)
        
        if prayer_times:
            users[user_id]['prayer_times'] = prayer_times
            save_user_data(users)
            logger.info(f"User {user_id} uchun namoz vaqtlari olindi")
            
            # Kunlik jadvalini yuborish
            await send_daily_schedule(update, prayer_times, location_name)
            
            await update.message.reply_text(
                f"✅ Joylashuvingiz saqlandi!\n\n📍 **{location_name}**\n\n"
                "Kunlik namoz jadvalini yuborib chiqdim.\n\n"
                "Siz har namoz oldidan eslatma olasiz.",
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("📍 Lokatsiyani qayta belgilash", request_location=True)],
                     [KeyboardButton("❓ Yordam"), KeyboardButton("⚙️ Sozlamalar")]],
                    resize_keyboard=True
                )
            )
        else:
            logger.error(f"User {user_id} uchun namoz vaqtlarini olib bo'lmadi")
            await update.message.reply_text(
                "❌ Namoz vaqtlarini olishda xato yuz berdi. Iltimos, lokatsiyani qayta yuboring.",
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("📍 Lokatsiyani qayta belgilash", request_location=True)]],
                    resize_keyboard=True
                )
            )
    except Exception as e:
        logger.error(f"Location handleri xatosi: {e}", exc_info=True)
        await update.message.reply_text(
            f"❌ Xato: {str(e)}\n\nIltimos, qayta urinib ko'ring.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("📍 Lokatsiyani qayta belgilash", request_location=True)]],
                resize_keyboard=True
            )
        )

# Kunlik jadvalini yuborish
async def send_daily_schedule(update: Update, prayer_times, location_name=None):
    """Kunlik namoz jadvalini yuborish"""
    schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
    
    if location_name:
        schedule_text += f"\n📍 **{location_name}**\n"
    
    schedule_text += "\n"
    
    for prayer_name, prayer_time in prayer_times.items():
        schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
    
    schedule_text += "\n⏰ Siz har namoz oldidan eslatma olasiz!"
    
    await update.message.reply_text(schedule_text, parse_mode='Markdown')

# /help komandasiga javob berish
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam ma'lumotlarini ko'rsatish"""
    help_text = """
📖 **Namoz Vaqti Botining Yordam Markazi**

**🎯 Botning funksiyalari:**

1️⃣ **Lokatsiya yuborish**
   - Lokatsiyani yuborish tugmasini bosing
   - Bot sizning joyingizga mos namoz vaqtlarini ko'rsatadi

2️⃣ **Kunlik jadval**
   - Har kuni bomdoddan oldin (4:00 AM) kunlik jadval yuboriladi
   - Barcha 5 ta namozning vaqti ko'rsatiladi

3️⃣ **Namoz eslatmalari**
   - Har namoz oldidan 15 daqiqa oldin eslatma olasiz
   - Shaxsiy eslatmalar sizning vaqt zonangizga mos

4️⃣ **Lokatsiyani qayta belgilash**
   - "📍 Lokatsiyani qayta belgilash" tugmasini bosing
   - Shuning bilan yangi joyga ko'chib kelgan bo'lsa, vaqtlar yangilanadi

**📞 Agar savollaringiz bo'lsa:**
Bot doim yozishda javob berishliga tayyorgman!

Boshlash uchun lokatsiyangizni yuboring! 📍
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

# /echo komandasiga javob berish
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi matnini qayta chop etish"""
    if not context.args:
        await update.message.reply_text("Iltimos, echo buyrug'idan keyin matn kiriting.\nMisol: /echo Salom dunyo")
        return
    
    text = ' '.join(context.args)
    await update.message.reply_text(f"Echo: {text}")

# Matnli xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har qanday matnli xabarni qayta ishlash"""
    user_message = update.message.text
    
    # Botni "yozmoqda" bo'lish ko'rsatish
    await update.message.chat.send_action(ChatAction.TYPING)
    
    # Xabarni qayta chop etish
    response = f"Siz yubordingiz: {user_message}\n\nMen bu xabarni qabul qildim! 👍"
    await update.message.reply_text(response)

# Tugma callback handleri
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inline tugmalarga javob berish"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        help_text = """
📖 **Namoz Vaqti Botining Yordam Markazi**

**🎯 Botning funksiyalari:**

1️⃣ **Lokatsiya yuborish**
   - Lokatsiyani yuborish tugmasini bosing

2️⃣ **Kunlik jadval**
   - Har kuni bomdoddan oldin kunlik jadval yuboriladi

3️⃣ **Namoz eslatmalari**
   - Har namoz oldidan eslatma olasiz

4️⃣ **Lokatsiyani qayta belgilash**
   - Yangi lokatsiya orqali yangilang

Boshlash uchun lokatsiyangizni yuboring! 📍
"""
        await query.edit_message_text(help_text, parse_mode='Markdown')
    
    elif query.data == 'settings':
        settings_text = """
⚙️ **Sozlamalar**

Sozlamalarni boshqarish uchun buyruqlardan foydalaning:

/start - Botni qayta ishga tushirish
/schedule - Kunlik jadvalini ko'rish
/location - Lokatsiyani ko'rish
/help - Yordam olish
"""
        await query.edit_message_text(settings_text)

# /schedule komandasiga javob berish
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Joriy kunlik jadvalini ko'rsatish"""
    user_id = str(update.effective_user.id)
    users = load_user_data()
    
    if user_id in users and users[user_id]['prayer_times']:
        schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n\n"
        prayer_times = users[user_id]['prayer_times']
        
        for prayer_name, prayer_time in prayer_times.items():
            schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
        
        await update.message.reply_text(schedule_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Avval lokatsiyangizni yuboring!\n\n"
            "Lokatsiyani yuborish tugmasini bosing."
        )

# /location komandasiga javob berish
async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Saqlangan lokatsiyani ko'rsatish"""
    user_id = str(update.effective_user.id)
    users = load_user_data()
    
    if user_id in users and users[user_id]['location_name']:
        location_info = f"""
📍 **Sizning Joylashuvingiz**

🏙️ **Hudud:** {users[user_id]['location_name']}
📌 **Koordinatalar:** {users[user_id]['latitude']:.4f}, {users[user_id]['longitude']:.4f}

Lokatsiyani qayta belgilash uchun "📍 Lokatsiyani qayta belgilash" tugmasini bosing.
"""
        await update.message.reply_text(location_info, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Lokatsiya saqlangan emas. Iltimos, lokatsiyangizni yuboring!")

# Bomdoddan oldin kunlik jadvalini avtomatik yuborish
async def send_morning_schedule(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har kuni bomdodda kunlik jadvalini yuborish"""
    users = load_user_data()
    
    for user_id, user_data in users.items():
        if user_data['latitude'] and user_data['longitude']:
            try:
                prayer_times = await get_prayer_times(user_data['latitude'], user_data['longitude'])
                
                if prayer_times:
                    users[user_id]['prayer_times'] = prayer_times
                    save_user_data(users)  # ⭐ YANGI VAQTLARNI SAQLASH!
                    
                    schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
                    
                    if user_data['location_name']:
                        schedule_text += f"\n📍 **{user_data['location_name']}**\n"
                    
                    schedule_text += "\n"
                    
                    for prayer_name, prayer_time in prayer_times.items():
                        schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
                    
                    schedule_text += "\n⏰ Har namoz oldidan eslatma olasiz!"
                    
                    try:
                        await context.bot.send_message(
                            chat_id=int(user_id),
                            text=schedule_text,
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        logger.error(f"User {user_id}ga xabar yuborishda xato: {e}")
            except Exception as e:
                logger.error(f"User {user_id} uchun jadval tayyorlanishda xato: {e}")
    
    save_user_data(users)

# Namoz eslatmasini yuborish
async def send_prayer_reminder(context: ContextTypes.DEFAULT_TYPE, prayer_name: str) -> None:
    """Namozdan 15 daqiqa oldin eslatma yuborish"""
    users = load_user_data()
    
    for user_id, user_data in users.items():
        if user_data['prayer_times'] and prayer_name in user_data['prayer_times']:
            reminder_text = f"🔔 **{prayer_name} namozi vaqti yaqin!**\n\n⏰ Vaqti: {user_data['prayer_times'][prayer_name]}\n\nZaharla qiling!"
            
            try:
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=reminder_text,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"User {user_id}ga eslatma yuborishda xato: {e}")

# Text xabarlari handleri
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Keyboard tugmalaridan matnni qayta ishlash"""
    text = update.message.text
    user_id = str(update.effective_user.id)
    
    if text == "❓ Yordam":
        await help_command(update, context)
    elif text == "⚙️ Sozlamalar":
        settings_text = """
⚙️ **Sozlamalar**

Sozlamalarni boshqarish uchun buyruqlardan foydalaning:

/start - Botni qayta ishga tushirish
/schedule - Kunlik jadvalini ko'rish
/location - Lokatsiyani ko'rish
/help - Yordam olish
"""
        await update.message.reply_text(settings_text, parse_mode='Markdown')

# Xata qaytarish
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatalarni qayta ishlash"""
    logger.error(msg="Xato:", exc_info=context.error)

# Botni ishga tushirish
def main() -> None:
    """Bot asosiy funksiyasi"""
    # Application yaratish
    application = Application.builder().token(TOKEN).build()
    
    # Buyruq handlerlari
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("location", location_command))
    
    # Lokatsiya handleri
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    
    # Text message handleri (keyboard tugmalari uchun)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Tugma handleri
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Job queue - kunlik jadvalini yuborish
    job_queue = application.job_queue
    
    # Har kuni 4:00 AM da kunlik jadvalini yuborish
    job_queue.run_daily(
        send_morning_schedule,
        time=time(hour=4, minute=0),
        name='daily_schedule'
    )
    
    # Xata handleri
    application.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    print("🤖 Namoz Vaqti Boti ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
