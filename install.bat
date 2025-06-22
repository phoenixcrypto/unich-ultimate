@echo off
REM === تثبيت كل متطلبات مشروع UNICH-REF تلقائياً ===

REM 1. التأكد من وجود بايثون
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python غير مثبت. يرجى تثبيته من https://www.python.org/downloads/
    pause
    exit /b
)

REM 2. إنشاء البيئة الافتراضية
echo [*] إنشاء بيئة افتراضية...
python -m venv venv

REM 3. تفعيل البيئة الافتراضية
call venv\Scripts\activate

REM 4. تحديث pip و setuptools
echo [*] تحديث pip و setuptools...
python -m pip install --upgrade pip setuptools

REM 5. تثبيت جميع المكتبات المطلوبة
echo [*] تثبيت المكتبات من requirements.txt...
pip install -r requirements.txt

REM 6. تنزيل ChromeDriver تلقائياً (عبر webdriver-manager)
echo [*] تنزيل ChromeDriver تلقائياً...
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

REM 7. تنبيه للمتطلبات الخارجية
echo [!] تأكد من وجود Google Chrome على جهازك.
echo [!] إذا أردت حل الكابتشا تلقائياً، ضع مفتاح 2Captcha في config.py.
echo [!] إذا أردت قراءة OTP تلقائياً من Gmail، فعّل App Password في بريدك.

echo [*] تم التثبيت بنجاح! لتشغيل السكربت استخدم run.bat أو:
echo python main.py
pause 