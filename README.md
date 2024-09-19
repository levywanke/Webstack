-

# MindQuest

**MindQuest** is an interactive quiz application built using Django, designed to provide users with various quizzes and track their performance. It includes user authentication, quiz management, and performance tracking. The project also features a REST API to interact with quizzes.

## Features

- **User Registration & Authentication**
- **Quizzes**: Create, view, and take quizzes.
- **Scoring**: Automatically score quizzes upon completion.
- **User Profiles**: Track user performance and activity.
- **Responsive Design**: Optimized for mobile and desktop.
- **REST API**: Access and manage quizzes via API endpoints.

## Technologies

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (can be switched to PostgreSQL for production)
- **Deployment**: Heroku, Nginx (for static files)
- **Web3 Integration**: Token rewards for correct answers via Web3.js

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/mindquest.git
   cd mindquest
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## API Endpoints

- `GET /api/quizzes/`: List all quizzes.
- `GET /api/quiz/<id>/`: Get details of a specific quiz.
- `POST /api/quiz/`: Create a new quiz.
- `PUT /api/quiz/<id>/`: Update a quiz.
- `DELETE /api/quiz/<id>/`: Delete a quiz.

## Deployment

1. **Deploy on Heroku**:
   - Set up Heroku environment variables.
   - Deploy the project using Git.

2. **Nginx Configuration** (for serving static files):
   - Configure Nginx to serve static files for production.
