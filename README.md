# Learning CMS

A student exam management system built with Python (Flask) and Vue.js.

## Features
- User management (admin, teacher, student)
- Exam and question management
- Search functionality
- Frontend and mini-program support

## Setup

### Backend
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Initialize the database:
   ```bash
   python database/init_db.py
   ```
3. Run the backend server:
   ```bash
   python backend/app.py
   ```

### Frontend
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run the frontend development server:
   ```bash
   npm run dev
   ```

## Access
- Backend: `http://127.0.0.1:5000/`
- Frontend: `http://localhost:5173/`