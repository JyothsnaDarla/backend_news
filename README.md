# 🚀 News Portal Backend (Django + LLM News Generation)

This is the backend for the **AI-powered News Portal**, built with **Django REST Framework** and integrated with an **LLM (OpenAI API)** for automatic news generation.

---

## 📌 Features

✔ LLM-based automatic news generation
✔ Django Admin customization
✔ API endpoints for articles, categories, and media
✔ Auto-generated news in multiple languages
✔ Secure `.env` configuration
✔ Production static files included (`staticfiles_prod`)

---

## 📂 Project Structure

```
newsportal_backEnd/
│
├── news_portal/        # Main Django project
├── news/               # News app with LLM generator
├── staticfiles_prod/   # Production static files
└── manage.py
```

---

# 🔑 Environment Variables (IMPORTANT)

You **must create a `.env` file** inside the folder:

```
news_portal/.env
```

And add:

```
OPENAI_API_KEY=your_openai_api_key_here
```

✅ **Do NOT commit your `.env` file to GitHub.**
It is already included in `.gitignore`.

⚠️ **Do NOT share your API key publicly.**
Replace `your_openai_api_key_here` with your own key from OpenAI.

---

# ▶️ How to Run the Project

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Apply migrations

```
python manage.py migrate
```

### 3️⃣ Run the server

```
python manage.py runserver
```

Your backend will be available at:

```
http://127.0.0.1:8000/
```

---

# 📰 Generating News (LLM)

The Django Admin includes a **"Generate Article"** option where your LLM model produces:

* Title
* Content
* Category
* Summary

The generated article is automatically saved in your database.

---

# 📷 Static Files (Production)

This project uses:

```
staticfiles_prod/
```

for production builds.
Run this if needed:

```
python manage.py collectstatic
```

---

# 🛡 Security Notes

* Never upload `.env` files
* Never upload secret keys
* Do not hardcode API keys
* Rotate your API key if accidentally exposed

---

# 🤝 Contributing

Pull requests are welcome.
Please ensure that no sensitive data is included in commits.

---

# 📄 License

MIT License.
