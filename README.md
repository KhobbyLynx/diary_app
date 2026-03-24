# Django AI Diary

A high-performance, responsive Diary application built with Django. It features seamless Google OAuth 2.0 authentication and integrates with the Groq Cloud API (LLaMA 3.3) for intelligent, automated entry analysis (sentiment and summarization).

## Tech Stack

- **Python**: 3.13
- **Django**: 6.0.3
- **Authentication**: `django-allauth` (Google OAuth)
- **AI Integration**: `groq` (LLaMA 3.3)
- **Frontend**: Tailwind CSS (CDN), Vanilla JS
- **Database**: PostgreSQL (Production) / SQLite3 (Local Development)
- **Package Management**: Pipenv

## Environment Variables

Create a `.env` file in the root directory and add the following keys.

```env
DEBUG=
SECRET_KEY=
GROQ_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
RENDER_EXTERNAL_HOSTNAME=
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

6. **Create Superuser**
   Create an initial admin account to access the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at `http://127.0.0.1:8000/`.

## Google OAuth Notes

For local dev, make sure your Google Cloud Console Authorized Redirect URI is exactly set to: `http://127.0.0.1:8000/accounts/google/login/callback/`.

## Architectural Decisions & Trade-offs

- **Third-Party Integration**: Google OAuth 2.0 was selected over alternatives (e.g., Facebook) to meet specific project requirements.
- **Authentication UX Improvements**: The Google OAuth flow is selectively configured to automatically log in returning users without prompting for account selection. This deliberate UX decision streamlines the login process and can be overridden by adding `'prompt': 'select_account'` to the configuration if explicit selection is required.
- **AI Provider Selection**: Groq API was chosen over alternatives like Claude due to its rapid response times, straightforward setup, and a generous developer free tier allowing approximately 30 requests per minute.
- **LLM Rate Management**: AI insights are generated exactly once per entry to strictly manage the volume of outbound requests to the LLM. If insights are omitted during entry creation, they can be triggered during the editing phase. The insight generation trigger is subsequently disabled once insights exist for a given entry.
- **Data Privacy**: Social sharing functionality is scoped exclusively to the entry summary; AI sentiment analysis is intentionally excluded when sharing to social platforms. If no summary, that is, generated AI analysis, sharing is disabled for that entry.

## Deployment to Render

The application is configured for deployment on Render, utilizing PostgreSQL as the production database. The deployment process relies on the following configurations:

- **`render.yaml`**: Dictates the infrastructure as code, outlining the necessary environment variables, database definitions, and service configurations.
- **`build.sh`**: Executed automatically during the deployment pipeline to install dependencies, run `collectstatic`, and apply database migrations.
