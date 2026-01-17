# 🔍 BOT KODINING BATAFSIL TUSHUNTIRISHI

## KUTUBXONALAR VA IMPORT QISMLARI

```python
import os                    # Operatsion sistem o'zgaruvchilari
import json                  # JSON fayllarni o'qish/yozish
import logging              # Xatolarni yozib turish
import requests             # API lardan so'rov yuborish
from datetime import ...    # Vaqt va sana bilan ishlash
from telegram import ...    # Telegram API
from telegram.ext import... # Telegram bot extensionlari
import asyncio              # Asinxron programmalar
```

---

## ASOSIY FUNKSIYALAR BATAFSIL

### 1️⃣ VERI SAQLASH FUNKSIYALARI

#### `load_user_data()`
```python
def load_user_data():
    if os.path.exists('user_data.json'):  # Fayl bormi?
        with open(...) as f:               # Fayl ochadi
            return json.load(f)            # JSON dan o'qiydi
    return {}                              # Yo'q bo'lsa bo'sh dict
```

**NIMA QILADI:**
- `user_data.json` faylini ochadi
- JSON formatini Python dictionary ga o'zgartirada
- Agar fayl bo'lmasa, bo'sh dictionary qaytaradi

**MISOL NATIJASI:**
```python
{
    "778165270": {
        "first_name": "Otamurod",
        "latitude": 40.756,
        "longitude": 69.115,
        ...
    }
}
```

---

#### `save_user_data(data)`
```python
def save_user_data(data):
    with open('user_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**NIMA QILADI:**
- Python dictionary ni JSON formatiga o'zgartirada
- `user_data.json` faylga yozadi
- `ensure_ascii=False` - O'zbek tilidagi matnni to'g'ri yozadi
- `indent=2` - Komponentlarni qancha qayla formatlanadi

---

### 2️⃣ API FUNKSIYALARI

#### `get_prayer_times(latitude, longitude)`
```python
async def get_prayer_times(latitude, longitude):
    url = "https://api.aladhan.com/v1/timings/..."
    params = {
        'latitude': latitude,      # 40.756
        'longitude': longitude,    # 69.115
        'method': 2                # ISNA metodi
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if data['code'] == 200:  # Muvaffaq bo'ldimi?
        timings = data['data']['timings']
        return {
            'Bomdod': timings['Fajr'],
            'Peshin': timings['Dhuhr'],
            ...
        }
```

**ISHCHI JARAYON:**
```
1. API URL yasaladi
2. Latitude va Longitude parametrlari qo'shiladi
3. GET so'rov yuboriladi (timeout=10 soniya)
4. JSON javob olinadi
5. Status code tekshiriladi (200 = muvaffaq)
6. Timings ma'lumotlari o'zgartiriladi
7. Python dictionary qaytariladi
```

**ALADHAN API METHOD LARI:**
- Method 1: University of the Islamic Sciences, Karachi
- Method 2: Islamic Society of North America (ISNA) ← FOYDALANAMIZ
- Method 3: Muslim World League
- ...va boshqalar

**JAVOB STRUKTURA:**
```json
{
    "code": 200,
    "data": {
        "timings": {
            "Fajr": "06:25",    ← Bomdod
            "Sunrise": "07:52",
            "Dhuhr": "12:34",   ← Peshin
            "Asr": "15:02",     ← Asr
            "Sunset": "17:20",
            "Maghrib": "17:23", ← Shom
            "Isha": "18:43",    ← Xufton
            "Imsak": "06:08"
        }
    }
}
```

---

#### `get_location_name(latitude, longitude)`
```python
async def get_location_name(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': latitude,           # 40.756
        'lon': longitude,          # 69.115
        'format': 'json',
        'zoom': 10,                # Aniqlik darajasi
        'addressdetails': 1
    }
    headers = {'User-Agent': 'PrayerTimesBot/1.0'}
    
    response = requests.get(url, params=params, 
                           headers=headers, timeout=10)
    data = response.json()
    
    if 'address' in data:
        address = data['address']
        city = address.get('city', ...)
        state = address.get('state', ...)
        country = address.get('country', ...)
        
        location_parts = [city, state, country]
        return ', '.join(location_parts)
```

**REVERSE GEOCODING NIMA:**
- Koordinatalardan hudud nomini topish
- Longitude + Latitude → Shahar, Viloyat, Davlat
- OpenStreetMap dan foydalanadi (bepul)

**JAVOB MISOLI:**
```json
{
    "address": {
        "city": "Tashkent",
        "state": "Tashkent City",
        "country": "Uzbekistan",
        "postcode": "100000"
    }
}
```

**NATIJA:** "Tashkent, Tashkent City, Uzbekistan"

---

### 3️⃣ TELEGRAM HANDLER FUNKSIYALARI

#### `start(update, context)`
```python
async def start(update, context):
    user = update.effective_user      # Kimdir yubordi
    user_id = str(user.id)            # User ID
    
    users = load_user_data()          # JSON dan o'qiy
    
    if user_id not in users:          # Yangi foydalanuvchimi?
        users[user_id] = {
            'first_name': user.first_name,
            'latitude': None,
            'longitude': None,
            'location_name': None,
            'prayer_times': None,
            'registered_date': datetime.now().isoformat()
        }
        save_user_data(users)         # JSON ga yoz
    
    keyboard = [
        [KeyboardButton("📍 Lokatsiyani yuborish", 
                       request_location=True)],
        [KeyboardButton("❓ Yordam"), 
         KeyboardButton("⚙️ Sozlamalar")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, 
                                       resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, 
                                    reply_markup=reply_markup)
```

**ISHCHI JARAYON:**
```
1. Foydalanuvchining ID si olinadi
2. JSON dan barcha users yuklnadi
3. Yangi foydalanuvchimi tekshiriladi
4. Agar yangi bo'lsa, yangi record qo'shiladi
5. JSON ga saqlanaladi
6. Keyboard tugmalari yasaladi
7. Salom xabari yuboriladi
```

---

#### `handle_location(update, context)`
```python
async def handle_location(update, context):
    try:  # Xatolarni tutish uchun
        user_id = str(update.effective_user.id)
        location = update.message.location
        
        latitude = location.latitude
        longitude = location.longitude
        
        # Hudud nomini olish
        location_name = await get_location_name(
            latitude, longitude)
        
        # Namoz vaqtlarini olish
        prayer_times = await get_prayer_times(
            latitude, longitude)
        
        if prayer_times:
            # JSON ga saqlash
            users = load_user_data()
            users[user_id]['latitude'] = latitude
            users[user_id]['longitude'] = longitude
            users[user_id]['location_name'] = location_name
            users[user_id]['prayer_times'] = prayer_times
            save_user_data(users)
            
            # Jadval yuborish
            await send_daily_schedule(update, 
                                     prayer_times, 
                                     location_name)
            
            # Tasdiqlash xabari
            await update.message.reply_text(
                f"✅ Joylashuvingiz saqlandi!\n\n"
                f"📍 **{location_name}**")
        else:
            await update.message.reply_text(
                "❌ Namoz vaqtlarini olib bo'lmadi")
    
    except Exception as e:
        logger.error(f"Xato: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")
```

**ISHCHI JARAYON:**
```
try BLOKI:
├─ User ID ni ol
├─ Location object dan latitude/longitude ni ol
├─ await get_location_name() → Hudud nomi ol
├─ await get_prayer_times() → Namoz vaqtlarni ol
├─ JSON dan users ni o'qiy
├─ User ma'lumotlarni yangilang
├─ JSON ga saqlang
├─ Jadvalini yuborish
└─ Tasdiqlash xabari

except BLOKI:
└─ Xato bo'lsa, foydalanuvchiga xabar
```

**ASYNC FUNKSIYALARI NIMA:**
- `async def` - Asinxron funksiya
- `await` - Natijani kutish (API javob kelgunini)
- Bu API lardan javob kutganda boshqa ishlar bajariladi

---

#### `send_daily_schedule(update, prayer_times, location_name)`
```python
async def send_daily_schedule(update, prayer_times, 
                             location_name=None):
    schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
    
    if location_name:
        schedule_text += f"\n📍 **{location_name}**\n\n"
    
    for prayer_name, prayer_time in prayer_times.items():
        schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
    
    schedule_text += "\n⏰ Siz har namoz oldidan eslatma olasiz!"
    
    await update.message.reply_text(schedule_text, 
                                   parse_mode='Markdown')
```

**STRING FORMATTING:**
```
f"📍 **{location_name}**"
  ↑
  f-string - o'zgaruvchilar joyiga qo'yiladi

parse_mode='Markdown':
- **qo'lin** → qo'lin (qalin)
- *qiyoshma* → qiyoshma (italik)
- `kod` → kod (monospace)
```

---

### 4️⃣ JOB QUEUE - AVTOMATIK ISHLAR

#### `send_morning_schedule(context)`
```python
async def send_morning_schedule(context):
    users = load_user_data()
    
    for user_id, user_data in users.items():
        if user_data['latitude'] and user_data['longitude']:
            # Har bir foydalanuvchi uchun
            prayer_times = await get_prayer_times(
                user_data['latitude'], 
                user_data['longitude'])
            
            if prayer_times:
                # Jadval yasaladi
                schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
                schedule_text += f"\n📍 **{user_data['location_name']}**\n"
                
                for prayer_name, prayer_time in prayer_times.items():
                    schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
                
                # Xabar yuboriladi
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=schedule_text,
                    parse_mode='Markdown')
```

**MAIN FUNKSIYADA:**
```python
job_queue = application.job_queue

job_queue.run_daily(
    send_morning_schedule,
    time=time(hour=4, minute=0),  # 4:00 AM
    name='daily_schedule'
)
```

**NIMA QILADI:**
- Har kuni 4:00 AM da chaqiriladi
- Barcha foydalanuvchilarni loop qiladi
- Har birining lokatsiyasi uchun yangi vaqtlarni oladi
- Jadval xabarini yuboradi

---

## ⚡ ASINKRON PROGRAMMALAR (ASYNC/AWAIT)

### Nima uchun kerak?

```
UMUMAN (synchronous):
┌─────────────────────────────────────────┐
│ 1. API so'rov yuborish (5 soniya)       │ <- Kutish
│ 2. Javobni qayta ishlash (1 soniya)     │
│ 3. Boshqa operatsiya (1 soniya)         │
│ TOTAL: 7 soniya                         │
└─────────────────────────────────────────┘

ASINXRON (async/await):
┌─────────────────────────────────────────┐
│ 1. API so'rov yuborish (boshlanadi)     │
│ 2. Boshqa ishlarni qil (kutmasdan)      │ ← Parallel
│ 3. API javob kelsa, qayta ishlang       │
│ TOTAL: 5 soniya                         │
└─────────────────────────────────────────┘
```

---

## 🎯 MISOL: FOYDALANUVCHI LOKATSIYA YUBORGANDA QADAMLAR

```
QADAM 1: Foydalanuvchi Telegramda
└─ "📍 Lokatsiyani yuborish" bosadi
   └─ Telegram: "Joylashuvni yubor" so'rashi

QADAM 2: Foydalanuvchi lokatsiya yuboradi
└─ Update: {
    "message": {
        "location": {
            "latitude": 40.756,
            "longitude": 69.115
        }
    }
}

QADAM 3: Bot handle_location() chaqiradi
└─ Logger: "User 778165270 lokatsiya yubordi: 40.756, 69.115"

QADAM 4: Bot "⏳ Aniqlanmoqda..." xabari yuboradi
└─ Telegram → Foydalanuvchi

QADAM 5: Bot get_location_name() chaqiradi
└─ Nominatim API ga so'rov:
   "https://nominatim...?lat=40.756&lon=69.115"
   ↓
   Javob: "Tashkent, Tashkent City, Uzbekistan"

QADAM 6: Bot get_prayer_times() chaqiradi
└─ Aladhan API ga so'rov:
   "https://api.aladhan...?latitude=40.756&longitude=69.115"
   ↓
   Javob: {
     "Bomdod": "06:25",
     "Peshin": "12:34",
     ...
   }

QADAM 7: Bot send_daily_schedule() chaqiradi
└─ Xabar yasaladi:
   📅 **Bugungi Namoz Vaqtlari**
   📍 **Tashkent, Tashkent City, Uzbekistan**
   🕌 Bomdod: 06:25
   🕌 Peshin: 12:34
   ...

QADAM 8: Bot save_user_data() chaqiradi
└─ user_data.json ga yozadi:
   {
     "778165270": {
       "latitude": 40.756,
       "longitude": 69.115,
       "location_name": "Tashkent, Tashkent City, Uzbekistan",
       "prayer_times": {
         "Bomdod": "06:25",
         ...
       }
     }
   }

QADAM 9: Bot tasdiqlash xabari yuboradi
└─ "✅ Joylashuvingiz saqlandi!
     📍 Tashkent, Tashkent City, Uzbekistan"

QADAM 10: Har kuni 4:00 AM
└─ send_morning_schedule() avtomatik chaqiriladi
   ├─ Yangi namoz vaqtlari olinadi
   ├─ Jadval yasaladi
   └─ Xabar yuboriladi
```

---

## 📊 XULOSA

```
BOT KODINING ASOSIY TUZILISHI:

KUTUBXONALAR
    ↓
GLOBAL O'ZGARUVCHILAR (TOKEN, FILE_NAME, PRAYER_NAMES)
    ↓
HELPER FUNKSIYALARI (load_user_data, save_user_data)
    ↓
API FUNKSIYALARI (get_prayer_times, get_location_name)
    ↓
TELEGRAM HANDLER FUNKSIYALARI (start, handle_location, help_command, ...)
    ↓
JOB QUEUE FUNKSIYALARI (send_morning_schedule)
    ↓
ERROR HANDLER
    ↓
MAIN() FUNKSIYASI
    ├─ Application yasaladi
    ├─ Barcha handlerlari qo'shiladi
    ├─ Job Queue sozlanadi
    └─ polling ishga tushar
```

Umid qilamki, endi botning ishlashi juda aniq! 🎯✨
