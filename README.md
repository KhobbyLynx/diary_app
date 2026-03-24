# Django AI Diary

A high-performance, responsive Diary application built with Django. It features seamless Google OAuth 2.0 authentication and integrates with the Groq Cloud API (LLaMA 3.3) for intelligent, automated entry analysis (sentiment and summarization).

## Tech Stack

- **Python**: 3.13
- **Django**: 6.0.3
- **Authentication**: `django-allauth` (Google OAuth)
- **AI Integration**: `groq` (LLaMA 3.3)
- **Frontend**: Tailwind CSS (CDN), Vanilla JS
- **Database**: SQLite3 (Local)
- **Package Management**: Pipenv

## Environment Variables

Create a `.env` file in the root directory and add the following keys. Do not commit your actual keys to version control.

```env
GROQ_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd diary
   ```

2. **Install dependencies**
   We use Pipenv for dependency management. If you don't have it installed, run `pip install pipenv`. Then, pull down the environment:

   ```bash
   pipenv install
   ```

   _(If you prefer standard virtual environments, the `requirements.txt` is also available.)_

3. **Activate the environment**

   ```bash
   pipenv shell
   ```

4. **Populate Environment Variables**
   Ensure your `.env` file is fully populated with your Groq API key and Google OAuth Client credentials.

5. **Run Migrations**
   Initialize the database:

   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.

## Google OAuth Notes

For local dev, make sure your Google Cloud Console Authorized Redirect URI is exactly set to: `http://127.0.0.1:8000/accounts/google/login/callback/`.
