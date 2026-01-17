# ☁️ BOT CLOUDGA YUKLASH - BEPUL VARIANTLAR

## 🎯 MAQSAD
Bot **24/7 ishlab turishi** uchun compyuterini yoqib qolish shart emas!

---

## 📊 BEPUL VARIANTLARNI TAQQOSLASH

| Platform | Narx | Xotira | CPU | Fayl Saqlash | Muddat | Qo'llash |
|----------|------|--------|-----|--------------|--------|---------|
| **Railway** | 📍 $5/oy free | 8GB (shared) | 0.5 CPU | 1GB | ∞ | ⭐⭐⭐ ENG OSON |
| **Render** | 🆓 Free tier | 512MB | Shared | - | 15 min (sleep) | ⭐⭐ Boshlang'ich |
| **Replit** | 🆓 Free | 512MB | Shared | 5GB | ∞ | ⭐ Juda oson |
| **PythonAnywhere** | 🆓 Free | 512MB | Shared | 512MB | ∞ | ⭐⭐ O'rta |
| **Heroku** | ❌ Bepul YOQILDI | - | - | - | - | ❌ Endi haq bilan |
| **Linode/Akamai** | 💰 $5/oy min | - | - | - | - | 💰 To'lovli |

---

## 🥇 TAVSIYA: RAILWAY.APP (ENG YAXSHI)

### ✅ **Nima uchun Railway?**
- ✅ **Haqsiz!** Ilk $5/oy bepul (bu ushbu bot uchun etarli)
- ✅ **24/7 ishlab turadi** (uyku vaqti yo'q)
- ✅ **Python 3.13 qo'llab-quvvatlaydi**
- ✅ **GitHub integratsiyasi** (auto deploy)
- ✅ **Environment variables** (TOKEN saqlash uchun)
- ✅ **Logging va monitoring** (debug qilish oson)

### 📋 SETUP (15 daqiqa)

#### 1️⃣ **GitHub orqali qayd qiling**
```
1. railway.app ga qadim yuboring
2. "Deploy with GitHub" bosing
3. GitHub akkauntingizni ulashtiring
```

#### 2️⃣ **Repositoriyani tayyorlash**
```powershell
# 1. GitHub da yangi repo quring
#    Nom: telegram-prayer-bot

# 2. Kodingizni yukla
cd "C:\Users\Otamurod Pirnapasov\Downloads\BOT"
git init
git add .
git commit -m "Telegram Prayer Times Bot"
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/telegram-prayer-bot.git
git push -u origin main
```

#### 3️⃣ **Railway da deploy qiling**
```
1. railway.app ga kiring (GitHub orqali)
2. "New Project" bosing
3. "Deploy from GitHub" tanlang
4. telegram-prayer-bot repo tanlang
5. "Deploy" bosing
```

#### 4️⃣ **Environment Variables qo'shing**
Railway dashboard da:
```
BOT_TOKEN = 8517360815:AAEchs0SAX-axPg5oo8rko3GCtSCCcjnB2M
```

#### 5️⃣ **requirements.txt yaratish**
```
python-telegram-bot[job-queue]==21.8
requests==2.31.0
```

---

## 🟡 RENDER.COM (IYUN OSON, LEKIN SLEEP VAQTI BOR)

### ⚠️ **Muammo:**
- **15 daqiqadan keyin SLEEP** bo'lib qoladi (bepul tariff)
- **Bot ishlamay qoladi** 15 min uchun
- **Keyin qayta uyanadi** (slow)

### ✅ **Afzal tarafi:**
- Juda oson setup
- GitHub integratsiyasi
- Monitoring qo'llab-quvvatlaydi

### 📋 SETUP (10 daqiqa)
```
1. render.com ga kiring
2. "New +" bosing
3. "Web Service" tanlang
4. GitHub repo ulashtiring
5. Deploy qiling
```

---

## 🔵 REPLIT (ENG OSON, LEKIN SEKIN)

### ✅ **Afzal tarafi:**
- **Web IDE** (browser orqali code o'zgartirishingiz mumkin)
- **24/7 ishlab turadi** (Replit Pro uchun)
- **Juda oson**

### ⚠️ **Muammo:**
- **Bepul tariff sekin** (sleep vaqti yo'q, lekin CPU kam)
- **Replit Pro** $7/oy

### 📋 SETUP (5 daqiqa)
```
1. replit.com ga kiring
2. "Import from GitHub" bosing
3. Repository URL ni kiritng
4. "Run" bosing
```

---

## 🟣 PYTHONANYWHERE.COM

### ✅ **Afzal tarafi:**
- **24/7 bot ishlab turadi**
- **Bepul tier bor**
- **MySQL database** (bepul)

### ⚠️ **Muammo:**
- **Web interface qiyin**
- **Deploy qiyin** (manual)
- **Setup vaqti ko'p** (45 min)

---

## 📱 ALTERNATIVE: MOBILE APP

### 📲 **Termux (Android orqali)**
Agar Android telefon bo'lsa:
```
1. Termux o'rnating
2. Python 3.13 o'rnating
3. Bot kodi yukla
4. 24/7 ishlab turadi!
```

---

## 🚀 RAILWAY ORQALI STEP-BY-STEP

### **QADAM 1: Githubda repo yarating**

Buning uchun GitHub account kerak:
1. github.com ga kiring
2. "New repository" bosing
3. Nom: `telegram-prayer-bot`
4. "Create repository" bosing

### **QADAM 2: Kod yukla**

PowerShell da:
```powershell
cd "C:\Users\Otamurod Pirnapasov\Downloads\BOT"

# Git yaratish
git init
git config user.email "sizning@email.com"
git config user.name "Sizning Ismi"

# Barcha fayl qo'shish
git add .

# Commit
git commit -m "Telegram Prayer Times Bot - Birinchi yuklash"

# GitHub ga ulash
git branch -M main
git remote add origin https://github.com/SIZNING_USERNAME/telegram-prayer-bot.git
git push -u origin main
```

### **QADAM 3: requirements.txt yaratish**

Terminal orqali:
```powershell
cd "C:\Users\Otamurod Pirnapasov\Downloads\BOT"
pip freeze > requirements.txt
```

Yoki qo'lda `requirements.txt` fayl yarating:
```
python-telegram-bot[job-queue]==21.8
requests==2.31.0
```

### **QADAM 4: Railway qo'shing**

```powershell
# Railway CLI o'rnating
npm install -g @railway/cli

# Login qiling
railway login

# Railway projectni yaratish
railway init

# Deploy qiling
railway up
```

Yoki web orqali:
1. railway.app ga kiring
2. "New Project" bosing
3. GitHub repo tanlang
4. "Deploy" bosing

### **QADAM 5: Environment Variables**

Railway dashboard:
```
BOT_TOKEN = 8517360815:AAEchs0SAX-axPg5oo8rko3GCtSCCcjnB2M
```

### **QADAM 6: Bot ishlab turganini tekshirish**

Railway logs:
```
Tekshiring: 🤖 Namoz Vaqti Boti ishga tushdi...
```

---

## 💾 CLOUD DATABASE (Opsional)

Agar JSON faylni cloud da saqlashni xohlasangiz:

### **Firebase** (Google)
```python
# Installation
pip install firebase-admin

# user_data.json o'rniga Firestore
```

### **MongoDB Atlas** (Bepul)
```python
# Installation
pip install pymongo

# JSON o'rniga NoSQL database
```

### **Supabase** (Bepul)
```python
# Installation
pip install supabase

# PostgreSQL + Real-time
```

---

## ⚡ TEZKOR TAVSIYA

**MEN TAVSIYA QILAMAN:**
1. **Railway** ← ENG YAXSHI (24/7, bepul, oson)
2. **Render** ← Agar sleep vaqti kashshani qabul qilsangiz
3. **Replit** ← Agar web IDE xohlasangiz

**BOSHLANGI UCHUN RAILWAY+GitHub KOMBINATSIYASI:**
- 0️⃣ GitHub account yaratish (5 min)
- 1️⃣ Code yukla (10 min)
- 2️⃣ Railway deploy (5 min)
- **= 20 DAQIQADA TO'LIQ ☁️**

---

## 📊 XARAJAT

| Variant | Birinchi 3 oy | Keyingi oylar |
|---------|---------------|--------------|
| **Railway** | 🆓 FREE ($5 free tier) | 🆓 FREE (agar $5 dan kam) |
| **Render** | 🆓 FREE (lekin sleep) | 🆓 FREE (lekin sleep) |
| **Replit** | 🆓 FREE | 💰 $7/oy (Replit Pro) |
| **PythonAnywhere** | 🆓 FREE | 💰 $5/oy (unlimited) |

---

## ⚠️ MUAMMOLAR VA YECHIM

### **Muammo: Bot 15 min dan keyin yupqa bo'ladi**
- **Sabab:** Render sleep mode
- **Yechim:** Railway ishlatish

### **Muammo: GitHub push qilishda xato**
```powershell
# SSH key yaratish
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

### **Muammo: TOKEN xavfsizligi**
```
❌ KOD DA TOKEN SAQLAMANG!
✅ Environment variable ishlatish
```

---

## 🎓 BONUS: DOCKER (Advanced)

Railway DOCKER ham qo'llab-quvvatlaydi:

```dockerfile
FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "telegram_bot.py"]
```

---

## 📞 YORDAM

| Muammo | Yechim |
|--------|--------|
| Railway login ishlama | `railway login --browser` |
| GitHub permission xato | GitHub settings → Developer settings → Personal access tokens |
| Bot token xavfsiz emas | Environment variable ishlatish |
| Deploy qilishda xato | Railway logs qarash: `railway logs` |

---

**XULOSA:** 🚀
```
Endi bot 24/7 ishlab turadi!
Compyuteri yoq bo'lsa ham xizmat beraydi!
```

---

**Yaratilgan:** 2026-01-17  
**Til:** O'zbek  
**Darajasi:** Boshlang'ich → Advanced
