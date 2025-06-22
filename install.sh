#!/bin/bash
# === تثبيت كل متطلبات مشروع UNICH-REF تلقائياً ===

# 1. التأكد من وجود بايثون 3
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 غير مثبت. يرجى تثبيته عبر: sudo apt install python3 python3-pip python3-venv"
    exit
fi

# 2. إنشاء البيئة الافتراضية
echo "[*] إنشاء بيئة افتراضية..."
python3 -m venv venv

# 3. تفعيل البيئة الافتراضية
source venv/bin/activate

# 4. تحديث pip و setuptools
echo "[*] تحديث pip و setuptools..."
pip3 install --upgrade pip setuptools

# 5. تثبيت جميع المكتبات المطلوبة
echo "[*] تثبيت المكتبات من requirements.txt..."
pip3 install -r requirements.txt

# 6. تنزيل ChromeDriver تلقائياً (عبر webdriver-manager)
echo "[*] تنزيل ChromeDriver تلقائياً..."
python3 -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"

# 7. تنبيه للمتطلبات الخارجية
echo "[!] تأكد من وجود Google Chrome على جهازك."
echo "[!] إذا أردت حل الكابتشا تلقائياً، ضع مفتاح 2Captcha في config.py."
echo "[!] إذا أردت قراءة OTP تلقائياً من Gmail، فعّل App Password في بريدك."

echo "[*] تم التثبيت بنجاح! لتشغيل السكربت استخدم ./run.sh أو:"
echo "python3 main.py"

echo "========================================"
echo "UNICH-REF Automation Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python version $python_version is too old. Required: $required_version or higher"
    exit 1
fi

echo "Python $python_version found. Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo
echo "To run the automation:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the script: python main.py"
echo 