# راهنمای راه‌اندازی ربات سیگنال کریپتو
## نحوه اجرا روی سیستم شخصی

### پیش‌نیازها (Prerequisites)

#### 1. نصب Python
```bash
# روی Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip

# روی macOS (با Homebrew):
brew install python3

# روی Windows:
# Python را از python.org دانلود و نصب کنید
```

#### 2. نصب Git
```bash
# روی Ubuntu/Debian:
sudo apt install git

# روی macOS:
brew install git

# روی Windows:
# Git را از git-scm.com دانلود کنید
```

### مراحل نصب و راه‌اندازی

#### مرحله 1: دانلود پروژه
```bash
# کلون کردن یا دانلود فایل‌های پروژه
git clone [repository-url]
cd crypto-signal-bot

# یا اگر فایل‌ها را دستی دانلود کرده‌اید:
cd path/to/crypto-signal-bot
```

#### مرحله 2: ساخت محیط مجازی Python
```bash
# ساخت محیط مجازی
python3 -m venv crypto_bot_env

# فعال کردن محیط مجازی:
# روی Linux/macOS:
source crypto_bot_env/bin/activate

# روی Windows:
crypto_bot_env\Scripts\activate
```

#### مرحله 3: نصب وابستگی‌ها
```bash
# نصب پکیج‌های مورد نیاز
pip install fastapi aiohttp uvicorn apscheduler

# یا استفاده از فایل requirements.txt:
pip install -r requirements.txt

# نصب پکیج‌های اضافی مورد نیاز:
pip install ccxt pandas numpy requests ta
```

#### مرحله 4: راه‌اندازی API کلیدهای Binance (اختیاری)
برای استفاده کامل از ربات، نیاز به API کلیدهای Binance دارید:

1. وارد حساب Binance خود شوید
2. به قسمت API Management بروید
3. یک API Key جدید ایجاد کنید
4. مجوزهای "Read" را فعال کنید (برای تحلیل فقط)

```python
# در فایل crypto_bot_enhanced (1).py خط 20-25:
# API کلیدهای خود را اینجا وارد کنید
api_key = "YOUR_BINANCE_API_KEY"
api_secret = "YOUR_BINANCE_API_SECRET"
```

### روش‌های اجرا

#### روش 1: اجرای وب اپلیکیشن (پیشنهادی)
```bash
# اجرای سرور FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

# یا با reload برای توسعه:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

سپس به آدرس `http://localhost:8000` بروید

#### روش 2: اجرای مستقیم ربات
```bash
# اجرای مستقیم فایل ربات
python crypto_bot_enhanced\ \(1\).py
```

#### روش 3: اجرای در پس‌زمینه
```bash
# اجرای در پس‌زمینه روی Linux/macOS:
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &

# یا استفاده از screen:
screen -S crypto_bot
uvicorn main:app --host 0.0.0.0 --port 8000
# سپس Ctrl+A+D برای جدا شدن از session
```

### پیکربندی

#### تنظیم زمان‌بندی تحلیل
در فایل `scheduler.py` خط 11:
```python
# تغییر فاصله زمانی تحلیل (به دقیقه)
scheduler.add_job(job, 'interval', minutes=5)  # هر 5 دقیقه
```

#### انتخاب جفت ارزهای مورد نظر
در فایل `crypto_bot_enhanced (1).py` خط 29-33:
```python
self.trading_pairs = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT',
    'MATIC/USDT', 'AVAX/USDT', 'DOT/USDT', 'LINK/USDT',
    # ارزهای دلخواه خود را اضافه کنید
]
```

### نظارت و استفاده

#### مشاهده وضعیت ربات
- آدرس API: `http://localhost:8000`
- مشاهده سیگنال‌ها در کنسول/terminal

#### مشاهده لاگ‌ها
```bash
# مشاهده لاگ‌های زنده
tail -f logs/crypto_bot.log  # اگر لاگ فایل تنظیم شده باشد
```

### عیب‌یابی مشکلات رایج

#### خطای نصب پکیج‌ها
```bash
# ارتقای pip
pip install --upgrade pip

# نصب با verbose برای مشاهده جزئیات خطا
pip install -v package_name
```

#### خطای اتصال به Binance
- بررسی اتصال اینترنت
- بررسی صحت API کلیدها
- بررسی محدودیت‌های IP در تنظیمات Binance

#### خطای پورت در حال استفاده
```bash
# تغییر پورت
uvicorn main:app --host 0.0.0.0 --port 8001

# یا کشتن پروسه‌های در حال اجرا روی پورت 8000
sudo lsof -t -i tcp:8000 | xargs kill -9
```

### امنیت

⚠️ **نکات امنیتی مهم:**
- هرگز API کلیدهای خود را در فایل‌های عمومی قرار ندهید
- از متغیرهای محیطی برای API کلیدها استفاده کنید
- فقط مجوزهای "Read" را فعال کنید (نه Trading)
- فایروال و آنتی‌ویروس خود را فعال نگه دارید

### پشتیبانی

برای مشکلات فنی:
1. ابتدا بخش عیب‌یابی را بررسی کنید
2. لاگ‌های خطا را کامل بخوانید
3. نسخه Python و پکیج‌ها را بررسی کنید

---

**توجه:** این ربات صرفاً برای تحلیل و ارائه سیگنال است. قبل از هر تصمیم‌گیری مالی، تحقیقات کافی انجام دهید.

---

## English Summary

### Quick Setup Guide for Crypto Signal Bot

This is a cryptocurrency analysis bot built with FastAPI that provides trading signals based on technical analysis.

**Prerequisites:**
- Python 3.7+
- Internet connection

**Quick Setup:**
```bash
# 1. Create virtual environment
python3 -m venv crypto_bot_env
source crypto_bot_env/bin/activate  # Linux/macOS
# or: crypto_bot_env\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the bot
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Access:** Open `http://localhost:8000` in your browser

**Features:**
- Real-time crypto market analysis
- Multiple technical indicators
- Smart Money Concepts (SMC)
- Volume analysis
- Automated signal generation every 5 minutes
- Support for 12+ trading pairs

**Optional:** Add your Binance API keys in `crypto_bot_enhanced (1).py` for enhanced functionality (read-only permissions recommended).

**Note:** This bot is for analysis purposes only. Always do your own research before making financial decisions.