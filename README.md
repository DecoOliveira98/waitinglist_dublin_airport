# 🛫 Lounge Waiting List System


## Developers

  - Andre Luiz [LinkedIn](https://www.linkedin.com/in/andre-oliveira-1066b7220/)
  - Marcella Mello [LinkedIn](https://www.linkedin.com/in/marcellasouzamello/)


A web-based waiting list management system for airport lounges, built with **Django**. The application allows staff to register passengers, notify them via **SMS** or **Email** when their lounge spot is ready, and manage the queue with full transparency.

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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Config environment variables

Edite `settings.py` com suas credenciais:

```python
# Email config (Gmail SMTP com senha de app)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your.email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

# Twilio config
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
```

> 🔐 Use `python-decouple` ou arquivos `.env` para ambientes de produção.

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
│   │   ├── email/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
├── manage.py
├── db.sqlite3
```
