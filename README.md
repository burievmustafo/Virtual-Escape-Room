# 🧩 Jumboq O'yini

Django asosida yaratilgan interaktiv jumboq o'yini. Foydalanuvchilar xonalarga kirib, jumboqlarni yechib, ball to'plashadi.

## ✨ Funksiyalar

- 👤 **Foydalanuvchi autentifikatsiyasi** - Login/Register
- 🗝️ **Xonalar (Rooms)** - Har bir xonada maxsus jumboqlar
- 🧩 **Jumboqlar** - Turli xil jumboq turlari (matematika, mantiqiy, so'z, xotira, naqsh)
- ⏱️ **Vaqt hisoblash** - Har bir jumboq uchun vaqt kuzatiladi
- 🏅 **Ball tizimi** - Vaqtga qarab ball beriladi
- 📊 **Statistika** - Foydalanuvchi statistikasi va progress
- 🔒 **Xona qulfi** - Oldingi xona tugallanmaguncha keyingi xona ochilmaydi

## 🚀 O'rnatish

1. **Virtual environment yaratish:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Kerakli paketlarni o'rnatish:**
```bash
pip install -r requirements.txt
```

3. **Ma'lumotlar bazasini yaratish:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Superuser yaratish:**
```bash
python manage.py createsuperuser
```

5. **Serverni ishga tushirish:**
```bash
python manage.py runserver
```

6. **Admin panelga kirish:**
- [https://nurbek.pythonanywhere.com/admin/login/?next=/admin/)
-	•	Username: staffadmin
	•	Password: Xa!92_zQpLom48
7. **Admin panelga kirish:**
- [http://127.0.0.1:8001/admin/)
-	•	Username: admin
	•	Password: admin123

## 📝 Foydalanish

1. **Ro'yxatdan o'tish yoki kirish:**
   - `/register/` - Yangi hisob yaratish
   - `/login/` - Mavjud hisobga kirish

2. **Xonalar va jumboqlar:**
   - Admin panel orqali xonalar va jumboqlar qo'shish
   - Har bir xonada bir nechta jumboq bo'lishi mumkin
   - Jumboqlar tartib bo'yicha yechiladi

3. **Javob yuborish:**
   - Har bir jumboq uchun vaqt hisoblanadi
   - To'g'ri javob uchun ball beriladi
   - Vaqtga qarab ball miqdori o'zgaradi

4. **Statistika:**
   - `/statistics/` - Batafsil statistika ko'rish

## 🎮 Jumboq turlari

- **Matematika** - Matematik masalalar
- **Mantiqiy** - Mantiqiy jumboqlar
- **So'z** - So'z jumboqlari
- **Xotira** - Xotira o'yinlari
- **Naqsh** - Naqsh tushunish

## 📊 Model struktura

- **Room** - Xona modeli
- **Puzzle** - Jumboq modeli
- **UserProgress** - Foydalanuvchi progressi
- **UserStatistics** - Foydalanuvchi statistikasi

## 🔧 Admin panel

Admin panel orqali:
- Xonalar qo'shish/tahrirlash
- Jumboqlar qo'shish/tahrirlash
- Foydalanuvchi progressini ko'rish
- Statistikani kuzatish

## 📝 Eslatmalar

- Har bir jumboq uchun to'g'ri javob kiritilishi kerak
- Vaqt qisqa bo'lsa, ko'proq ball olinadi
- Oldingi xona tugallanmaguncha keyingi xona ochilmaydi
- Har bir jumboq bir necha marta urinish mumkin


# Virtual-Escape-Room
