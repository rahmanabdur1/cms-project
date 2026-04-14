##  Project Setup Instructions

### 1. Clone the Repository

```bash
git clon
cd cms-backend
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-multipart python-dotenv cloudinary pillow
```

---

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/cms_db
FRONTEND_URL=http://localhost:3000
UPLOAD_DIR=static/uploads
MAX_FILE_SIZE_MB=10
```

---

### 5. Setup Database

Make sure PostgreSQL is running, then create database:

```bash
psql -U postgres -c "CREATE DATABASE cms_db;"
```

---

### 6. Run Database Migrations

```bash
alembic upgrade head
```

---

### 7. Run the Server

```bash
uvicorn main:app --reload --port 8000
```

---

### 8. Access API Documentation

Open in browser:

```
http://localhost:8000/docs
```

You can test all endpoints from Swagger UI.

---

### 9. Verify API

* Create Category → `/categories`
* Create Content → `/contents`
* Upload File → `/upload`
* Check Health → `/health`

If all endpoints work correctly, the backend setup is successful.
