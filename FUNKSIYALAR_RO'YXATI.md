# 📚 KUTUBXONALAR VA FUNKSIYALAR RO'YXATI

## 📦 ASOSIY KUTUBXONALAR

### 1. `os` - Operatsion Sistema
```python
import os

os.getenv('TELEGRAM_BOT_TOKEN')  # Environment variable olish
os.path.exists('user_data.json')  # Fayl bormi tekshirish
```
**Nima uchun kerak:** Fayl tekshirish, environment o'zgaruvchilari

---

### 2. `json` - JSON Fayl Boshqaruvi
```python
import json

json.load(f)        # JSON fayldan o'qish
json.dump(data, f)  # Python datani JSON ga o'zgartirib yozish
```
**Nima uchun kerak:** user_data.json bilan ishlash

---

### 3. `logging` - Xatolarni Yozib Turish
```python
import logging

logging.basicConfig(format='...', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.error(f"Xato: {e}")
```
**Nima uchun kerak:** Xatolarni debug qilish, bot jarayonlarini kuzatish

---

### 4. `requests` - HTTP So'rovlar
```python
import requests

response = requests.get(url, params=params, timeout=10)
data = response.json()
```
**Nima uchun kerak:** Nominatim va Aladhan API lardan ma'lumot olish

---

### 5. `datetime` - Vaqt va Sana
```python
from datetime import datetime, time, timedelta

datetime.now()                      # Joriy vaqt
time(hour=4, minute=0)             # 4:00 AM
datetime.now().isoformat()         # String formatda vaqt
```
**Nima uchun kerak:** Vaqt bilan ishlash, timestamp, registered_date

---

### 6. `telegram` - Telegram Bot API
```python
from telegram import Update, InlineKeyboardButton, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler
```
**Nima uchun kerak:** Bot asosiy kutubxonasi

---

### 7. `asyncio` - Asinxron Programmalar
```python
import asyncio

async def get_prayer_times(lat, lon):  # Asinxron funksiya
    ...
    await ...  # Natijani kutish
```
**Nima uchun kerak:** API lardan javob kutganda boshqa ishlarni bajarish

---

## 🔧 BOT ASOSIY FUNKSIYALARI

### VERI SAQLASH FUNKSIYALARI

#### `load_user_data()`
```python
def load_user_data():
    """Foydalanuvchi ma'lumotlarini JSON fayldan yuklash"""
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
```
- **Nima qiladi:** JSON fayldan o'qiydi yoki bo'sh dict qaytaradi
- **Qaytaradi:** Python dictionary
- **Misol:**
```python
{
    "778165270": {
        "first_name": "Otamurod",
        "latitude": 40.756,
        ...
    }
}
```

---

#### `save_user_data(data)`
```python
def save_user_data(data):
    """Foydalanuvchi ma'lumotlarini JSON faylga saqlash"""
    with open('user_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```
- **Nima qiladi:** Python dictionary ni JSON ga o'zgartirib yozadi
- **Parametrlar:** data - dictionary
- **ensure_ascii=False:** O'zbek harflari to'g'ri yoziladi
- **indent=2:** Chiroyli formatlanadi

---

### API FUNKSIYALARI

#### `get_prayer_times(latitude, longitude)`
```python
async def get_prayer_times(latitude, longitude):
    """API orqali namoz vaqtlarini olish"""
    url = f"https://api.aladhan.com/v1/timings/{int(datetime.now().timestamp())}"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'method': 2  # ISNA method
    }
    response = requests.get(url, params=params, timeout=10)
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
    return None
```

**Parametrlar:**
- `latitude` (float): Joylashuvning kengligi (40.756)
- `longitude` (float): Joylashuvning uzunligi (69.115)

**Qaytaradi:**
```python
{
    'Bomdod': '06:25',
    'Peshin': '12:34',
    'Asr': '15:02',
    'Shom': '17:23',
    'Xufton': '18:43'
}
```

**Xatolar:** None qaytaradi

**API URL misoli:**
```
https://api.aladhan.com/v1/timings/1705537200?latitude=40.756&longitude=69.115&method=2
```

---

#### `get_location_name(latitude, longitude)`
```python
async def get_location_name(latitude, longitude):
    """Koordinatalardan hudud nomini olish"""
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': latitude,
        'lon': longitude,
        'format': 'json',
        'zoom': 10,
        'addressdetails': 1
    }
    headers = {'User-Agent': 'PrayerTimesBot/1.0'}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    data = response.json()
    
    if 'address' in data:
        address = data['address']
        city = address.get('city', address.get('town', address.get('village', '')))
        state = address.get('state', '')
        country = address.get('country', '')
        
        location_parts = [city, state, country]
        location_name = ', '.join([p for p in location_parts if p])
        return location_name
    
    return f"{latitude:.4f}, {longitude:.4f}"
```

**Parametrlar:**
- `latitude` (float): Joylashuvning kengligi
- `longitude` (float): Joylashuvning uzunligi

**Qaytaradi:**
```python
"Tashkent, Tashkent City, Uzbekistan"
# yoki agar xato bo'lsa:
"40.7562, 69.1151"
```

---

### TELEGRAM HANDLER FUNKSIYALARI

#### `start(update, context)`
```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot boshlanishida foydalanuvchiga salom berish"""
    user = update.effective_user
    user_id = str(user.id)
    
    users = load_user_data()
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
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = f"""
Assalomu alaykum {user.first_name}! 👋

🕌 Bu Namoz Vaqti Botiga xush kelibsiz!
...
"""
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
```

**Parametrlar:**
- `update` - Telegram UPDATE objekt
- `context` - Bot konteksti

**Qiladi:**
1. Foydalanuvchini qayd qiladi
2. Keyboard tugmalarini ko'rsatadi
3. Salom xabari yuboradi

---

#### `handle_location(update, context)`
```python
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchining lokatsiyasini qabul qilish"""
    try:
        user_id = str(update.effective_user.id)
        location = update.message.location
        
        latitude = location.latitude
        longitude = location.longitude
        
        # "Aniqlanmoqda..." xabari
        await update.message.reply_text("⏳ Joylashuvni aniqlanmoqda...")
        
        # Hudud nomini olish
        location_name = await get_location_name(latitude, longitude)
        
        # Namoz vaqtlarini olish
        prayer_times = await get_prayer_times(latitude, longitude)
        
        if prayer_times:
            # JSON ga saqlash
            users = load_user_data()
            users[user_id]['latitude'] = latitude
            users[user_id]['longitude'] = longitude
            users[user_id]['location_name'] = location_name
            users[user_id]['prayer_times'] = prayer_times
            save_user_data(users)
            
            # Jadval yuborish
            await send_daily_schedule(update, prayer_times, location_name)
            
            # Tasdiqlash
            await update.message.reply_text(
                f"✅ Joylashuvingiz saqlandi!\n\n📍 **{location_name}**"
            )
    
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")
```

**Qiladi:**
1. Lokatsiyani qabul qiladi
2. Hudud nomini oladi
3. Namoz vaqtlarini oladi
4. JSON da saqlaydi
5. Xabar yuboradi

---

#### `send_daily_schedule(update, prayer_times, location_name=None)`
```python
async def send_daily_schedule(update: Update, prayer_times, location_name=None):
    """Kunlik namoz jadvalini yuborish"""
    schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
    
    if location_name:
        schedule_text += f"\n📍 **{location_name}**\n\n"
    
    for prayer_name, prayer_time in prayer_times.items():
        schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
    
    schedule_text += "\n⏰ Siz har namoz oldidan eslatma olasiz!"
    
    await update.message.reply_text(schedule_text, parse_mode='Markdown')
```

**Parametrlar:**
- `update` - Telegram UPDATE
- `prayer_times` - Namoz vaqtlari dictionary
- `location_name` - Hudud nomi (ixtiyoriy)

**Qiladi:** Jadval xabarini formatlaydi va yuboradi

---

#### `help_command(update, context)`
```python
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yordam ma'lumotlarini ko'rsatish"""
    help_text = """
📖 **Namoz Vaqti Botining Yordam Markazi**
...
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')
```

---

#### `schedule_command(update, context)`
```python
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
            "❌ Avval lokatsiyangizni yuboring!"
        )
```

---

#### `location_command(update, context)`
```python
async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Saqlangan lokatsiyani ko'rsatish"""
    user_id = str(update.effective_user.id)
    users = load_user_data()
    
    if user_id in users and users[user_id]['location_name']:
        location_info = f"""
📍 **Sizning Joylashuvingiz**

🏙️ **Hudud:** {users[user_id]['location_name']}
📌 **Koordinatalar:** {users[user_id]['latitude']:.4f}, {users[user_id]['longitude']:.4f}
"""
        await update.message.reply_text(location_info, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Lokatsiya saqlangan emas. Iltimos, lokatsiyangizni yuboring!"
        )
```

---

#### `handle_text_message(update, context)`
```python
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Keyboard tugmalaridan matnni qayta ishlash"""
    text = update.message.text
    
    if text == "❓ Yordam":
        await help_command(update, context)
    elif text == "⚙️ Sozlamalar":
        settings_text = "⚙️ **Sozlamalar**\n..."
        await update.message.reply_text(settings_text, parse_mode='Markdown')
```

---

### JOB QUEUE FUNKSIYALARI

#### `send_morning_schedule(context)`
```python
async def send_morning_schedule(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Har kuni 4:00 AM da kunlik jadvalini yuborish"""
    users = load_user_data()
    
    for user_id, user_data in users.items():
        if user_data['latitude'] and user_data['longitude']:
            # Yangi vaqtlarni olish
            prayer_times = await get_prayer_times(
                user_data['latitude'], 
                user_data['longitude']
            )
            
            if prayer_times:
                users[user_id]['prayer_times'] = prayer_times
                
                # Jadval yasash
                schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
                schedule_text += f"\n📍 **{user_data['location_name']}**\n\n"
                
                for prayer_name, prayer_time in prayer_times.items():
                    schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
                
                # Xabar yuborish
                try:
                    await context.bot.send_message(
                        chat_id=int(user_id),
                        text=schedule_text,
                        parse_mode='Markdown'
                    )
                except Exception as e:
                    logger.error(f"Xato: {e}")
    
    save_user_data(users)
```

**Kisha chaqiriladi:** Har kuni 4:00 AM
**Qiladi:**
1. Barcha foydalanuvchilarni loop qiladi
2. Har birining yangi namoz vaqtlarini oladi
3. JSON da yangilaydi
4. Xabar yuboradi

---

### ERROR HANDLER

#### `error_handler(update, context)`
```python
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatalarni qayta ishlash"""
    logger.error(msg="Xato:", exc_info=context.error)
```

---

### MAIN FUNKSIYA

#### `main()`
```python
def main() -> None:
    """Bot asosiy funksiyasi"""
    # Application yasaladi
    application = Application.builder().token(TOKEN).build()
    
    # COMMAND HANDLERLARI
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("location", location_command))
    
    # LOCATION HANDLERI
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    
    # TEXT MESSAGE HANDLERI
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text_message
    ))
    
    # CALLBACK HANDLERI (BUTTON CHIQISHI)
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # JOB QUEUE - AVTOMATIK ISHLAR
    job_queue = application.job_queue
    
    # Har kuni 4:00 AM da
    job_queue.run_daily(
        send_morning_schedule,
        time=time(hour=4, minute=0),
        name='daily_schedule'
    )
    
    # ERROR HANDLER
    application.add_error_handler(error_handler)
    
    # BOT BOSHLANADI
    print("🤖 Namoz Vaqti Boti ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
```

---

## 📊 FUNKSIYALAR QAVS JADVAL

| Funksiya Nomi | Turi | Parametrlar | Qaytaradi | Nima Qiladi |
|---|---|---|---|---|
| `load_user_data()` | def | Yo'q | dict | JSON dan o'qiydi |
| `save_user_data()` | def | data:dict | Yo'q | JSON ga yozadi |
| `get_prayer_times()` | async | lat, lon | dict/None | API dan vaqtlarni oladi |
| `get_location_name()` | async | lat, lon | str | API dan hudud nomini oladi |
| `start()` | async | update, context | Yo'q | Salom xabari |
| `handle_location()` | async | update, context | Yo'q | Lokatsiyani qayta ishlaydi |
| `send_daily_schedule()` | async | update, times, name | Yo'q | Jadvalini yuboradi |
| `help_command()` | async | update, context | Yo'q | Yordam ko'rsatadi |
| `schedule_command()` | async | update, context | Yo'q | Jadvalini ko'rsatadi |
| `location_command()` | async | update, context | Yo'q | Lokatsiyani ko'rsatadi |
| `handle_text_message()` | async | update, context | Yo'q | Text xabarini qayta ishlaydi |
| `send_morning_schedule()` | async | context | Yo'q | Avtomatik jadval yuboradi |
| `button_callback()` | async | update, context | Yo'q | Tugma bosilishini qayta ishlaydi |
| `error_handler()` | async | update, context | Yo'q | Xatalarni tutadi |
| `main()` | def | Yo'q | Yo'q | Bot boshlanadi |

---

## 🎯 XULOSA

Bot **15 ta asosiy funksiya** dan iborat:
- **2 ta** veri saqlash funksiyasi
- **2 ta** API funksiyasi
- **7 ta** Telegram handler funksiyasi
- **1 ta** Job queue funksiyasi
- **1 ta** Error handler
- **1 ta** Main funksiya
- **1 ta** Button callback funksiya

Barcha funksiyalar birgalikda ishlaydi va foydalanuvchiga namoz vaqtlarini samarali tarzda ta'minlaydi! 🕌📱✨
