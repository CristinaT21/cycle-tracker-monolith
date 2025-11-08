# Cycle Tracker - Modular Monolith

A backend-only menstrual cycle tracking application built using the **Modular Monolith** architecture pattern with Django and Python.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [What is a Modular Monolith?](#what-is-a-modular-monolith)
  - [Module Boundaries](#module-boundaries)
  - [Inter-Module Communication](#inter-module-communication)
- [Modules](#modules)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

## Overview

The Cycle Tracker is a comprehensive menstrual cycle tracking application designed to help users monitor their cycles, symptoms, moods, and receive predictive insights. The application follows the **Modular Monolith** architecture, providing clear module boundaries while maintaining the simplicity of a monolithic deployment.

### Core Features

- **User Authentication & Profiles**: JWT-based authentication with customizable user profiles
- **Cycle Tracking**: Record period dates, flow intensity, and cycle history
- **Symptom & Mood Logging**: Daily logging of physical symptoms and emotional states
- **Analytics & Predictions**: ML-ready prediction algorithms for upcoming cycles
- **Notifications & Reminders**: Configurable reminders for periods and ovulation
- **Data Visualization**: API endpoints providing chart-ready data for frontend clients

## Architecture

### What is a Modular Monolith?

A **Modular Monolith** is an architectural pattern that combines the benefits of both monolithic and microservices architectures:

- **Single Deployment Unit**: All code is deployed together, simplifying deployment and operations
- **Clear Module Boundaries**: Code is organized into independent modules with well-defined interfaces
- **Loose Coupling**: Modules interact through defined contracts, not direct dependencies
- **Independent Evolution**: Each module can evolve independently without affecting others
- **Easy to Refactor**: Modules can be extracted into separate microservices if needed

### Module Boundaries

Each module in this application represents a **bounded context** in the domain model:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│                  (Django REST Framework)                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│    Users     │      │    Cycles    │     │  Analytics   │
│   Module     │──────│    Module    │─────│    Module    │
└──────────────┘      └──────────────┘     └──────────────┘
                              │                     │
                    ┌─────────┴────────┐           │
                    │                  │           │
                    ▼                  ▼           ▼
            ┌──────────────┐   ┌──────────────────────┐
            │Notifications │   │   Visualizations     │
            │    Module    │   │      Module          │
            └──────────────┘   └──────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │   Shared     │
            │  Utilities   │
            └──────────────┘
```

### Inter-Module Communication

Modules communicate through:

1. **Direct Function Calls**: For synchronous operations within the same process
2. **Shared Models**: Through Django's ORM (with clear ownership boundaries)
3. **Events/Signals**: For decoupled communication (future enhancement)
4. **Service Layer**: Business logic encapsulated in service classes

**Rules**:
- Modules should NOT directly access other modules' models
- Communication happens through service interfaces
- Each module owns its data
- Cross-module queries go through service methods

## Modules

### 1. Users Module (`modules.users`)

**Responsibility**: User authentication, authorization, and profile management

**Key Components**:
- Custom User model with email-based authentication
- JWT token management
- User profiles and preferences
- Password management

**API Endpoints**:
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `GET /api/v1/auth/me/` - Get current user profile
- `PUT /api/v1/auth/me/update/` - Update user profile
- `PUT /api/v1/auth/me/preferences/` - Update user preferences
- `POST /api/v1/auth/me/change-password/` - Change password

**Dependencies**: None (independent module)

---

### 2. Cycles Module (`modules.cycles`)

**Responsibility**: Menstrual cycle tracking and daily logging

**Key Components**:
- Cycle management (start/end dates, length)
- Period day tracking with flow intensity
- Daily symptom and mood logging
- Symptom catalog

**API Endpoints**:
- `GET /api/v1/cycles/` - List all cycles
- `POST /api/v1/cycles/` - Create new cycle
- `GET /api/v1/cycles/{id}/` - Get cycle details
- `PUT /api/v1/cycles/{id}/` - Update cycle
- `GET /api/v1/cycles/current/` - Get current active cycle
- `POST /api/v1/cycles/{id}/add_period_day/` - Add period day
- `GET /api/v1/cycles/logs/` - List daily logs
- `POST /api/v1/cycles/logs/` - Create daily log
- `GET /api/v1/cycles/symptoms/` - List available symptoms

**Dependencies**: Users module (for user authentication)

---

### 3. Analytics Module (`modules.analytics`)

**Responsibility**: Predictions, statistics, and insights generation

**Key Components**:
- Cycle prediction algorithms
- Statistical analysis
- Insight generation
- Pattern recognition

**API Endpoints**:
- `GET /api/v1/analytics/predictions/current/` - Get active prediction
- `POST /api/v1/analytics/predictions/generate/` - Generate new prediction
- `GET /api/v1/analytics/statistics/` - Get cycle statistics
- `POST /api/v1/analytics/statistics/calculate/` - Calculate statistics
- `GET /api/v1/analytics/insights/` - List insights
- `POST /api/v1/analytics/insights/{id}/mark_as_read/` - Mark insight as read
- `POST /api/v1/analytics/insights/generate/` - Generate new insights

**Dependencies**: Users, Cycles modules

---

### 4. Notifications Module (`modules.notifications`)

**Responsibility**: Notification delivery and reminder management

**Key Components**:
- Notification templates
- Reminder scheduling
- Multi-channel delivery (email, push, in-app)
- Notification preferences

**API Endpoints**:
- `GET /api/v1/notifications/` - List notifications
- `POST /api/v1/notifications/{id}/mark_as_read/` - Mark as read
- `POST /api/v1/notifications/mark_all_as_read/` - Mark all as read
- `GET /api/v1/notifications/reminders/` - List reminder schedules
- `POST /api/v1/notifications/reminders/` - Create reminder
- `GET /api/v1/notifications/preferences/` - Get preferences
- `PUT /api/v1/notifications/preferences/update/` - Update preferences

**Dependencies**: Users, Cycles, Analytics modules

---

### 5. Visualizations Module (`modules.visualizations`)

**Responsibility**: Aggregated data for charts and graphs

**Key Components**:
- Cycle history charts
- Calendar views
- Symptom frequency analysis
- Mood timeline
- Statistical comparisons

**API Endpoints**:
- `GET /api/v1/visualizations/cycles/history/` - Cycle length history
- `GET /api/v1/visualizations/cycles/calendar/` - Calendar data
- `GET /api/v1/visualizations/cycles/statistics/` - Statistics chart data
- `GET /api/v1/visualizations/symptoms/frequency/` - Symptom frequency
- `GET /api/v1/visualizations/symptoms/by-phase/` - Symptoms by cycle phase
- `GET /api/v1/visualizations/mood/timeline/` - Mood timeline
- `GET /api/v1/visualizations/mood/distribution/` - Mood distribution

**Dependencies**: Cycles, Analytics modules

---

### 6. Shared Module (`shared`)

**Responsibility**: Cross-cutting concerns and utilities

**Key Components**:
- Custom exception handlers
- Utility functions
- Middleware (logging, module boundary tracking)
- Common response formatters

## Technology Stack

### Core Technologies

- **Python**: 3.12+
- **Django**: 5.0.2
- **Django REST Framework**: 3.14.0
- **PostgreSQL**: 16+

### Key Libraries

- **djangorestframework-simplejwt**: JWT authentication
- **drf-spectacular**: OpenAPI/Swagger documentation
- **django-cors-headers**: CORS handling
- **django-filter**: Query filtering
- **psycopg2-binary**: PostgreSQL adapter
- **gunicorn**: Production WSGI server

### Development Tools

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **docker & docker-compose**: Containerization

## Project Structure

```
cycle-tracker-monolith/
│
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                  # Project settings
│   ├── urls.py                      # Root URL configuration
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
│
├── modules/                         # Business modules
│   ├── __init__.py
│   │
│   ├── users/                       # User & Authentication module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                # User, UserProfile
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── cycles/                      # Cycle Tracking module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                # Cycle, PeriodDay, DailyLog, Symptom
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── analytics/                   # Analytics & Predictions module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                # CyclePrediction, CycleStatistics, Insight
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py              # Business logic
│   │   └── admin.py
│   │
│   ├── notifications/               # Notifications module
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                # Notification, ReminderSchedule, etc.
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   └── visualizations/              # Data Visualization module
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py                # (No models - aggregation only)
│       ├── views.py
│       ├── urls.py
│       ├── services.py              # Data aggregation logic
│       └── admin.py
│
├── shared/                          # Shared utilities
│   ├── __init__.py
│   ├── exceptions.py                # Custom exceptions
│   ├── utils.py                     # Helper functions
│   └── middleware.py                # Custom middleware
│
├── logs/                            # Application logs
├── manage.py                        # Django management script
├── requirements.txt                 # Python dependencies
├── requirements-dev.txt             # Development dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── docker-compose.yml               # Docker composition
├── Dockerfile                       # Docker image definition
└── README.md                        # This file
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 16 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cycle-tracker-monolith
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up PostgreSQL database**:
   ```bash
   # Create database (PostgreSQL must be running)
   createdb cycle_tracker_db

   # Or use docker-compose
   docker-compose up -d postgres
   ```

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Load initial data** (optional):
   ```bash
   # Load symptom data
   python manage.py loaddata fixtures/symptoms.json
   ```

9. **Run development server**:
   ```bash
   python manage.py runserver
   ```

10. **Access the application**:
    - API: http://localhost:8000/api/v1/
    - Admin: http://localhost:8000/admin/
    - API Docs: http://localhost:8000/api/docs/

### Docker Setup

1. **Build and start containers**:
   ```bash
   docker-compose up --build
   ```

2. **Run migrations** (in a new terminal):
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Authentication

All endpoints (except registration and login) require JWT authentication.

**Getting a token**:
```bash
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "tokens": {
      "access": "eyJ0eXAiOiJKV1...",
      "refresh": "eyJ0eXAiOiJKV1..."
    }
  }
}
```

**Using the token**:
```bash
Authorization: Bearer <access_token>
```

## Development

### Code Style

This project follows PEP 8 guidelines and uses:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 .

# Type check
mypy .
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

### Creating a New Module

1. Create module directory under `modules/`
2. Add `__init__.py` with module documentation
3. Create `apps.py` with AppConfig
4. Define models in `models.py`
5. Create serializers in `serializers.py`
6. Implement views in `views.py`
7. Define URLs in `urls.py`
8. Register admin in `admin.py`
9. Add module to `INSTALLED_APPS` in `config/settings.py`
10. Include URLs in `config/urls.py`

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules --cov-report=html

# Run specific module tests
pytest modules/users/tests/

# Run with verbose output
pytest -v
```

## Deployment

### Environment Variables

Ensure all required environment variables are set in production:

- `DJANGO_SECRET_KEY`: Strong secret key
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: Your domain names
- `POSTGRES_*`: Database credentials
- `CORS_ALLOWED_ORIGINS`: Frontend URLs

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure strong `SECRET_KEY`
- [ ] Set up PostgreSQL with proper credentials
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up CORS for frontend domains
- [ ] Configure static files serving (nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging
- [ ] Set up database backups
- [ ] Configure monitoring and alerts

### Running with Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Architecture Decisions

### Why Modular Monolith?

1. **Simpler Operations**: Single deployment, easier to manage
2. **Clear Boundaries**: Enforced module separation
3. **Performance**: No network overhead between modules
4. **Easier Development**: Shared codebase, faster iteration
5. **Future-Proof**: Can extract modules to microservices later

### Module Independence

Each module:
- Has its own models and database tables
- Exposes a clear API/service interface
- Can be developed and tested independently
- Owns its business logic
- Minimizes coupling with other modules

### Data Ownership

- **Users Module**: Owns user accounts and profiles
- **Cycles Module**: Owns cycle and daily log data
- **Analytics Module**: Owns predictions and insights
- **Notifications Module**: Owns notification records
- **Visualizations Module**: Reads from other modules (no ownership)

## Contributing

Guidelines for contributing to the project:

1. Follow the modular architecture principles
2. Keep modules loosely coupled
3. Write tests for new features
4. Document API endpoints
5. Follow code style guidelines
6. Update README for significant changes

## License

[Specify your license here]

## Support

For issues and questions:
- GitHub Issues: [Your repo URL]
- Email: [Your email]
- Documentation: [Your docs URL]

---

Built with Django and the Modular Monolith architecture pattern.
