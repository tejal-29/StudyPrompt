# Smart Study – An AI-Powered Personalized Study Planner

Smart Study is an AI-powered personalized learning platform designed to help students plan, organize, and optimize their learning journey. It enables users to create customized study plans, manage daily tasks, track progress, and receive intelligent assistance through an AI chatbot.

Whether you're preparing for competitive exams, college studies, or learning new skills, Smart Study provides a structured and personalized approach to achieve your learning goals.

---

## 🚀 Features

-  Personalized Study Plans
-  Daily Task & To-Do Management
-  Progress Tracking Dashboard
-  AI Chatbot powered by Google Gemini
-  Goal-Based Learning Roadmaps
-  Subject & Topic Management
-  Learning Analytics
-  Secure JWT Authentication
-  User Profile Management
-  Fully Responsive User Interface

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- React Router DOM
- Axios

### Backend
- Django
- Django REST Framework
- JWT Authentication (Simple JWT)

### Database
- PostgreSQL (Supabase)

### AI Integration
- Google Gemini API

### Development Tools
- Git & GitHub
- Postman
- VS Code

---

## 📂 Project Structure

```text
Smart-Study/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── accounts/
│   ├── planner/
│   ├── chatbot/
│   ├── study/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Smart-Study.git

cd Smart-Study
```

---

## 🔧 Backend Setup

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Start the Backend Server

```bash
python manage.py runserver
```

Backend URL

```
http://127.0.0.1:8000/
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend folder.

```env
SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_supabase_database_url

GEMINI_API_KEY=your_gemini_api_key
```

Create a `.env` file inside the frontend folder.

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## 📷 Screenshots

Add screenshots of the following pages:

- Login
- Register
- Dashboard
- Study Planner
- AI Chatbot
- Progress Tracker
- Profile
- Analytics

---

## 🎯 Future Enhancements

- 📅 AI Smart Study Scheduler
- 📄 PDF Upload & AI Summarization
- 🎤 Voice-Based AI Assistant
- 📹 Learning Resource Recommendations
- 🏆 Gamification & Achievement Badges
- 👥 Collaborative Study Groups
- 📱 Mobile Application
- 🔔 Email & Push Notifications
- 📊 Advanced Performance Analytics
- 🌙 Dark Mode

---

## 📡 API Modules

- Authentication
- User Management
- Study Planner
- Task Management
- Progress Tracking
- AI Chatbot
- Analytics

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork the repository.

2. Create a new feature branch.

```bash
git checkout -b feature-name
```

3. Commit your changes.

```bash
git commit -m "Add new feature"
```

4. Push the branch.

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

## 📄 License

This project is licensed for educational and portfolio purposes.

---

## 👩‍💻 Author

**Tejal Subhash Komb**

Full Stack Developer

**Tech Stack**

- React.js
- Django
- Python
- Django REST Framework
- PostgreSQL
- REST APIs
- Google Gemini API

---



> **Smart Study** aims to make learning smarter, more personalized, and AI-driven by combining modern web technologies with intelligent assistance.
