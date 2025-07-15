🛫 Lounge Waiting List System
=============================

## 👨‍💻 Developers

- [Andre Luiz](https://www.linkedin.com/in/andre-oliveira-1066b7220/)
- [Marcella Mello](https://www.linkedin.com/in/marcellasouzamello/)

---

## ✨ Features

- Add passengers with name, phone, number of guests, and preferred notification method.
- Notify passengers via:
  - ✅ SMS (Twilio)
  - ✅ Email (Gmail SMTP)
- View and manage the live waiting list.
- Export call logs to:
  - 📄 PDF
  - 📊 Excel
- View individual passenger details.
- Call next or specific passengers.
- Skip or remove passengers manually.
- Responsive UI built with **Bootstrap 5**.

---

## 🔧 Tech Stack

- **Backend:** Django 5.2
- **Frontend:** HTML + Bootstrap 5
- **Notifications:** Twilio API, Gmail SMTP
- **PDF Export:** xhtml2pdf
- **Excel Export:** openpyxl
- **Database:** SQLite (for development)

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/DecoOliveira98/lounge-waitinglist.git
cd lounge-waitinglist
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Crie um arquivo `.env` com o seguinte conteúdo:

```
# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email (Gmail SMTP com senha de app)
HOST_USER=your.email@gmail.com
HOST_PASSWORD=your_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS=True

# Django Settings
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Run the migrations
```bash
python manage.py migrate
```

### 6. Start the server
```bash
python manage.py runserver
```

---

## 📁 Project Structure

```
waitinglist_dublin_airport/
│
├── waitlist/
│   ├── templates/
│   │   ├── waitlist/
│   │   └── email/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
├── waitinglist_dublin_airport/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3
├── .env
├── requirements.txt
└── README.txt
```