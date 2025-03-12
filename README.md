# FastAPI Auth Bootstrap

A **FastAPI** boilerplate with authentication, database setup, and a well-structured project layout. Includes Docker support for easy deployment.

## ✨ Features
- **Authentication system** using OAuth2 with password hashing.
- **Database setup** with SQLAlchemy and Alembic migrations.
- **Modular structure** with routers, models, and schemas.
- **Dockerized deployment** with Docker Compose.
- **Pre-configured API security** with authentication and user management.

## 📂 Project Structure
```plaintext
.  
├── Dockerfile             # Docker build configuration  
├── docker-compose.yml     # Docker Compose setup  
├── entrypoint.sh          # Container entrypoint script  
├── LICENSE                # License file  
├── README.md              # Documentation  
├── requirements.txt       # Dependencies  
├── app/                   # Main application folder  
│   ├── __init__.py        
│   ├── main.py            # FastAPI application entrypoint  
│   ├── settings.py        # Application settings  
│   ├── models/            # Database models and queries  
│   │   ├── __init__.py    
│   │   ├── database.py    # Database connection setup  
│   │   ├── models.py      # SQLAlchemy models  
│   │   └── querys.py      # Query utilities  
│   ├── routers/           # API routers  
│   │   ├── auth_router.py # Authentication endpoints  
│   │   └── user_router.py # User-related endpoints  
│   ├── schemas/           # Pydantic schemas  
│   │   └── schemas.py     
│   ├── security/          # Authentication and security  
│   │   └── auth.py        # Password hashing and token handling  
│   ├── alembic/           # Database migrations  
│   │   ├── README        
│   │   ├── env.py        
│   │   ├── script.py.mako 
│   │   └── versions/     
│   │       └── 1.py      # Migration script  
│   ├── alembic.ini       # Alembic configuration  
```

## 🚀 Installation & Execution

### 1️⃣ Run with Docker Compose
```sh
docker compose up --build
```

### 2️⃣ Access the Running Container
```sh
docker exec -it <container_id> /bin/sh
```

### 3️⃣ Apply Migrations
```sh
alembic upgrade head
```

## 🛠️ Tech Stack
- **FastAPI** for building the API
- **SQLAlchemy** & **Alembic** for database management
- **Docker** & **Docker Compose** for containerization
- **OAuth2 & JWT** for authentication

