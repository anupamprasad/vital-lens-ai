# Phase 3: Application Engineering - Implementation Guide

**Project:** Vital Lens AI  
**Phase:** 3 - Frontend/Backend Development  
**Timeline:** 12 Weeks (June - August 2026)  
**Status:** 🚀 STARTING

---

## 📋 Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Git

### Start Everything (One Command)
```bash
cd phase3_application
docker-compose up -d
```

### Access Points
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Admin:** http://localhost:15672 (RabbitMQ)
- **Database:** localhost:5432 (PostgreSQL)

---

## 🏗️ Project Structure

```
phase3_application/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy database models
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Container configuration
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py    # Authentication endpoints
│   │   │   │   ├── users.py   # User management
│   │   │   │   ├── vitals.py  # Vitals measurements
│   │   │   │   └── admin.py   # Admin features
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py      # Configuration
│   │   │   ├── security.py    # JWT, hashing
│   │   │   └── constants.py
│   │   ├── db/
│   │   │   ├── database.py    # Database setup
│   │   │   └── session.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── vitals.py
│   │   │   └── common.py
│   │   └── services/
│   │       ├── auth.py
│   │       ├── user.py
│   │       ├── vitals.py
│   │       └── encryption.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_vitals.py
│   └── migrations/             # Alembic migrations
│
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── Dockerfile              # Container config
│   ├── vite.config.js          # Vite configuration
│   ├── src/
│   │   ├── main.jsx            # Entry point
│   │   ├── App.jsx             # Root component
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Measurement.jsx
│   │   │   └── Settings.jsx
│   │   ├── components/
│   │   │   ├── CameraFeed.jsx
│   │   │   ├── VitalsDisplay.jsx
│   │   │   ├── Navigation.jsx
│   │   │   └── ConsentFlow.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useVitals.js
│   │   │   └── useCamera.js
│   │   ├── store/
│   │   │   └── authStore.js    # Zustand store
│   │   ├── services/
│   │   │   ├── api.js          # Axios instance
│   │   │   └── auth.js
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   └── tailwind.css
│   │   └── utils/
│   │       ├── constants.js
│   │       └── helpers.js
│   └── public/
│
├── docker-compose.yml          # Service orchestration
├── nginx.conf                  # Reverse proxy config
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## 🚀 Development Setup

### Backend Setup

```bash
# Navigate to backend
cd phase3_application/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
alembic upgrade head

# Run development server
uvicorn main:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend
cd phase3_application/frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

---

## 📚 Key Components

### Backend Architecture

#### 1. Authentication System
```python
# JWT-based authentication with 2FA support
- Token generation (1-hour expiry)
- Refresh token mechanism (7-day expiry)
- TOTP 2FA integration
- Biometric auth support
```

#### 2. User Management
```python
# Complete user lifecycle
- User registration
- Profile management
- Password reset
- Account deletion (GDPR)
- Consent tracking
```

#### 3. Vitals API
```python
# Measurement recording and retrieval
POST   /api/v1/vitals           # Record measurement
GET    /api/v1/vitals           # List vitals
GET    /api/v1/vitals/{id}      # Get specific
DELETE /api/v1/vitals/{id}      # Delete
GET    /api/v1/vitals/stats     # Statistics
```

#### 4. Data Security
```python
# AES-256 encryption for sensitive fields
- Password hashing (bcrypt)
- Token encryption
- PII field encryption
- TLS for all communications
```

### Frontend Architecture

#### 1. Camera Integration
```jsx
// WebRTC-based camera capture
- getUserMedia API
- Video preview
- Face detection overlay
- Lighting feedback
```

#### 2. Real-time Vitals Display
```jsx
// Live measurement visualization
- Heart rate graph
- Signal quality indicator
- Progress tracking
- Confidence scoring
```

#### 3. State Management
```jsx
// Zustand store for app state
- Authentication state
- User profile
- Vitals history
- UI preferences
```

#### 4. API Client
```jsx
// Axios-based HTTP client
- Automatic token refresh
- Error handling
- Request interceptors
- Response parsing
```

---

## 🔐 Security Features

### Authentication
- JWT tokens with RS256 signing
- Refresh token rotation
- TOTP 2FA support
- Biometric authentication

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- API rate limiting
- Session management

### Data Protection
- AES-256 encryption at rest
- TLS 1.2+ for transit
- Field-level encryption for PII
- Database encryption (pgcrypto)

### Compliance
- GDPR user rights (delete, export, portability)
- HIPAA audit logging
- Consent management
- Privacy-by-design

---

## 📊 API Endpoints (Phase 3 Week 5-6)

### Authentication
```
POST   /api/v1/auth/signup  # user registration
POST   /api/v1/auth/register  # alias for signup (same handler)
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh-token
POST   /api/v1/auth/2fa/setup
```

### Users
```
GET    /api/v1/users/me
GET    /api/v1/users/          # list all users (admin/debug)
PUT    /api/v1/users/profile
GET    /api/v1/users/settings
PUT    /api/v1/users/settings
DELETE /api/v1/users/account
POST   /api/v1/users/consent
```

### Vitals
```
POST   /api/v1/vitals
GET    /api/v1/vitals
GET    /api/v1/vitals/{id}
DELETE /api/v1/vitals/{id}
GET    /api/v1/vitals/stats
POST   /api/v1/vitals/inference
```

### Admin
```
GET    /api/v1/admin/users
GET    /api/v1/admin/logs
GET    /api/v1/admin/stats
```

---

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_auth.py::test_login
```

### Frontend Tests
```bash
# Run tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test -- --coverage
```

---

## 🐳 Docker Commands

### Build Images
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services
```bash
docker-compose down
```

### Database Management
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U vitalensai -d vital_lens_ai

# Reset database
docker-compose down -v
docker-compose up
```

---

## 📈 Development Workflow

### Week 1-2: Setup & Architecture
1. Initialize projects
2. Design database schema
3. Create API specification
4. Setup CI/CD pipeline

### Week 3-4: Authentication
1. User model and registration
2. JWT authentication
3. 2FA implementation
4. OAuth integration

### Week 5-6: Backend API
1. User endpoints
2. Vitals endpoints
3. Model integration
4. Error handling

### Week 7-8: Frontend
1. Camera integration
2. Dashboard UI
3. Real-time display
4. User settings

### Week 9-10: Advanced Features
1. Data export/import
2. Reporting engine
3. Admin dashboard
4. Notifications

### Week 11-12: Testing & Deployment
1. Comprehensive testing
2. Security hardening
3. Performance optimization
4. Production deployment

---

## 📝 Environment Variables

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql://vitalensai:develop123@localhost:5432/vital_lens_ai
DB_USER=vitalensai
DB_PASSWORD=develop123
DB_NAME=vital_lens_ai

# Redis
REDIS_URL=redis://localhost:6379

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Frontend
VITE_API_URL=http://localhost:8000  # or include /api/v1; services strip version prefix automatically

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# AWS/Cloud (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

# Debug
DEBUG=True
LOG_LEVEL=INFO
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up postgres
```

### Frontend Can't Reach API
```bash
# Check VITE_API_URL in .env
# Ensure backend is running
# Check CORS configuration
```

### Permission Denied
```bash
# Fix file permissions
chmod +x backend/start.sh
chmod +x frontend/start.sh
```

---

## 📚 Documentation

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Database Schema:** See `backend/models.py`
- **Frontend Components:** See `frontend/src/components/`
- **Security:** See `PHASE_3_IMPLEMENTATION_PLAN.md`

---

## 🎯 Success Metrics

- All API endpoints functional
- >80% test coverage
- <200ms API response time
- <3 second frontend load time
- GDPR/HIPAA compliance
- Security audit passed

---

## 🤝 Contributing

1. Create feature branch
2. Make changes with tests
3. Submit pull request
4. Code review + approval
5. Merge to main

---

## 📞 Support

See `PHASE_3_IMPLEMENTATION_PLAN.md` for detailed architecture and planning.

---

**Status: 🚀 READY FOR PHASE 3**

**Next: Week 1-2 Project Setup**
