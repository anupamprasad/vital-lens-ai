# Getting Started with Phase 3 Development

Welcome to Phase 3 of Vital Lens AI! This guide will help you set up your local development environment and start building.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Git** 2.30+ — version control
- **Docker** 20.10+ — containerization
- **Docker Compose** 2.0+ — multi-container orchestration

### For Backend Development (Optional)
- **Python** 3.11+ — backend language
- **pip** or **poetry** — Python package manager

### For Frontend Development (Optional)
- **Node.js** 18+ — JavaScript runtime
- **npm** 9+ or **yarn** 3+ — Node package manager

### System Requirements
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 20GB minimum
- **OS**: macOS, Linux, or Windows (WSL2)

---

## 🚀 Quick Start (5 minutes)

### 1. Clone & Navigate
```bash
cd /path/to/vital-lens-ai
cd phase3_application
```

### 2. Create Environment File
```bash
cp .env.example .env
```

### 3. Start All Services
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
docker-compose exec backend alembic upgrade head
```

### 5. Access the Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **RabbitMQ Admin:** http://localhost:15672 (guest/guest)

---

## 🔧 Detailed Setup Guide

### Option A: Docker-Only Development (Recommended for Quick Start)

#### Setup
```bash
# Navigate to project
cd phase3_application

# Create environment file
cp .env.example .env

# Build images
docker-compose build

# Start services
docker-compose up -d

# Verify all services are running
docker-compose ps
```

#### View Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

#### Access Services
```bash
# Backend shell
docker-compose exec backend bash

# Database shell
docker-compose exec postgres psql -U vitalensai -d vital_lens_ai

# Redis CLI
docker-compose exec redis redis-cli
```

#### Stop Services
```bash
docker-compose down
```

#### Clean Everything (Fresh Start)
```bash
docker-compose down -v  # Remove volumes too
rm -rf phase3_application/postgres_data
rm -rf phase3_application/redis_data
docker-compose up -d
```

---

### Option B: Local Backend Development (With Docker Services)

#### Install Python Dependencies
```bash
# Navigate to backend
cd phase3_application/backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Ensure Docker services are running
cd ..
docker-compose up -d postgres redis rabbitmq

# Initialize database
cd backend
alembic upgrade head

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Database Migrations
```bash
# Create new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

#### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_login"
```

#### Code Quality
```bash
# Format code with black
black app/

# Sort imports with isort
isort app/

# Check linting
flake8 app/

# Type checking
mypy app/
```

---

### Option C: Local Frontend Development (With Docker Services)

#### Install Node Dependencies
```bash
# Navigate to frontend
cd phase3_application/frontend

# Install dependencies
npm install
# or
yarn install

# Create .env file
cp .env.example .env

# Ensure Docker services are running (for API)
cd ..
docker-compose up -d backend

# Run development server
npm run dev
```

#### Development Commands
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Check types
npm run type-check

# Lint code
npm run lint

# Format code
npm run format
```

#### Debugging in Browser
```bash
# Frontend dev server is at http://localhost:5173
# Open browser DevTools (F12)
# Check Console for errors
# Check Network tab for API calls
```

---

### Option D: Full Local Development (Backend + Frontend)

This setup requires both Python and Node.js installed locally.

```bash
# Terminal 1: Start Docker services only
cd phase3_application
docker-compose up -d postgres redis rabbitmq

# Terminal 2: Start backend
cd phase3_application/backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 3: Start frontend
cd phase3_application/frontend
npm run dev

# Access application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 🔑 Important Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://vitalensai:develop123@postgres:5432/vital_lens_ai

# Redis
REDIS_URL=redis://redis:6379

# JWT
SECRET_KEY=your-super-secret-key-change-in-production

# Debug
DEBUG=true
LOG_LEVEL=INFO
```

### Frontend (.env)
```bash
# API
VITE_API_URL=http://localhost:8000  # may also include /api/v1, endpoints are relative to base
VITE_DEBUG=true

# Features
VITE_ENABLE_CAMERA=true
VITE_ENABLE_2FA=true
```

---

## 📊 Database Operations

### Access PostgreSQL
```bash
# Via Docker
docker-compose exec postgres psql -U vitalensai -d vital_lens_ai

# Via local psql
psql postgresql://vitalensai:develop123@localhost:5432/vital_lens_ai

# Useful commands
\dt                    # List tables
\d users              # Describe table
SELECT * FROM users;  # Query
```

### Backup Database
```bash
# Full backup
docker-compose exec postgres pg_dump \
  -U vitalensai vital_lens_ai > backup.sql

# Restore from backup
docker-compose exec postgres psql \
  -U vitalensai vital_lens_ai < backup.sql
```

### Reset Database
```bash
# Drop and recreate
docker-compose exec postgres psql -U vitalensai << EOF
DROP DATABASE IF EXISTS vital_lens_ai;
CREATE DATABASE vital_lens_ai;
EOF

# Run migrations
cd backend
alembic upgrade head
```

---

## 🧪 Testing Workflow

### Backend Testing
```bash
# Run tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_auth.py::test_login

# Run tests in watch mode
pytest-watch
```

### Frontend Testing
```bash
# Run tests
npm run test

# Run with coverage
npm run test -- --coverage

# Run in watch mode
npm run test -- --watch
```

### Integration Testing
```bash
# Test full flow: Frontend → API → Database
# 1. Start all services (docker-compose up)
# 2. Access http://localhost:5173
# 3. Go through registration, login, measurement flow
# 4. Check browser console for errors
# 5. Check API logs for issues
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Issue: Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Recreate container
docker-compose down postgres
docker-compose up -d postgres

# Verify connection
docker-compose exec postgres pg_isready
```

### Issue: Frontend Can't Reach API
```bash
# Check VITE_API_URL in .env
cat frontend/.env | grep VITE_API_URL

# Check API is running
curl http://localhost:8000/health

# Check network tab in browser DevTools
# Look for failed /api/ requests
```

### Issue: Redis Connection Failed
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# View Redis data
docker-compose exec redis redis-cli
> DBSIZE
> KEYS *
```

### Issue: RabbitMQ Connection Failed
```bash
# Check RabbitMQ is running
docker-compose ps rabbitmq

# Access management UI
# http://localhost:15672
# Username: guest
# Password: guest
```

### Issue: Docker Compose Won't Start
```bash
# Check Docker daemon
docker ps

# Try restart
docker-compose down
docker system prune
docker-compose up -d

# Check docker-compose version
docker-compose --version

# Ensure you have Docker Compose V2
# Update Docker Desktop if needed
```

### Issue: Node/npm Errors
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install
```

### Issue: Python Dependency Conflicts
```bash
# Create fresh virtual environment
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

---

## 📚 Project File Reference

```
phase3_application/
├── README.md                 # Main documentation
├── TECH_STACK.md            # Technology details
├── GETTING_STARTED.md       # This file
├── .env.example             # Environment template
├── docker-compose.yml       # Service orchestration
├── nginx.conf               # Reverse proxy config
│
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── models.py            # Database models
│   ├── requirements.txt      # Python packages
│   ├── Dockerfile           # Container config
│   ├── .env.example         # Backend env template
│   └── [to be created]
│       ├── app/             # Application code
│       ├── tests/           # Test files
│       └── migrations/      # Alembic migrations
│
└── frontend/
    ├── package.json         # Node dependencies
    ├── vite.config.js       # Vite config
    ├── Dockerfile           # Container config
    ├── .env.example         # Frontend env template
    └── [to be created]
        ├── src/             # Source code
        ├── public/          # Static files
        └── tests/           # Test files
```

---

## 🚀 Next Steps

1. **Start Services**: `docker-compose up -d`
2. **Access Frontend**: http://localhost:5173
3. **View API Docs**: http://localhost:8000/docs
4. **Read Architecture**: See PHASE_3_IMPLEMENTATION_PLAN.md
5. **Begin Development**: Follow the 12-week plan
6. **Run Tests**: `pytest` and `npm run test`

---

## 💡 Pro Tips

### Use Docker Compose Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias dc='docker-compose'
alias dcl='docker-compose logs -f'
alias dce='docker-compose exec'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'

# Usage
dc ps
dcl backend
dce backend bash
```

### Keep Terminal Clean
```bash
# Run services in background
docker-compose up -d

# View logs separately
docker-compose logs -f
```

### Debug API Requests
```bash
# Use httpie for nice formatting
http http://localhost:8000/api/v1/users/me \
  Authorization:"Bearer YOUR_TOKEN"
# user registration examples
http http://localhost:8000/api/v1/auth/signup \
  name="Alice" email="alice@example.com" password="secret123"

# alias endpoint (same behaviour)
http http://localhost:8000/api/v1/auth/register \
  name="Bob" email="bob@example.com" password="secret123"

# list all users (requires auth)
http http://localhost:8000/api/v1/users/ \
  Authorization:"Bearer YOUR_TOKEN"

# Or use curl with jq
curl http://localhost:8000/api/v1/users/me | jq .

# curl example for list
curl http://localhost:8000/api/v1/users/ -H "Authorization: Bearer YOUR_TOKEN" | jq .
```

### Monitor Resource Usage
```bash
# View container stats
docker stats

# View detailed logs with timestamps
docker-compose logs --timestamps -f
```

---

## 📞 Help & Support

- **API Documentation**: http://localhost:8000/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Docker Docs**: https://docs.docker.com
- **Project Plan**: See `PHASE_3_IMPLEMENTATION_PLAN.md`

---

## ✅ Setup Verification Checklist

After setup, verify everything is working:

- [ ] Docker running: `docker ps`
- [ ] Services started: `docker-compose ps` (all up)
- [ ] Frontend accessible: http://localhost:5173
- [ ] Backend running: http://localhost:8000
- [ ] API docs loaded: http://localhost:8000/docs
- [ ] Database ready: `docker-compose exec postgres pg_isready`
- [ ] Redis ready: `docker-compose exec redis redis-cli ping`
- [ ] RabbitMQ ready: http://localhost:15672

---

**Status:** 🚀 Ready to Start Phase 3 Development!

**Last Updated:** January 2024
