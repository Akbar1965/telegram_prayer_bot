# 🟣 REPLIT ORQALI BOT DEPLOY - STEP BY STEP

## 🎯 MAQSAD
Bot **24/7 ishlab turadi**, compyuter yoq bo'lsa ham! Bepul va oson!

---

## ⏱️ JAMI VAQTI: 30 DAQIQA

### Arafka:
- **Replit account** → 5 min
- **Kod upload** → 10 min
- **Deploy** → 5 min
- **Test** → 5 min
- **Uya** → 5 min

---

## 📋 CHECKLIST

- [ ] Replit.com ga reg qiling
- [ ] Python project yarating
- [ ] Kod yukla
- [ ] requirements.txt qo'shing
- [ ] Bot ishlab turganini tekshiring
- [ ] Always on (Replit Pro) yoki Keep Alive script
- [ ] Tayyoq! 24/7 ✅

---

# 🚀 QADAM-QADAM

## QADAM 1: REPLIT.COM GA RO'YXATDAN O'TISH (5 MIN)

### 1.1 Replit.com ga kiring
```
https://replit.com
```

### 1.2 "Sign Up" bosing

**Email orqali:**
```
Email: sizning@email.com
Password: Kuchli parol (123456 emas!)
```

**Yoki Google orqali:**
```
"Sign up with Google" → Google account tanlang → Done!
```

### 1.3 Verify email (agar email orqali bo'lsa)
```
Email kutib oling → Link bosing → Tayyor!
```

---

## QADAM 2: PYTHON PROJECT YARATISH (5 MIN)

### 2.1 Dashboard da "Create Repl" bosing

```
1. replit.com dashboard (anasahifa)
2. "+ Create" yoki "Create Repl" bosing
3. Qidirish: "Python"
4. Python tanlang
```

### 2.2 Nomi va ombori

```
Name: telegram-prayer-bot
(Boshqa nom ham bo'lsa bo'ladi)
```

### 2.3 "Create Repl" bosing

**Kuting 30 sekund...**
```
IDE ochiladi → Tayyor!
```

---

## QADAM 3: KOD YUKLASH (10 MIN)

### 3.1 Kompyuterdan kod ko'chir

```
C:\Users\Otamurod Pirnapasov\Downloads\BOT
```

Bu fayllarni nusxalash kerak:
- ✅ telegram_bot.py
- ✅ user_data.json

### 3.2 Replit Files da

**LEFT SIDE:** Files panel
```
1. "Files" (chap taraf)
2. "main.py" faylni o'ching
3. O'rniga telegram_bot.py ni nusxala
```

### VARIANT A: COPYPASTE (eng oson)

```
1. telegram_bot.py ni kompyuterda oching
2. Barcha kodni CTRL+A → CTRL+C
3. Replit main.py ni oching
4. Barcha CTRL+A → Delete
5. CTRL+V paste qiling
6. CTRL+S save qiling
```

### VARIANT B: UPLOAD

```
1. Files panel → Upload
2. telegram_bot.py ni tanlang
3. Upload bosing
4. main.py ni o'ching → telegram_bot.py dan ko'chir → save
```

### 3.3 user_data.json ni qo'shing

```
1. Files panel → "+"
2. "Create file"
3. Nomi: user_data.json
4. Kontenti:
```

```json
{
  "778165270": {
    "first_name": "Test",
    "latitude": 40.756225,
    "longitude": 69.115157,
    "location_name": "Toshkent, Oʻzbekiston",
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

---

## QADAM 4: requirements.txt YARATISH (5 MIN)

### 4.1 Replit da "+" bosing

```
1. Files panel
2. "+" icon
3. "Create file"
4. Nomi: requirements.txt
```

### 4.2 Kontenti (Copy-paste qiling):

```
python-telegram-bot[job-queue]==21.8
requests==2.31.0
```

**Oyna:**
```
python-telegram-bot[job-queue]==21.8
requests==2.31.0
```

### 4.3 Save (CTRL+S)

---

## QADAM 5: PACKAGE O'RNATISH (3 MIN)

### 5.1 RIGHT SIDE: Console

```
Replit da right side da "Console" tab bor
```

### 5.2 O'rnatish

Terminal da yozing:

```bash
pip install -r requirements.txt
```

**WAIT...**
```
Collecting python-telegram-bot[job-queue]==21.8
Collecting requests==2.31.0
Installing collected packages...
Successfully installed...
```

**Tayyor!** ✅

---

## QADAM 6: BOT ISHLATISH (5 MIN)

### 6.1 "Run" bosing

```
Replit TOP DA GREEN "Run" button
```

**WAIT 5 SEKUND...**

### 6.2 Console OUTPUT da ko'rasiz:

```
🤖 Namoz Vaqti Boti ishga tushdi...
INFO:root:Bot started successfully
```

**✅ TAYYOR!** Bot ishlab turadi!

### 6.3 Telegramda test qiling

```
1. Bot qidiring: @PrayerTimesBot_SIZNING_USERNAME
2. /start yuboring
3. Lokatsiya yuboring
4. ✅ Javob olasiz!
```

---

## QADAM 7: 24/7 ISHLAB TURISHI (KEEP ALIVE)

### ⚠️ MUAMMO:
Replit **BEPUL** versiyada bot **30 daqiqadan keyin** shut down bo'ladi (agar heched qilmasa).

### ✅ YECHIM: Keep Alive script

### 7.1 "keep_alive.py" fayl yarating

```
1. Files panel
2. "+"
3. "Create file"
4. Nomi: keep_alive.py
```

### 7.2 Kontenti (Copy-paste):

```python
from flask import Flask
from threading import Thread
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot 24/7 ishlab turibdi!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Bot yupqa bo'lmasligi uchun har 5 minutda ping yuborish"""
    while True:
        try:
            requests.get('http://localhost:8080/')
            print("✅ Keep-Alive: Bot hali-ham ishlab turadi!")
        except:
            print("⚠️ Keep-Alive: Xato, lekin bot ishlab turadi")
        time.sleep(300)  # 5 minutdan keyin

def start_keep_alive():
    """Alohida thread da Flask serverini ishga tushirish"""
    thread = Thread(target=run_flask, daemon=True)
    thread.start()
    
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()

if __name__ == '__main__':
    start_keep_alive()
```

### 7.3 main.py ga qo'shish

**main.py (telegram_bot.py) boshidagi import laridan OLDIN:**

```python
# Keep Alive (Replit uchun)
try:
    from keep_alive import start_keep_alive
    start_keep_alive()
    print("✅ Keep Alive script ishga tushdi")
except:
    print("⚠️ Keep Alive script bilalmadi, lekin bot ishlab turibdi")
```

### 7.4 requirements.txt ni yangilash

```
python-telegram-bot[job-queue]==21.8
requests==2.31.0
flask==3.0.0
```

**Pip reinstall qiling:**
```bash
pip install -r requirements.txt
```

---

## QADAM 8: FINAL TEST (5 MIN)

### 8.1 Replit da RUN bosing

```
GREEN "Run" button → Tekshiring
```

**Konsol da:**
```
✅ Keep Alive script ishga tushdi
🤖 Namoz Vaqti Boti ishga tushdi...
```

### 8.2 Telegramda test

```
1. Bot topish: @YourBotUsername
2. /start
3. Lokatsiya yuboring
4. ✅ Javob olish
```

### 8.3 Browser da check (optional)

```
Replit konsol da URL ko'rasiz:
https://telegram-prayer-bot.replit.dev

Uni oching → "✅ Bot 24/7 ishlab turibdi!"
```

---

## QADAM 9: ALWAYS ON (Replit Pro) - IXTIYORIY

### 9.1 24/7 100% qo'llab-quvvatlash uchun

```
Replit PRO: $7/oy (Ixtiyoriy)
```

**Manfaat:**
- ✅ Bot hiç qachon shut down bo'lmaydi
- ✅ Keep Alive script shart emas
- ✅ Tezkor

### 9.2 Yoki bepul qoldiring

```
Keep Alive script + Bepul = 24/7 ✅
```

---

# 📊 TAQQOSLASH

| Funksiya | Bepul + Keep Alive | Replit Pro |
|----------|-------------------|-----------|
| 24/7 ishlab turadi | ✅ Ha | ✅ Ha |
| Narxi | 🆓 Bepul | 💰 $7/oy |
| Setup | ⭐⭐ O'rta | ⭐ Oson |
| Performance | ⭐⭐ Norma | ⭐⭐⭐ Tez |

---

# 🎯 FILE STRUKTURASI

**Replit da bu fayllar bo'lishi kerak:**

```
📁 telegram-prayer-bot (Replit Project)
├── 📄 main.py (telegram_bot.py nusxasi)
├── 📄 keep_alive.py (Keep alive script)
├── 📄 requirements.txt (Packages)
├── 📄 user_data.json (Foydalanuvchi data)
└── 📁 .replit (Replit config - avtomatik)
```

---

# ⚠️ MUAMMOLAR VA YECHIM

## Muammo 1: "ModuleNotFoundError: No module named 'telegram'"

**Yechim:**
```bash
pip install -r requirements.txt
```

**Tekshiring:**
```bash
pip list | grep telegram
```

---

## Muammo 2: Bot ishlamayapti / Error ko'rinishi

**Yechim:**
```bash
# Replit Console da:
python main.py
```

**Xato ko'ring → Fix qiling**

---

## Muammo 3: "Token noto'g'ri"

**Yechim:**
```
1. main.py oching
2. TOKEN = "8517360815:AAEchs0SAX-axPg5oo8rko3GCtSCCcjnB2M"
3. CTRL+S save
4. Run bosing
```

---

## Muammo 4: Bot 30 min dan keyin yupqa

**Yechim:**
```
Keep Alive script qo'shing (QADAM 7)
```

---

# 💡 TIPS & TRICKS

### Replit dan GitHub ga ulash (Sync)

```bash
git init
git add .
git commit -m "Telegram Prayer Bot on Replit"
git remote add origin https://github.com/USERNAME/telegram-prayer-bot.git
git push -u origin main
```

### Logs ko'rish

```bash
tail -f output.log
```

### Bot restart qiling

```bash
# Run tugmasini bosing
# Yoki Console da CTRL+C → python main.py
```

---

# 🎓 BONUS: ADVANCED

### Secrets/Environment Variables

Agar token xavfsizligini xohlasangiz:

```
1. Replit: Secrets button (🔒)
2. Key: BOT_TOKEN
3. Value: 8517360815:AAEchs0SAX-axPg5oo8rko3GCtSCCcjnB2M
4. code da: os.environ.get('BOT_TOKEN')
```

---

# ✅ FINAL CHECKLIST

- [ ] Replit account yaratdim
- [ ] Python project yaratdim
- [ ] telegram_bot.py kodni yukla
- [ ] user_data.json kodni yukla
- [ ] requirements.txt kodni yukla
- [ ] Pip o'rnatdim
- [ ] Bot ishlab turganini tekshirdim
- [ ] Keep Alive script qo'shdi
- [ ] Telegramda test qildim
- [ ] ✅ 24/7 ishlab turadi!

---

# 📞 YORDAM

| Xato | Yechim |
|------|--------|
| Bot ishlamayapti | Console logs ko'rish |
| Token xato | TOKEN ni check qiling |
| 30 min yupqa | Keep Alive script qo'shish |
| Module not found | `pip install -r requirements.txt` |
| Port busy | Replit restart qiling |

---

# 🎉 NATIJA

```
✅ Bot REPLIT da 24/7 ishlab turadi!
✅ Compyuter yoq bo'lsa ham OK!
✅ Telegramda har vaqt ishlaydi!
✅ BEPUL! (Keep Alive + Bepul Replit)
```

---

**MUVAFFAQIYAT!** 🚀🕌

Savollaringiz bo'lsa, ushbu faylni qayta o'qing yoki ask qiling!

---

**Yaratilgan:** 2026-01-17  
**Til:** O'zbek  
**Darajasi:** Yangi boshlagich
