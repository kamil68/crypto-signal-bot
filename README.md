# 🤖 سیستم سیگنال ارز دیجیتال - نسخه فارسی
# Crypto Signal Bot - Persian Edition

سیستم کامل و پیشرفته تحلیل و سیگنال گیری ارز دیجیتال با رابط کاربری فارسی زیبا

## ✨ ویژگی ها

- 🔍 **تحلیل پیشرفته**: تحلیل تکنیکال کامل با Smart Money Concepts
- 📊 **داشبورد فارسی**: رابط زیبا و کاربرپسند به زبان فارسی
- 🤖 **خودکار**: تحلیل خودکار هر 5 دقیقه
- 📈 **سیگنال های دقیق**: سیگنال های خرید و فروش با نقاط ورود و خروج
- 🧠 **شاخص ترس و طمع**: نمایش حس کلی بازار
- 📱 **واکنش گرا**: سازگار با موبایل و دسکتاپ

## 🚀 نحوه استفاده

### 1. نصب بسته ها
```bash
pip install -r requirements.txt
```

### 2. تست سیستم
```bash
python test_signals.py
```

### 3. اجرای کامل سیستم
```bash
python run_all.py
```

## 🌐 دسترسی ها

پس از اجرا، به آدرس های زیر مراجعه کنید:

- **Bot اصلی**: http://localhost:8000
- **داشبورد فارسی**: http://localhost:8001  
- **مستندات API**: http://localhost:8000/docs

## 📊 جفت ارزهای تحلیل شده

- BTC/USDT, ETH/USDT, SOL/USDT
- ADA/USDT, MATIC/USDT, AVAX/USDT
- DOT/USDT, LINK/USDT, DOGE/USDT
- XRP/USDT, BNB/USDT, ATOM/USDT

## 🔧 پیکربندی

می‌توانید API Key های Binance خود را در متغیرهای محیطی تنظیم کنید:

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

## 📁 ساختار فایل ها

- `main.py` - سرور اصلی FastAPI
- `signals.py` - منطق تحلیل سیگنال ها (فارسی)
- `dashboard.py` - داشبورد فارسی
- `scheduler.py` - زمانبند تحلیل ها
- `crypto_bot_enhanced (1).py` - هسته اصلی bot
- `run_all.py` - اجرای کامل سیستم
- `test_signals.py` - تست های سیستم

## 🎯 ویژگی های پیشرفته

- **تحلیل حجم معاملات**: شناسایی Volume Spike ها
- **Order Block Detection**: تشخیص نواحی مهم Smart Money
- **تحلیل Divergence**: تشخیص واگرایی های RSI و MACD
- **Risk Management**: محاسبه نقاط Stop Loss و Take Profit
- **Signal Tracking**: پیگیری وضعیت سیگنال های فعال

## ⚠️ هشدار

این ابزار صرفاً جهت تحلیل و آموزش است. لطفاً قبل از هر تصمیم مالی، تحقیقات کاملی انجام دهید.

---

💡 **نکته**: برای بهترین عملکرد، اتصال اینترنت پایدار مورد نیاز است.

🔄 **به‌روزرسانی**: سیستم هر 5 دقیقه به‌طور خودکار به‌روزرسانی می‌شود.
