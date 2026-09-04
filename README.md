# StudyPrompt – Personalized Study Planner

StudyPrompt is a full-stack web application that helps students organize their learning in one place. Users can create learning goals, generate a structured roadmap, manage topics and tasks, and track their study progress.

The application also includes an AI chatbot that helps users with learning-related questions and difficult concepts.

## Features

### User Authentication
- User registration and login
- JWT-based authentication
- Access and refresh tokens
- Protected user-specific data
- Forgot password / password reset
- User profile management

### Personalized Study Planning
- Create learning goals
- Generate a structured learning roadmap
- Divide the roadmap into phases
- Organize phases into topics
- Set study preferences based on the user's profile

### Topics and Resources
- View individual topics
- Topic descriptions and difficulty levels
- Estimated learning time
- Learning resources
- Practice quizzes
- Topic progress tracking

### Task Management
- Create and manage study tasks
- Set task priority and status
- Add estimated study time
- Schedule tasks by date
- Mark tasks as completed
- Track time spent on tasks

### Progress Tracking
- Track completed tasks and topics
- Calculate overall learning progress
- Record daily study time
- Maintain study streaks
- View learning statistics

### Analytics
- Overall study progress
- Completed topics and tasks
- Study hours
- Weekly study activity
- Topic-wise progress
- Study streak information

### AI Chatbot
- Ask learning-related questions
- Get explanations for difficult concepts
- Ask for examples
- Get help with study doubts
- Receive responses based on the user's learning information

The chatbot is powered by the Google Gemini API and can be used throughout the learning process.

---

## Tech Stack

### Frontend
- Next.js
- TypeScript
- React
- Tailwind CSS
- Axios
- React Markdown
- Recharts
- Lucide React

### Backend
- Python
- Django
- Django REST Framework
- Simple JWT

### Database
- PostgreSQL
- Supabase

### AI
- Google Gemini API

### Tools
- Git
- GitHub
- Postman
- VS Code

### Deployment
- Netlify – Frontend
- Render – Backend
- Supabase – Database

---

## Project Architecture

```text
                         StudyPrompt
                              |
             +----------------+----------------+
             |                                 |
             v                                 v
       Next.js Frontend                  Django REST API
       TypeScript + Tailwind             Python + DRF
             |                                 |
             |            REST API             |
             +---------------->----------------+
                              |
                +-------------+-------------+
                |                           |
                v                           v
        Supabase PostgreSQL           Google Gemini API
             Database                    AI Chatbot
```

---

## Application Flow

```text
User
 |
 v
Register / Login
 |
 v
Complete Profile
 |
 v
Set Learning Goal
 |
 v
Generate Personalized Roadmap
 |
 v
Roadmap
 |
 +----> Phases
          |
          +----> Topics
                    |
                    +----> Resources
                    |
                    +----> Quizzes
                    |
                    +----> Tasks
                              |
                              v
                       Complete Tasks
                              |
                              v
                       Track Progress
                              |
                              v
                          Analytics
                              |
                              v
                       Continue Learning
```

The AI chatbot can be used at different stages whenever the user needs help with a learning-related question.

---

## Project Structure

```text
StudyPrompt/
│
├── frontend/
│   ├── app/
│   │   ├── analytics/
│   │   ├── chatbot/
│   │   ├── dashboard/
│   │   ├── goals/
│   │   ├── profile/
│   │   ├── roadmap/
│   │   ├── tasks/
│   │   └── topics/
│   │
│   ├── components/
│   ├── context/
│   ├── lib/
│   │   ├── api.ts
│   │   ├── analytics.ts
│   │   └── chatbot.ts
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.ts
│
├── backend/
│   ├── accounts/
│   ├── profiles/
│   ├── goals/
│   ├── roadmap/
│   ├── topics/
│   ├── tasks/
│   ├── chatbot/
│   ├── analytics_app/
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## Backend Modules

```text
accounts
   |
   +-- Registration
   +-- Login
   +-- JWT Authentication
   +-- Password Reset

profiles
   |
   +-- User Profile
   +-- Learning Preferences

goals
   |
   +-- Learning Goals

roadmap
   |
   +-- Roadmaps
   +-- Roadmap Phases

topics
   |
   +-- Topics
   +-- Resources
   +-- Quizzes

tasks
   |
   +-- Study Tasks
   +-- Daily Progress

analytics_app
   |
   +-- Study Statistics
   +-- Progress
   +-- Study Streak

chatbot
   |
   +-- Chat History
   +-- Gemini Integration
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/tejal-29/StudyPrompt.git
cd StudyPrompt
```

---

# Backend Setup

Go to the backend directory:

```bash
cd backend
```

## Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Start Django Server

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# Frontend Setup

Open another terminal and go to the frontend directory:

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Start Development Server

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

---

# Environment Variables

## Backend `.env`

Create a `.env` file inside the backend directory.

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_supabase_database_url
GEMINI_API_KEY=your_gemini_api_key
```

For password reset email functionality:

```env
RESEND_API_KEY=your_resend_api_key
```

Do not upload the `.env` file to GitHub.

## Frontend `.env.local`

Create a `.env.local` file inside the frontend directory.

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

For production:

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api
```

---

# API Modules

The backend provides REST APIs for the main application features.

```text
/api/accounts/
    |
    +-- register/
    +-- login/
    +-- refresh/
    +-- me/

/api/profile/

/api/goals/

/api/roadmap/

/api/topics/

/api/tasks/

/api/analytics/

/api/chatbot/
    |
    +-- message/
```

The frontend communicates with these APIs using Axios.

---

# Authentication Flow

StudyPrompt uses JWT authentication.

```text
User Login
    |
    v
Django Authentication API
    |
    v
Validate Email + Password
    |
    v
Generate Access + Refresh Token
    |
    v
Frontend stores Access Token
    |
    v
Axios sends Authorization Header
    |
    v
Protected Django API
```

Protected APIs can only be accessed by authenticated users.

---

# AI Chatbot Flow

```text
User asks a question
        |
        v
Next.js Chatbot Page
        |
        v
Django Chatbot API
        |
        v
Collect user learning information
        |
        +---- Profile
        +---- Goal
        +---- Roadmap progress
        +---- Current learning phase
        +---- Recent chat history
        |
        v
Gemini API
        |
        v
AI Response
        |
        v
Django
        |
        v
Next.js
        |
        v
User
```

Recent chat history is stored so it can be used as context for future responses.

---

# Progress Tracking

```text
Task Completed
      |
      v
Topic Progress Updated
      |
      v
Overall Progress
      |
      +---- Study Time
      |
      +---- Completed Tasks
      |
      +---- Completed Topics
      |
      +---- Study Streak
      |
      v
Analytics Dashboard
```

This allows users to see how much of their roadmap has been completed.

---

# Deployment

The application uses separate services for the frontend and backend.

```text
User
  |
  v
Netlify
Next.js Frontend
  |
  | HTTPS REST API
  v
Render
Django REST Backend
  |
  +------------------+
  |                  |
  v                  v
Supabase          Gemini API
PostgreSQL        AI Chatbot
```

### Frontend
The Next.js application can be deployed using Netlify.

### Backend
The Django REST API can be deployed using Render with Gunicorn.

### Database
PostgreSQL is hosted using Supabase.

---

# Screenshots

Suggested screenshots for the project:

- Login page
- Registration page
- Dashboard
- Profile
- Goal creation
- Roadmap
- Topic details
- Task management
- Analytics
- AI Chatbot

Example:

```text
screenshots/
├── login.png
├── dashboard.png
├── roadmap.png
├── topics.png
├── tasks.png
├── analytics.png
└── chatbot.png
```

---

# Future Improvements

- AI-based study scheduling
- PDF upload and summarization
- Voice interaction with the chatbot
- Better learning resource recommendations
- Achievement badges and gamification
- Study reminders
- Email and push notifications
- Collaborative study groups
- Mobile application
- More detailed performance reports

---

# Why I Built StudyPrompt

Managing subjects, tasks, resources, and study schedules separately can make it difficult to keep track of learning.

I built StudyPrompt to bring these parts together into one application. The project also helped me gain practical experience with frontend development, REST APIs, authentication, database management, deployment, and AI integration.

---

# Author

**Tejal Subhash Komb**

Full Stack Developer

### Technologies Used

- Next.js
- TypeScript
- React
- Tailwind CSS
- Python
- Django
- Django REST Framework
- PostgreSQL
- Supabase
- REST APIs
- JWT Authentication
- Google Gemini API

---

## License

This project is developed for educational and portfolio purposes.
