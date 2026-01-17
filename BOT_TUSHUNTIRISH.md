# 🤖 NAMOZ VAQTI BOTI - KODNING ISHCHI MEXANIZMI

## 📋 UMUMIY TUZILISH

```
┌─────────────────────────────────────────────────────────┐
│           TELEGRAM BOT ASOSIY JARAYON                   │
└─────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  1. Foydalanuvchi /start yubor-       │
        │     yapmaqda                          │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  2. start() FUNKSIYASI ISHGA TUSHAR   │
        │     - Keyboard tugmalar ko'rsatadi     │
        │     - Foydalanuvchini JSON da saqladi │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  3. Foydalanuvchi 📍 LOKATSIYA        │
        │     TUGMASINI BOSADI                  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  4. handle_location() ISHGA TUSHAR    │
        └───────────────────────────────────────┘
```

---

## 🔧 ASOSIY FUNKSIYALAR VA ULARNING ISHCHI JARAYONI

### 1️⃣ FOYDALANUVCHI MA'LUMOTLARI (JSON FAYL)
```
load_user_data() - Ma'lumotni o'qish
save_user_data() - Ma'lumotni yozish

JSON STRUKTURA:
{
  "user_id": {
    "first_name": "Ism",
    "latitude": 40.756225,        ← Joylashuvning kengligi
    "longitude": 69.115157,       ← Joylashuvning uzunligi
    "location_name": "Tashkent",  ← Shahar nomi
    "prayer_times": {
      "Bomdod": "06:25",
      "Peshin": "12:34",
      "Asr": "15:02",
      "Shom": "17:23",
      "Xufton": "18:43"
    },
    "registered_date": "2026-01-17..."
  }
}
```

---

### 2️⃣ LOKATSIYA YUBORILGANDA NIMA SODIR BO'LADI?

```
STEP 1: handle_location() CHAQIRILADI
├─ Foydalanuvchining ID sini oladi
├─ Latitude va Longitude ni oladi
└─ Error handling (xatolarni tekshiradi)

STEP 2: get_location_name() - HUDUD NOMINI OLISH
├─ OpenStreetMap API ga so'rov yuboradi
│  URL: https://nominatim.openstreetmap.org/reverse
│  PARAMETRLAR: latitude, longitude
├─ API javob beradi: "Tashkent, Tashkent City, Uzbekistan"
└─ Hudud nomini foydalanuvchiga ko'rsatadi

STEP 3: get_prayer_times() - NAMOZ VAQTLARINI OLISH
├─ Aladhan API ga so'rov yuboradi
│  URL: https://api.aladhan.com/v1/timings
│  PARAMETRLAR: latitude, longitude, method=2
├─ API javob beradi:
│  {
│    "Bomdod": "06:25",
│    "Peshin": "12:34",
│    "Asr": "15:02",
│    "Shom": "17:23",
│    "Xufton": "18:43"
│  }
└─ Vaqtlarni JSON da saqlaydi

STEP 4: send_daily_schedule() - JADVALINI YO'NATISH
├─ Kunlik namoz jadvalini formatlaydi
│  📅 Bugungi Namoz Vaqtlari
│  📍 Tashkent, Tashkent City, Uzbekistan
│  🕌 Bomdod: 06:25
│  🕌 Peshin: 12:34
│  ...
└─ Foydalanuvchiga xabar yuboradi

STEP 5: JSON FAYLGA SAQLASH
└─ Barcha ma'lumotlar user_data.json da saqlanadi
```

---

### 3️⃣ KEYBOARDS VA TUGMALAR

#### REGULAR KEYBOARD (Text tugmalari):
```python
[
  [KeyboardButton("📍 Lokatsiyani yuborish", request_location=True)],
  [KeyboardButton("❓ Yordam"), KeyboardButton("⚙️ Sozlamalar")]
]

👇 ISHCHI JARAYON:
├─ "📍 Lokatsiyani yuborish" → handle_location()
├─ "❓ Yordam" → handle_text_message() → help_command()
└─ "⚙️ Sozlamalar" → handle_text_message() → settings
```

---

### 4️⃣ BUYRUQLAR (COMMANDS)

```
/start → start()
├─ Foydalanuvchini qayd qiladi
├─ Keyboard ko'rsatadi
└─ Salomi yuboradi

/help → help_command()
├─ Yordam ma'lumotlarini ko'rsatadi
└─ Bot funksiyalarini tushuntiradi

/schedule → schedule_command()
├─ JSON dan prayer_times ni o'qiydi
└─ Kunlik jadvalini ko'rsatadi

/location → location_command()
├─ JSON dan location_name ni o'qiydi
└─ Saqlangan lokatsiyani ko'rsatadi
```

---

### 5️⃣ JOB QUEUE - AVTOMATIK ISHLAR

```
JOBQUEUE - Har kuni shuning bilan sodir bo'ladi:

4:00 AM → send_morning_schedule() CHAQIRILADI
│
├─ Barcha foydalanuvchilarni loop qiladi
├─ Har birining lokatsiyasi bo'yicha namoz vaqtlarini qayta oladi
├─ Kunlik jadvalini yangi vaqtlar bilan tayorlaydi
├─ Har bir foydalanuvchiga xabar yuboradi
│  📅 Bugungi Namoz Vaqtlari
│  📍 Joylashuvingiz
│  🕌 Bomdod: 06:25
│  ...
└─ Yangi pray_times JSON da o'zgaradi
```

---

## 🔄 VERI OQIMI (DATA FLOW)

```
TELEGRAM SERVER
    ↓
Foydalanuvchi xabar yuboradi
    ↓
BOT UPDATES QABUL QILADI
    ↓
HANDLER TANLANADI
├─ MessageHandler(filters.LOCATION)    → handle_location()
├─ CommandHandler("start")             → start()
├─ CommandHandler("help")              → help_command()
├─ MessageHandler(filters.TEXT)        → handle_text_message()
└─ CallbackQueryHandler()              → button_callback()
    ↓
FUNKSIYA ISHGA TUSHAR
    ↓
EXTERNAL API CHAQIRILADI (agar kerak)
├─ Nominatim API (hudud nomi)
├─ Aladhan API (namoz vaqtlari)
└─ Requests kutubxonasi orqali
    ↓
JAVOB OLINADI VA QAYTA ISHLANADI
    ↓
JSON FAYLGA SAQLASH
    ↓
FOYDALANUVCHIGA XABAR YO'NATISH
    ↓
TELEGRAM SERVER
    ↓
FOYDALANUVCHINING TELEGRAMIGA CHIQADI
```

---

## 🌐 API INTEGRATSIYASI

### ALADHAN API - Namoz Vaqtlari
```
REQUEST:
GET https://api.aladhan.com/v1/timings/1705537200?latitude=40.756&longitude=69.115&method=2

RESPONSE:
{
  "code": 200,
  "status": "OK",
  "data": {
    "timings": {
      "Fajr": "06:25",
      "Dhuhr": "12:34",
      "Asr": "15:02",
      "Maghrib": "17:23",
      "Isha": "18:43"
    }
  }
}

NIMA QILADI:
- Lokatsiya bo'yicha namoz vaqtlarini hisoblaydi
- Method 2 = ISNA metodi (Shimoliy Amerika)
- Har kunlik vaqtlar boshqacha
```

### NOMINATIM API - Reverse Geocoding
```
REQUEST:
GET https://nominatim.openstreetmap.org/reverse?lat=40.756&lon=69.115&format=json

RESPONSE:
{
  "address": {
    "city": "Tashkent",
    "state": "Tashkent City",
    "country": "Uzbekistan"
  }
}

NIMA QILADI:
- Koordinatalardan hudud nomini topadi
- Shahar, viloyat, davlatni ko'rsatadi
- Foydalanuvchiga o'qish mumkin bo'lgan nomi beradi
```

---

## 📁 FAYLLAR TUZILISHI

```
BOT_PAPKA/
├─ telegram_bot.py       ← Asosiy bot kodi (517 qator)
├─ user_data.json        ← Foydalanuvchi ma'lumotlari (LOCAL)
├─ .venv/                ← Python virtual muhiti
│  └─ Scripts/python.exe ← Bot ishga tushadigan Python
└─ requirements.txt      ← Kutubxonalar (ixtiyoriy)
```

---

## 🔐 XAVFSIZLIK

```
HOZIRGI HOLATDA:
✅ Lokatsiya - Foydalanuvchining kompyuterida (LOCAL)
✅ Namoz vaqtlari - JSON faylda (LOCAL)
✅ API lar - HTTPS orqali (ENCRYPTED)
⚠️  Token - KOD ICHIDA (XAVFSIZ EMAS)

TAVSIYALAR:
1. Token environment variable da saqlang
2. user_data.json ni server ga ko'chiring
3. HTTPS dan foydalaning
```

---

## ⚠️ XATOLARNI QANDAY TUTADI

```
try - except bloglari bilan xatolar tutiladi:

try:
    API ga so'rov yuboradi
    Javobni qayta ishlanadi
except Exception as e:
    logger.error(f"Xato: {e}")
    Foydalanuvchiga xabar yuboradi: "❌ Xato yuz berdi"
    Muammoni terminal da log qiladi
```

---

## 📊 MISOL: FOYDALANUVCHI LOKATSIYA YUBORGANDA

```
QADAMLAR:

1. Foydalanuvchi: "📍 Lokatsiyani yuborish" bosadi
   └─ Telegram: Lokatsiya so'rashi ko'rsatadi

2. Foydalanuvchi: Lokatsiyasini yuboradi
   └─ Update object: location(40.756, 69.115)

3. Bot: handle_location() chaqiriladi
   └─ ⏳ "Joylashuvni aniqlanmoqda..." xabari

4. Bot: get_location_name() ishga tushar
   ├─ Nominatim API ga so'rov
   └─ Javob: "Tashkent City, Uzbekistan"

5. Bot: get_prayer_times() ishga tushar
   ├─ Aladhan API ga so'rov
   └─ Javob: Bomdod: 06:25, Peshin: 12:34, ...

6. Bot: send_daily_schedule() ishga tushar
   └─ Jadval formatllanadi va yuboriladi

7. Bot: save_user_data() ishga tushar
   └─ user_data.json da saqlandi

8. Xabar: "✅ Joylashuvingiz saqlandi!"
   └─ Foydalanuvchiga ko'rsatiladi

9. Keyin: Har kuni 4:00 AM da send_morning_schedule()
   └─ Kunlik jadval avtomatik yuboriladi
```

---

## 🚀 XULOSA

Bot quyidagi jarayonlar bilan ishlaydi:

1. **Telegram Message** → Bot receives
2. **Handler Selection** → Qaysi funksiya ishga tusadi
3. **API Requests** → External API lardan ma'lumot oladi
4. **Data Processing** → Ma'lumotni qayta ishlaydi
5. **File Storage** → JSON da saqlaydi
6. **User Response** → Xabar yuboradi
7. **Scheduled Tasks** → Har kuni avtomatik ishlar

Shuning natijasida foydalanuvchi har kunning bomdodida namoz jadvalini oladi! 📅🕌
