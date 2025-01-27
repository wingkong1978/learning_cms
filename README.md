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

## Project Structure
/
├── backend/           # Backend application
│   ├── app.py        # Main application entry
│   ├── config.py     # Configuration settings
│   ├── models.py     # Database models
│   ├── extensions.py # Flask extensions
│   └── routes/       # API routes
│       ├── auth.py
│       ├── exam.py
│       ├── question.py
│       └── search.py
├── database/         # Database management
│   └── init_db.py   # Database initialization
├── frontend/        # Frontend application
│   ├── src/        # Source code
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router/
│   │   └── views/
│   ├── public/     # Static files
│   └── package.json
├── requirements.txt # Python dependencies
└── README.md       # Project documentation

## Deployment

### Deploy to Sealos Cloud

1. Build the Docker image:
   ```bash
   docker build -t learning-cms .
   ```

2. Push to Sealos registry:
   ```bash
   docker tag learning-cms sealos.hub/learning-cms:latest
   docker push sealos.hub/learning-cms:latest
   ```

3. Deploy to Sealos:
   ```bash
   kubectl apply -f deployment.yaml
   ```

The application will be available at the LoadBalancer IP provided by Sealos.
