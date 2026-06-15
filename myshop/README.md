
# 🛍️ MyShop – Modern Django E‑Commerce

[![Django Version](https://img.shields.io/badge/django-5.2.8-092e20?logo=django)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/celery-5.4.0-a9c92d?logo=celery)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/redis-5.0.1-dc382d?logo=redis)](https://redis.io/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**MyShop** is a full‑featured, production‑ready e‑commerce platform built with **Django**. It includes product catalog with categories, shopping cart (session‑based), order management, asynchronous email notifications via **Celery** and **Redis**, and a modern responsive frontend.


## ✨ Features

- 🛍️ **Product catalog** with categories and images
- 🛒 **Shopping cart** stored in user session
- 📝 **Order placement** with atomic database transactions
- 📧 **Asynchronous email** notifications using Celery & Redis
- 🎨 **Modern, responsive UI** built with CSS Grid / Flexbox
- 🖼️ **Image upload** for products (supports development media serving)
- 🔐 **Secure configuration** using environment variables
- 🧪 **Basic unit tests** for cart functionality
- 🚀 **Ready for deployment** (production settings separated)



## 🧰 Tech Stack

| Layer       | Technology                                         |
|-------------|----------------------------------------------------|
| Backend     | Django 5.2.8, Python 3.10+                        |
| Database    | SQLite (dev) / PostgreSQL (production recommended) |
| Task Queue  | Celery 5.4.0                                      |
| Broker      | Redis 5.0.1                                       |
| Frontend    | HTML5, CSS3, Font Awesome 6, Google Fonts (Poppins) |
| Email       | Console backend (dev) / SMTP (production)         |
| Env Config  | django-environ                                    |

## ⚙️ Installation

Follow these steps to get the project running locally.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/myshop.git
cd myshop
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows**: `venv\Scripts\activate`
- **macOS / Linux**: `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root (same level as `manage.py`) with the following content:

```env
SECRET_KEY=your-super-secret-django-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

> ⚠️ Never commit `.env` to version control. It's already ignored via `.gitignore`.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email and password.

### 7. Collect static files (optional for development)

```bash
python manage.py collectstatic
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## 🔧 Environment Variables

| Variable                 | Description                                          | Example                              |
|--------------------------|------------------------------------------------------|--------------------------------------|
| `SECRET_KEY`             | Django secret key (keep secret in production)       | `django-insecure-...`                |
| `DEBUG`                  | Set to `True` for development, `False` for production | `True`                             |
| `ALLOWED_HOSTS`          | Comma‑separated list of allowed hosts               | `localhost,127.0.0.1,myshop.com`     |
| `CELERY_BROKER_URL`      | URL of the message broker for Celery                | `redis://localhost:6379/0`           |
| `CELERY_RESULT_BACKEND`  | Backend for storing task results                    | `redis://localhost:6379/0`           |

## 🚀 Running the Project

### Start the Django server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000.

### Admin panel

Go to http://127.0.0.1:8000/admin and log in with your superuser credentials. From there you can:

- Add / edit **categories**
- Add / edit **products** (name, price, image, description, availability)
- View **orders**

### Adding products

1. Go to the admin panel → **Shop** → **Products** → **Add product**.
2. Fill in the fields (category, name, price, image, etc.).
3. Click **Save**.
4. The product will appear on the front page and in its category.

## 📧 Running Celery (Async Tasks)

MyShop uses Celery to send order confirmation emails asynchronously. To run the Celery worker:

1. Make sure Redis is installed and running:
   - **Windows** (via WSL or Docker recommended)
   - **macOS**: `brew services start redis`
   - **Linux**: `sudo systemctl start redis-server`

2. Start the Celery worker (in a separate terminal, with venv activated):

```bash
celery -A myshop worker -l info
```

Now when a customer places an order, the email will be sent in the background. For development without Redis, you can set:

```python
CELERY_TASK_ALWAYS_EAGER = True   # in settings.py
```

This runs tasks synchronously (no broker needed).

## 🧪 Testing

Run the test suite with:

```bash
python manage.py test cart
```

Or test all apps:

```bash
python manage.py test
```

Tests include:
- Adding products to cart
- Updating quantities
- Removing items
- Cart detail view rendering

## 📁 Project Structure

```
myshop/
├── cart/                 # Shopping cart app
│   ├── cart.py           # Cart class (session based)
│   ├── views.py          # add/remove/detail views
│   ├── tests.py
│   └── templates/cart/
├── orders/               # Order processing app
│   ├── models.py         # Order, OrderItem
│   ├── views.py          # order_create view
│   ├── tasks.py          # Celery task for email
│   └── templates/orders/
├── shop/                 # Products & categories
│   ├── models.py         # Category, Product
│   ├── admin.py
│   ├── views.py
│   └── templates/shop/
├── myshop/               # Project settings
│   ├── settings.py       # Main settings (with environ)
│   ├── urls.py
│   ├── celery.py         # Celery app definition
│   └── __init__.py
├── static/               # CSS, images, etc.
├── media/                # User uploaded images (ignored by git)
├── requirements.txt
├── .env                  # Environment variables (ignored)
├── .gitignore
└── manage.py
```


## 🤝 Contributing

Contributions, issues and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/amirjavarsineh/myshop/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgements

- [Django documentation](https://docs.djangoproject.com/)
- [Celery docs](https://docs.celeryq.dev/)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts (Poppins)](https://fonts.google.com/specimen/Poppins)

---
Copyright (c) 2026 Amir Javarsineh.
```

---

Simply copy the above content into a file named `README.md` in your project’s root folder. Replace placeholder images and links as needed. This README is professional, informative, and visually appealing with badges, clear sections, and step-by-step instructions.