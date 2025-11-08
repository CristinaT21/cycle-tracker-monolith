# Getting Started with Cycle Tracker

Quick guide to get the Cycle Tracker API up and running.

## Prerequisites

- Docker & Docker Compose installed
- Git installed

## Quick Start

### 1. Start the Application

```bash
cd cycle-tracker-monolith
docker-compose up -d
```

This starts:
- PostgreSQL database on port 5432
- Django API server on port 8000

### 2. Access the Application

- **API Documentation (Swagger)**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/
- **ReDoc**: http://localhost:8000/api/redoc/

### 3. Default Admin Account

- **Email**: `admin@example.com`
- **Password**: `admin123`

## Common Tasks

### View Logs
```bash
docker-compose logs -f web
```

### Stop the Application
```bash
docker-compose down
```

### Restart After Code Changes
```bash
docker-compose restart web
```

### Run Django Management Commands
```bash
docker-compose exec web python manage.py <command>
```

## API Workflow Example

### 1. Register a User
```bash
POST /api/v1/auth/register/
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Jane"
}
```

### 2. Login
```bash
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
Copy the `access` token from the response.

### 3. Authorize in Swagger
Click **"Authorize"** button and enter: `Bearer <your-access-token>`

### 4. Create Cycles
```bash
POST /api/v1/cycles/
{
  "start_date": "2025-09-01",
  "end_date": "2025-09-05",
  "notes": "First cycle"
}
```

Create at least 3 cycles for predictions to work.

### 5. Add Daily Logs
```bash
POST /api/v1/cycles/logs/
{
  "date": "2025-09-02",
  "mood": "good",
  "symptom_ids": [1, 4, 7],
  "notes": "Feeling okay"
}
```

### 6. Generate Analytics
```bash
POST /api/v1/analytics/statistics/calculate/
POST /api/v1/analytics/predictions/generate/
POST /api/v1/analytics/insights/generate/
```

### 7. View Visualizations
```bash
GET /api/v1/visualizations/cycles/history/
GET /api/v1/visualizations/symptoms/frequency/
GET /api/v1/visualizations/mood/timeline/
```

## Available Symptoms

The system comes pre-loaded with 32 symptoms across 5 categories:
- **Physical**: Cramps, Headache, Fatigue, Bloating, etc. (12 symptoms)
- **Emotional**: Mood Swings, Anxiety, Irritability, etc. (7 symptoms)
- **Digestive**: Nausea, Food Cravings, Bloating, etc. (6 symptoms)
- **Skin**: Acne, Dry Skin, Oily Skin, etc. (4 symptoms)
- **Other**: Increased Thirst, Frequent Urination, etc. (3 symptoms)

View all symptoms: `GET /api/v1/cycles/symptoms/`

## Key Concepts

### Cycle vs Period
- **Cycle**: The entire menstrual cycle (start of one period to start of next, typically 21-45 days)
- **Period**: The bleeding phase (typically 2-10 days)

### Cycle Tracking
- `start_date`: First day of period/bleeding
- `end_date`: Last day of period/bleeding (optional)
- Cycle length is automatically calculated from consecutive start dates

### Token Expiration
JWT access tokens expire after 1 hour. When you get "token expired" errors:
1. Logout in Swagger (click Authorize → Logout)
2. Login again to get a new token
3. Re-authorize with the new token

## Troubleshooting

### Port Already in Use
```bash
docker-compose down
# Change ports in docker-compose.yml if needed
```

### Database Issues
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d    # Fresh start
docker-compose exec web python manage.py migrate
```

### View Container Logs
```bash
docker-compose logs web
docker-compose logs postgres
```

## Project Structure

```
modules/
├── users/           - Authentication & user management
├── cycles/          - Cycle & symptom tracking
├── analytics/       - Predictions & statistics
├── notifications/   - Reminders & notifications
└── visualizations/  - Chart data endpoints

shared/              - Common utilities
config/              - Django settings & URLs
```

## Next Steps

- Explore the **Swagger UI** for full API documentation
- Check the **main README.md** for architecture details
- Review the **Django Admin** to see all data models

## Support

For issues or questions, check:
- Main README.md for detailed documentation
- Swagger UI for API endpoint details
- Django Admin for data inspection
