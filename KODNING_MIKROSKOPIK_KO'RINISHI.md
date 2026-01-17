# 🔬 BOT KODINING MIKROSKOPIK KO'RINISHI

## KODNING ASOSIY QISMLARI BATAFSIL

### 1. IMPORTS VA SETUP (1-20 qatorlar)

```python
import os                    # Sistema o'zgaruvchilari
import json                  # JSON format
import logging              # Log yozish
import requests             # HTTP so'rovlari
from datetime import datetime, time, timedelta  # Vaqt boshqaruvi
from telegram import ...    # Telegram kutubxonasi
from telegram.ext import ... # Bot functionallik
import asyncio              # Asinxron dasturlar
```

**Nima qiladi:**
- Barcha kerakli kutubxonalarni yuklaydi
- Telegram API bilan ishlashni tayyorlaydi
- API so'rovlar yuborish vositalarini olamiz

---

### 2. LOGGING SETUP (11-16 qatorlar)

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
```

**Nima qiladi:**
```
Har bir log xabari shunday ko'rinadi:
2026-01-17 18:25:53,357 - telegram - INFO - HTTP Request...

Buning yordamida:
- Qaysi vaqt bo'lganini bilishimiz
- Qaysi kutubxonadan kelganini bilishimiz
- Xato yoki ma'lumot ekanini bilishimiz
```

---

### 3. GLOBAL O'ZGARUVCHILAR (18-35 qatorlar)

```python
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8517360815:...')
USER_DATA_FILE = 'user_data.json'
PRAYER_NAMES = {
    'Bomdod': 'Fajr',
    'Peshin': 'Dhuhr',
    'Asr': 'Asr',
    'Shom': 'Maghrib',
    'Xufton': 'Isha'
}
```

**Nima qiladi:**
- `TOKEN` - Telegramdan ma'lumot yuborish uchun
- `USER_DATA_FILE` - Ma'lumot saqlash fayli nomi
- `PRAYER_NAMES` - Namoz nomlari

---

### 4. LOAD/SAVE FUNKSIYALARI (37-54 qatorlar)

```python
def load_user_data():
    """Foydalanuvchi ma'lumotlarini JSON fayldan yuklash"""
    if os.path.exists(USER_DATA_FILE):
        # Fayl borsa, ochadi
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}  # Yo'q bo'lsa, bo'sh dict

def save_user_data(data):
    """Foydalanuvchi ma'lumotlarini JSON faylga saqlash"""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**ISHLASH JARAYONI:**

```
load_user_data():
1. Fayl mavjudmi tekshir
2. Agar bor:
   - Fayl ochadi
   - JSON dan o'qiydi (Dictionary ga aylantirada)
   - Dictionary qaytaradi
3. Agar yo'q:
   - Bo'sh dictionary {} qaytaradi

save_user_data(data):
1. Dictionary olinadi
2. JSON formatiga o'zgartiriladi
3. Fayl ochiladi (yozish rejimida)
4. JSON ga yoziladi
5. Fayl yopiladi
```

**MISOL:**

```python
# Load
users = load_user_data()
# Natija: {"778165270": {"first_name": "Otamurod", ...}}

# Save
users["778165270"]["latitude"] = 40.756
save_user_data(users)
# JSON faylga yozildi
```

---

### 5. PRAYER TIMES API (56-79 qatorlar)

```python
async def get_prayer_times(latitude, longitude):
    try:
        # URL yasash
        url = f"https://api.aladhan.com/v1/timings/{int(datetime.now().timestamp())}"
        
        # Parametrlarni qo'shish
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'method': 2  # ISNA metodi
        }
        
        # SO'ROV YUBORISH
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # JAVOBNI QAYTA ISLASH
        data = response.json()
        
        # TEKSHIRISH
        if data['code'] == 200:  # Muvaffaq bo'ldimi?
            timings = data['data']['timings']
            
            # QAYTA FORMATLASH
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
```

**STEP BY STEP:**

```
STEP 1: URL YASASH
═══════════════════════════════════════════════════════════
url = "https://api.aladhan.com/v1/timings/1705537200"
      (timestamp - bugungi vaqt raqamlik formatda)

STEP 2: PARAMETRLAR QOSHISH
═══════════════════════════════════════════════════════════
?latitude=40.756
&longitude=69.115
&method=2

TO'LIQ URL:
https://api.aladhan.com/v1/timings/1705537200?latitude=40.756&longitude=69.115&method=2

STEP 3: SO'ROV YUBORISH
═══════════════════════════════════════════════════════════
requests.get(url, params=params, timeout=10)

timeout=10 → 10 sekundadan ko'p kutmasdan xato chiqaradi

STEP 4: JAVOB OLISH
═══════════════════════════════════════════════════════════
response = <Response status_code=200>
data = response.json()

data = {
  "code": 200,
  "status": "OK",
  "data": {
    "timings": {
      "Fajr": "06:25",
      "Dhuhr": "12:34",
      ...
    }
  }
}

STEP 5: TEKSHIRISH VA QAYTA FORMATLASH
═══════════════════════════════════════════════════════════
if data['code'] == 200:  # Muvaffaq bo'ldimi?
    timings = data['data']['timings']
    return {
        'Bomdod': timings['Fajr'],    # 06:25
        'Peshin': timings['Dhuhr'],   # 12:34
        ...
    }

NATIJA:
{
    'Bomdod': '06:25',
    'Peshin': '12:34',
    'Asr': '15:02',
    'Shom': '17:23',
    'Xufton': '18:43'
}
```

---

### 6. LOCATION NAME API (81-115 qatorlar)

```python
async def get_location_name(latitude, longitude):
    try:
        # Nominatim API URL
        url = "https://nominatim.openstreetmap.org/reverse"
        
        # Parametrlar
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'zoom': 10,
            'addressdetails': 1
        }
        
        # Header qo'shish (API so'rov qilish uchun)
        headers = {
            'User-Agent': 'PrayerTimesBot/1.0'
        }
        
        # SO'ROV
        response = requests.get(url, params=params, 
                               headers=headers, timeout=10)
        response.raise_for_status()
        
        # JAVOB
        data = response.json()
        
        # ADDRESS MA'LUMOTLARNI CHIQARISH
        if 'address' in data:
            address = data['address']
            
            # Hudud nomlari
            city = address.get('city', address.get('town', address.get('village', '')))
            state = address.get('state', '')
            country = address.get('country', '')
            
            # BIRLASHTIRIB QAYTARISH
            location_parts = []
            if city: location_parts.append(city)
            if state: location_parts.append(state)
            if country: location_parts.append(country)
            
            location_name = ', '.join(location_parts) if location_parts else f"{latitude:.4f}, {longitude:.4f}"
            return location_name
    
    except Exception as e:
        logger.error(f"Hudud nomini olishda xato: {e}")
    
    return f"{latitude:.4f}, {longitude:.4f}"
```

**MISOLIDA ISHCHI JARAYON:**

```
INPUT: latitude=40.756, longitude=69.115

API SO'ROQUSI:
https://nominatim.openstreetmap.org/reverse?lat=40.756&lon=69.115&format=json

API JAVOB:
{
  "address": {
    "city": "Tashkent",
    "state": "Tashkent City",
    "country": "Uzbekistan"
  }
}

QAYTA ISLASH:
city = "Tashkent"
state = "Tashkent City"
country = "Uzbekistan"

location_parts = ["Tashkent", "Tashkent City", "Uzbekistan"]

', '.join(location_parts) = "Tashkent, Tashkent City, Uzbekistan"

NATIJA: "Tashkent, Tashkent City, Uzbekistan"
```

---

### 7. START HANDLER (117-159 qatorlar)

```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    
    users = load_user_data()
    
    # YANGI FOYDALANUVCHI?
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
    
    # KEYBOARD TUGMALARI
    keyboard = [
        [KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)],
        [KeyboardButton("❓ Yordam"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # SALOM XABARI
    welcome_text = f"""
Assalomu alaykum {user.first_name}! 👋
...
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
```

**QADAMLAR:**

```
QADAM 1: Foydalanuvchini olish
═══════════════════════════════════════════════════════════
user = update.effective_user
user_id = "778165270"

QADAM 2: Mavjud foydalanuvchilarni yuklash
═══════════════════════════════════════════════════════════
users = {"old_user_id": {...}}

QADAM 3: Yangi foydalanuvchimi tekshirish
═══════════════════════════════════════════════════════════
if "778165270" not in users:
    # Yangi bo'lsa, record qo'shish
    users["778165270"] = {
        "first_name": "Otamurod",
        "latitude": None,
        "longitude": None,
        "location_name": None,
        "prayer_times": None,
        "registered_date": "2026-01-17T18:25:03..."
    }
    
    # JSON ga saqlash
    save_user_data(users)

QADAM 4: Keyboard yaratish
═══════════════════════════════════════════════════════════
keyboard = [
    [KeyboardButton(..., request_location=True)],
    [KeyboardButton("❓"), KeyboardButton("⚙️")]
]

QADAM 5: Xabar yuborish
═══════════════════════════════════════════════════════════
await update.message.reply_text(welcome_text, reply_markup=keyboard)
```

---

### 8. HANDLE LOCATION (161-233 qatorlar)

Bu funksiyada eng ko'p ish sodir bo'ladi:

```python
async def handle_location(update, context):
    try:
        # 1. LOKATSIYANI OLISH
        user_id = str(update.effective_user.id)
        location = update.message.location
        latitude = location.latitude
        longitude = location.longitude
        
        # 2. KUTISH XABARI
        await update.message.reply_text(
            "⏳ Joylashuvni aniqlanmoqda va namoz vaqtlari tayyorlanmoqda..."
        )
        
        # 3. HUDUD NOMINI OLISH (ASINXRON)
        location_name = await get_location_name(latitude, longitude)
        
        # 4. NAMOZ VAQTLARINI OLISH (ASINXRON)
        prayer_times = await get_prayer_times(latitude, longitude)
        
        if prayer_times:
            # 5. JSON DA SAQLASH
            users = load_user_data()
            users[user_id]['latitude'] = latitude
            users[user_id]['longitude'] = longitude
            users[user_id]['location_name'] = location_name
            users[user_id]['prayer_times'] = prayer_times
            save_user_data(users)
            
            # 6. JADVAL YUBORISH
            await send_daily_schedule(update, prayer_times, location_name)
            
            # 7. TASDIQLASH XABARI
            await update.message.reply_text(
                f"✅ Joylashuvingiz saqlandi!\n\n"
                f"📍 **{location_name}**\n\n"
                "Kunlik namoz jadvalini yuborib chiqdim."
            )
        else:
            # API xato bo'lgan
            await update.message.reply_text(
                "❌ Namoz vaqtlarini olishda xato yuz berdi."
            )
    
    except Exception as e:
        # XATO TUTISH
        logger.error(f"Location handleri xatosi: {e}")
        await update.message.reply_text(f"❌ Xato: {e}")
```

**PARALLEL ISHLAR:**

```
VAQT CHIZIQLı KO'RINISH:

0 soniya: get_location_name() BOSHLANADI
         │
1 soniya: get_prayer_times() BOSHLANADI
         │                      │
5 soniya: location_name KELDI   │
         │                      │
         │                      Aladhan API...
         │                      
7 soniya: prayer_times KELDI
         │
         JSON DA SAQLASH
         │
         XABAR YUBORISH

TOTAL VAQT: 7 SONIYA (EMAS 5+7=12)

ASYNC OLINGAN ODAM: Parallel so'rovlar tezraqligi!
```

---

### 9. SEND DAILY SCHEDULE (235-250 qatorlar)

```python
async def send_daily_schedule(update, prayer_times, location_name=None):
    schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"
    
    if location_name:
        schedule_text += f"\n📍 **{location_name}**\n\n"
    
    for prayer_name, prayer_time in prayer_times.items():
        schedule_text += f"🕌 {prayer_name}: {prayer_time}\n"
    
    schedule_text += "\n⏰ Siz har namoz oldidan eslatma olasiz!"
    
    await update.message.reply_text(schedule_text, parse_mode='Markdown')
```

**STRING YASASH:**

```
Boshlang'ich:
schedule_text = "📅 **Bugungi Namoz Vaqtlari**\n"

location_name = "Tashkent, ..." bo'lsa:
schedule_text += "\n📍 **Tashkent, ...**\n\n"

Natija:
📅 **Bugungi Namoz Vaqtlari**

📍 **Tashkent, Tashkent City, Uzbekistan**

Loop qilish:
prayer_times = {
    'Bomdod': '06:25',
    'Peshin': '12:34',
    ...
}

for prayer_name, prayer_time in prayer_times.items():
    schedule_text += f"🕌 Bomdod: 06:25\n"
    schedule_text += f"🕌 Peshin: 12:34\n"
    ...

FINAL TEXT:
📅 **Bugungi Namoz Vaqtlari**

📍 **Tashkent, Tashkent City, Uzbekistan**

🕌 Bomdod: 06:25
🕌 Peshin: 12:34
🕌 Asr: 15:02
🕌 Shom: 17:23
🕌 Xufton: 18:43

⏰ Siz har namoz oldidan eslatma olasiz!
```

---

## 🎯 XULOSA

Bot kodi quyidagi jarayonlar bilan ishlaydi:

```
┌──────────────────────────────────────────────┐
│ 1. IMPORTS - Kutubxonalarni yuklash          │
├──────────────────────────────────────────────┤
│ 2. SETUP - Token, fayl nomi, logging         │
├──────────────────────────────────────────────┤
│ 3. HELPER - load/save funksiyalari          │
├──────────────────────────────────────────────┤
│ 4. API CALLS - Nominatim, Aladhan           │
├──────────────────────────────────────────────┤
│ 5. HANDLERS - Telegram xabaralini ish       │
├──────────────────────────────────────────────┤
│ 6. JOB QUEUE - Avtomatik ishlar (4:00 AM)   │
├──────────────────────────────────────────────┤
│ 7. MAIN - Bot boshlanadi                    │
└──────────────────────────────────────────────┘
```

Har bir qism o'z vazifasini bajaradi va birgalikda foydalanuvchiga nomoz vaqtlarini samarali tarzda ta'minlaydi! 🕌✨
