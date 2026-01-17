# 🤖 NAMOZ VAQTI TELEGRAM BOTI

## 📌 QO'SHIMCHA DOKUMENTATSIYA

Ushbu papkada quyidagi dokumentatsion fayllar mavjud:

### 📖 1. **BOT_TUSHUNTIRISH.md** (Umumiy Tushuntirish)
Bot qanday ishlashini umumiy ko'rinishda tushuntiryapti.
- Bot jarayoni
- Data flow
- Asosiy funksiyalar
- Job Queue tushuntirish

👉 **Yangi foydalanuvchilar bu fayldan boshlashin!**

---

### 🔍 2. **KODNING_BATAFSIL_TUSHUNTIRISHI.md** (Batafsil Ko'shma)
Har bir kod qatorining batafsil tushuntirishi.
- Kutubxonalari
- Veri saqlash
- API integratsiyasi
- Handler funksiyalari
- Async/Await tushuntirish
- Real misol

👉 **Kodini chuqur tushunishni xohlaysiz bo'lsa o'qing!**

---

### 📊 3. **DIAGRAMMALAR.md** (Visual Diagrammalar)
ASCII art bilan visual diagrammalar.
- Bot jarayoni
- Handler selection
- Location yuborilishi
- Job Queue tasviri
- Async vs Synchronous
- Data flow diagram
- Memory struktura
- Error handling

👉 **Visual ko'rinishni sevdiysiz bo'lsa o'qing!**

---

### 📚 4. **FUNKSIYALAR_RO'YXATI.md** (Funksiyalar Spravka)
Har bir funksiyaning batafsil ma'lumotlari.
- Parametsrlari
- Qaytarishi
- Nima qiladisi
- Misollari

👉 **Tezda ishlashni xohlaysiz bo'lsa reference sifatida foydalaning!**

---

## 🚀 BOT ISHGA TUSHIRISH

### 1. Bot Topish
Telegramda botni qidiring: `@YourBotUsername`

### 2. /start Yuborish
Bot sizga salom beradi va keyboard ko'rsatadi

### 3. 📍 Lokatsiya Yuborish
"📍 Lokatsiyani yuborish" tugmasini bosing

### 4. ✅ Natija
Bot hudud nomini va kunlik namoz jadvalini ko'rsatadi

---

## 📁 PAPKA TUZILISHI

```
BOT/
├─ telegram_bot.py              ← ASOSIY BOT KODI
├─ user_data.json               ← FOYDALANUVCHI MA'LUMOTLARI
├─ .venv/                        ← VIRTUAL MUHIT
│  └─ Scripts/python.exe
├─ BOT_TUSHUNTIRISH.md          ← UMUMIY TUSHUNTIRISH
├─ KODNING_BATAFSIL_TUSHUNTIRISHI.md  ← BATAFSIL
├─ DIAGRAMMALAR.md              ← VISUAL DIAGRAMMALAR
├─ FUNKSIYALAR_RO'YXATI.md      ← FUNKSIYALAR SPRAVKA
└─ README.md                     ← BU FAYL
```

---

## 🎯 BOT FUNKSIYALARI

### ✅ ASOSIY FUNKSIYALAR
- [x] Lokatsiya qabul qilish
- [x] Hudud nomini olish (Reverse Geocoding)
- [x] Namoz vaqtlarini olish (Aladhan API)
- [x] Kunlik jadvalini ko'rsatish
- [x] Lokatsiyani qayta belgilash
- [x] Har kuni 4:00 AM da jadvalini yuborish

### 📋 BUYRUQLAR
| Buyruq | Nima Qiladi |
|--------|-------------|
| /start | Botni boshlash |
| /help | Yordam ko'rsatish |
| /schedule | Kunlik jadvalini ko'rish |
| /location | Joylashuvni ko'rish |

### 🔘 TUGMALAR
| Tugma | Nima Qiladi |
|-------|-------------|
| 📍 Lokatsiyani yuborish | Location so'rashi ochadi |
| ❓ Yordam | Yordam xabari yuboradi |
| ⚙️ Sozlamalar | Sozlamalari ko'rsatadi |

---

## 🔌 API INTEGRATSIYASI

### 1. **Aladhan API** - Namoz Vaqtlari
```
URL: https://api.aladhan.com/v1/timings/
METHOD: GET
PARAMETRLAR: latitude, longitude, method=2
JAVOB: Namoz vaqtlari (Bomdod, Peshin, Asr, Shom, Xufton)
```

### 2. **Nominatim API** - Reverse Geocoding
```
URL: https://nominatim.openstreetmap.org/reverse
METHOD: GET
PARAMETRLAR: lat, lon, format=json
JAVOB: Hudud nomi (shahar, viloyat, davlat)
```

---

## 💾 DATA SAQLASH

### JSON Struktura
```json
{
  "user_id": {
    "first_name": "Foydalanuvchining Ismi",
    "latitude": 40.756225,
    "longitude": 69.115157,
    "location_name": "Tashkent, Tashkent City, Uzbekistan",
    "prayer_times": {
      "Bomdod": "06:25",
      "Peshin": "12:34",
      "Asr": "15:02",
      "Shom": "17:23",
      "Xufton": "18:43"
    },
    "registered_date": "2026-01-17T18:20:53.302716"
  }
}
```

### Saqlash Joyı
- **LOCAL:** `user_data.json` (kompyuteringizda)
- **BULUNADI:** C:\Users\Otamurod Pirnapasov\Downloads\BOT\user_data.json

---

## ⚙️ TEXNIK MA'LUMOTLAR

### Python Versiyası
- Python 3.13.9

### Kerakli Kutubxonalar
```
python-telegram-bot[job-queue]
requests
```

### Virtual Muhit
```powershell
# Virtual muhitni faollash
.venv\Scripts\Activate

# Botni ishga tushirish
python telegram_bot.py
```

---

## 🐛 MUAMMOLARNI HAL QILISH

### Muammo: Bot ishlamayapti
**Yechim:**
1. Python ishga tushganmi tekshirish: `.venv\Scripts\python.exe --version`
2. Kutubxonalari tekshirish: `pip list`
3. Token to'g'rimi: `echo $env:TELEGRAM_BOT_TOKEN`

### Muammo: Location yuborish bo'lmayapti
**Yechim:**
1. Telegram Desktop da location button yok bo'lishi mumkin
2. Mobile Telegram ishlatib ko'ring
3. Keyboard tugmasini qayta bosing

### Muammo: Namoz vaqtlari xato
**Yechim:**
1. Lokatsiyani qayta belgilang
2. Internet ulanmani tekshiring
3. API javob berganmi tekshirish

---

## 🔐 XAVFSIZLIK

### Hozirgi Holatda
⚠️ **TOKEN KOD ICHIDA HARDCODED** - Xavfsiz emas!

### Tavsiyalar
1. **Environment variable dan foydalaning:**
```powershell
$env:TELEGRAM_BOT_TOKEN='your_token_here'
```

2. **`.env` fayldan yuklang:**
```python
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
```

3. **Server ga o'tkazish:**
- Firebase Realtime Database
- MongoDB Atlas
- Supabase
- AWS DynamoDB

---

## 📈 KELASI AMALIYOT

### To'plangan Funksiyalari
- [ ] Jadvalga qo'shimcha vaqt sug'urtalari
- [ ] Bot statistikasi
- [ ] Foydalanuvchi e-mail bildirishnomasi
- [ ] Web interfeys
- [ ] Admin panel

### Texnik Yaxshilanishlar
- [ ] Multilingual support (O'zbek + Ingliz)
- [ ] Database integratsiyası
- [ ] Cloud hosting
- [ ] Docker containerization
- [ ] Unit testlar

---

## 📞 YORDAM

Agar savollaringiz bo'lsa, quyidagi dokumentatsion fayllarni o'qing:

1. **Yangi bo'lsangiz:** BOT_TUSHUNTIRISH.md
2. **Kod tushunishni xohlasangiz:** KODNING_BATAFSIL_TUSHUNTIRISHI.md
3. **Visual ko'rinish:** DIAGRAMMALAR.md
4. **Tez spravka:** FUNKSIYALAR_RO'YXATI.md

---

## ✨ XULOSA

Bu Telegram bot o'zbekcha tilida ishlaydi va:
- ✅ Foydalanuvchining lokatsiyasini qabul qiladi
- ✅ Hudud nomini aytib beradi
- ✅ Kunlik namoz jadvalini ko'rsatadi
- ✅ Har kuni bomdodda avtomatik xabar yuboradi
- ✅ Foydalanuvchi ma'lumotlarini xavfsiz saqlaydi

**Bot ishga tushgan!** 🚀 Telegramda test qilishni boshlang! 📱

---

**Yaratilgan:** 2026-01-17  
**Mualliflar:** AI Programming Assistant  
**Versiya:** 1.0  
**Til:** O'zbek + Ingliz

🕌 Namoz jadvalini sotishtirsangiz, muvaffaq bo'lishingiz munajjazat! 🕌
