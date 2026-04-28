# Project Setup Guide: Student Organization Automated Voting System (SOAVS)

This guide will walk you through setting up and running the SOAVS application on your local machine. The project consists of three parts:

- **Backend** — Django REST API with JWT authentication
- **Frontend** — Vue 3 + Vite admin dashboard
- **Mobile App** — React Native (Expo) student voting app

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Node.js (LTS version)** and **npm**
- **MySQL Server** (XAMPP or MySQL Workbench)
- **Expo CLI** — Install globally with `npm install -g expo-cli` (for the mobile app)
- **Expo Go** app on your Android/iOS device (for testing the mobile app)

---

## Project Structure

```
appdev web/                    # Web project root
├── backend/                   # Django REST API
│   ├── api/                   # Main API app (models, views, serializers, urls)
│   ├── core/                  # Django project settings & configuration
│   ├── build.sh               # Render deployment build script
│   ├── manage.py
│   └── requirements.txt       # Python dependencies
├── frontend/                  # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/             # Pinia state management
│   │   ├── axios.js           # API client config
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── venv/                      # Python virtual environment
├── voting.sql                 # Database schema & seed data
├── students_2023.csv          # Sample voter CSV for import
└── SETUP.md

appdev mob/                    # Mobile project root (separate repo)
├── app/                       # Expo Router screens
├── components/                # Reusable React Native components
├── services/                  # API service layer
├── constants/                 # App constants & config
├── assets/                    # Images, icons, fonts
├── app.json                   # Expo configuration
├── eas.json                   # EAS Build configuration
└── package.json
```

---

## 1. Database Setup

The application uses a MySQL database named `voting`.

1. Start your MySQL server (via XAMPP or another service).
2. Create a database named `voting`.
3. Import the `voting.sql` file located in the root directory:
   ```bash
   mysql -u root -p voting < voting.sql
   ```
   *(Note: If you have no password, just omit `-p`)*

---

## 2. Backend Setup (Django)

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   - **Windows:** `..\venv\Scripts\activate`
   - **macOS/Linux:** `source ../venv/bin/activate`

3. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations (to ensure schema is up to date):
   ```bash
   python manage.py migrate
   ```

5. Start the backend server:
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://127.0.0.1:8000/`.

### Key Backend Dependencies

| Package                         | Version | Purpose                         |
|---------------------------------|---------|---------------------------------|
| Django                          | 6.0.4   | Web framework                   |
| djangorestframework             | 3.17.1  | REST API toolkit                |
| djangorestframework-simplejwt   | 5.5.1   | JWT authentication              |
| django-cors-headers             | 4.9.0   | CORS handling                   |
| mysqlclient                     | 2.2.8   | MySQL database adapter          |
| pillow                          | 12.2.0  | Image processing                |
| gunicorn                        | 23.0.0  | Production WSGI server          |
| dj-database-url                 | 2.3.0   | Database URL parsing (deploy)   |
| whitenoise                      | 6.9.0   | Static file serving (deploy)    |
| psycopg2-binary                 | 2.9.10  | PostgreSQL adapter (deploy)     |

---

## 3. Frontend Setup (Vue + Vite)

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173/`.

### Key Frontend Dependencies

| Package    | Purpose                    |
|------------|----------------------------|
| Vue 3      | UI framework               |
| Vue Router | Client-side routing        |
| Pinia      | State management           |
| Axios      | HTTP client for API calls  |
| Vite       | Dev server & build tool    |

---

## 4. Mobile App Setup (Expo / React Native)

The mobile app is in a separate directory (`appdev mob`).

1. Navigate to the mobile app directory:
   ```bash
   cd "appdev mob"
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Expo development server:
   ```bash
   npx expo start
   ```

4. Scan the QR code with the **Expo Go** app on your device, or press `a` to open in an Android emulator.

> **Note:** The mobile app connects to the backend API. Ensure the backend server is running and accessible from your device. If testing on a physical device, you may need to use a tunnel (e.g., `npx expo start --tunnel`) or update the API base URL in the `services/` directory to point to your machine's local IP address.

### Building an APK

To build a standalone APK for distribution:

```bash
npx eas build --platform android --profile preview
```

This uses the EAS Build service. See `eas.json` for build profiles.

---

## 5. Accessing the Application

| Interface           | URL                                   |
|---------------------|---------------------------------------|
| Admin Dashboard     | `http://localhost:5173/`              |
| Backend API         | `http://127.0.0.1:8000/api/`         |
| Django Admin Panel  | `http://127.0.0.1:8000/admin/`       |
| Mobile App          | Expo Go (scan QR code)                |

### Creating an Admin User

If you need to access the Django admin, run this command in the `backend` directory:
```bash
python manage.py createsuperuser
```
Follow the prompts to set your username and password.

---

## 6. Deployment (Render)

The backend is configured for deployment on [Render](https://render.com/) using the `build.sh` script.

### Render Setup

1. **Create a new Web Service** on Render and connect your Git repository.
2. **Configure the service:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn core.wsgi:application`
   - **Root Directory:** `backend`
3. **Set Environment Variables** on Render:

   | Variable         | Value                              |
   |------------------|------------------------------------|
   | `DATABASE_URL`   | Your PostgreSQL connection string   |
   | `SECRET_KEY`     | A strong, random secret key         |
   | `DEBUG`          | `False`                             |
   | `ALLOWED_HOSTS`  | Your Render domain                  |

4. The `build.sh` script will automatically:
   - Install Python dependencies from `requirements.txt`
   - Collect static files
   - Run database migrations

> **Note:** The production deployment uses PostgreSQL (via `psycopg2-binary` and `dj-database-url`) instead of MySQL.

---

## Troubleshooting

| Issue                              | Solution                                                                 |
|------------------------------------|--------------------------------------------------------------------------|
| `mysqlclient` install fails        | Install MySQL dev headers: `sudo apt install libmysqlclient-dev` (Linux) or use XAMPP's bundled libraries (Windows) |
| CORS errors in browser             | Ensure `django-cors-headers` is installed and `CORS_ALLOW_ALL_ORIGINS = True` is in `settings.py` |
| Mobile app can't reach backend     | Use `npx expo start --tunnel` or set the API URL to your machine's LAN IP |
| `npm install` fails in frontend    | Delete `node_modules` and `package-lock.json`, then run `npm install` again |
| Migrations fail                    | Ensure the `voting` database exists and MySQL is running                  |
