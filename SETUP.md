# 🚀 O'rnatish va Ishga tushirish

## 1. Virtual environment yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# yoki
venv\Scripts\activate  # Windows
```

## 2. Paketlarni o'rnatish

```bash
pip install -r requirements.txt
```

## 3. Ma'lumotlar bazasini yaratish

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Superuser yaratish (Admin panel uchun)

```bash
python manage.py createsuperuser
```

Kiritilishi kerak:
- Username
- Email (ixtiyoriy)
- Password

## 5. Namuna ma'lumotlar yaratish (ixtiyoriy)

```bash
python manage.py create_sample_data
```

Bu buyruq 3 ta xona va bir nechta jumboq yaratadi.

## 6. Serverni ishga tushirish

```bash
python manage.py runserver
```

Brauzerda oching: http://127.0.0.1:8000/

## 7. Admin panelga kirish

URL: http://127.0.0.1:8000/admin/

Superuser hisobidan kirish.

## 📝 Keyingi qadamlar

1. Admin panelda xonalar va jumboqlar qo'shing
2. Yangi foydalanuvchi ro'yxatdan o'tishi mumkin
3. Foydalanuvchilar jumboqlarni yechib ball to'plashadi

## ⚠️ Eslatmalar

- Har bir jumboq uchun `correct_answer` to'g'ri kiritilishi kerak
- Javoblar kichik harflarda solishtiriladi
- Vaqt qisqa bo'lsa, ko'proq ball olinadi
- Oldingi xona tugallanmaguncha keyingi xona ochilmaydi


