# VERIDEX

## Professional SaaS Market Research Intelligence Platform

VERIDEX is an enterprise-grade market research platform designed for organizations that need to track, analyze, and monitor competitor pricing, features, customer sentiment, and market trends in real-time. Built with modern enterprise architecture using FastAPI backend and Streamlit frontend.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Installation Guide](#installation-guide)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [API Documentation](#api-documentation)
9. [Project Structure](#project-structure)
10. [Database Schema](#database-schema)
11. [Security](#security)
12. [Usage Examples](#usage-examples)
13. [Troubleshooting](#troubleshooting)
14. [Development](#development)
15. [Deployment](#deployment)

---

## Project Overview

### What is VERIDEX?

VERIDEX stands for "Veritas Index" - the truth index. It's a professional intelligence gathering platform that enables businesses to:

- Track competitor pricing across multiple SaaS products in real-time
- Monitor feature releases and product updates
- Analyze customer sentiment from reviews and social feedback
- Identify pricing trends and market gaps
- Make data-driven strategic decisions about market positioning
- Generate competitive intelligence reports

### Why VERIDEX?

**For Strategic Planning:**
Understanding competitor moves helps you position your product correctly. VERIDEX gives you visibility into what competitors charge, what features they offer, and what customers think about them.

**For Pricing Strategy:**
Price changes signal market dynamics. Track when competitors raise/lower prices to understand market elasticity and customer willingness to pay.

**For Product Development:**
Customer sentiment reveals pain points. Monitor review sentiment to identify features customers want or problems with competitor offerings.

**For Sales Intelligence:**
Know your competition better than your sales team asks. Provide competitive win/loss analysis backed by real market data.

---

## Key Features

### Competitor Management
- Add and organize SaaS products you want to track
- Categorize by industry (CRM, Project Management, Productivity, Analytics, etc.)
- Store website URLs and founding information
- Track competitor addition/update history

### Pricing Intelligence
- Record pricing tiers for each competitor (Pro, Enterprise, etc.)
- Track price per billing period (monthly, yearly, per user/month)
- Monitor pricing changes over time
- Calculate price increase percentages automatically
- Identify pricing patterns and market positioning

### Sentiment Analysis
- Log customer reviews from multiple sources (G2, Capterra, Reddit, Twitter, etc.)
- Record sentiment (positive, neutral, negative)
- Store customer ratings (0-5 stars)
- Track review summaries and key feedback
- Calculate average ratings and sentiment distribution

### Feature Tracking
- Document features offered by competitors
- Specify which pricing tier includes each feature
- Compare feature sets across competitors
- Identify gaps in competitor offerings

### Price History Analytics
- Automatic calculation of price increase/decrease percentages
- Track historical pricing for trend analysis
- Identify competitors raising prices (market confidence)
- Spot competitors lowering prices (market pressure)
- Calculate average price changes over time

### Professional Dashboard
- Clean, intuitive Streamlit interface
- Real-time data visualization
- Filtering and sorting capabilities
- Accessible from any device with a browser

---

## Architecture

### Technology Stack

**Backend:**
- **FastAPI** – Modern, fast Python web framework for building APIs
- **SQLAlchemy** – Object-relational mapping for database operations
- **PostgreSQL** – Robust, scalable relational database
- **Uvicorn** – ASGI server for running FastAPI

**Frontend:**
- **Streamlit** – Rapid web app development in Python
- **Pandas** – Data manipulation and analysis
- **Plotly** – Interactive data visualizations

**Security:**
- **Passlib + Bcrypt** – Password hashing and verification
- **Python-Jose** – JWT token generation and validation

### Application Architecture

┌─────────────────────────────────────────────────────────────┐
│ VERIDEX Architecture │
├─────────────────────────────────────────────────────────────┤
│ │
│ Frontend Layer (Streamlit) │
│ ├── Dashboard Page │
│ ├── Competitors Management │
│ ├── Pricing Analysis │
│ ├── Sentiment Tracking │
│ └── Price History Visualization │
│ │ │
│ ▼ (HTTP Requests) │
│ │
│ API Layer (FastAPI) │
│ ├── Competitor Router /api/v1/competitors │
│ ├── Pricing Router /api/v1/pricing │
│ ├── Review Router /api/v1/reviews │
│ ├── Feature Router /api/v1/features │
│ └── Price History Router /api/v1/price-history │
│ │ │
│ ▼ │
│ │
│ Service Layer (Business Logic) │
│ ├── CompetitorService │
│ ├── PricingService │
│ ├── ReviewService │
│ ├── FeatureService │
│ └── PriceHistoryService │
│ │ │
│ ▼ │
│ │
│ Repository Layer (Data Access) │
│ ├── CompetitorRepository │
│ ├── PricingRepository │
│ ├── ReviewRepository │
│ ├── FeatureRepository │
│ └── PriceHistoryRepository │
│ │ │
│ ▼ │
│ │
│ Database Layer (PostgreSQL) │
│ ├── competitors table │
│ ├── pricing_tiers table │
│ ├── reviews table │
│ ├── features table │
│ └── price_history table │
│ │
└─────────────────────────────────────────────────────────────┘


### Folder Structure Explained

veridex/
│
├── core/ # Configuration and constants
│ ├── config.py # App settings (database URL, API keys, etc.)
│ └── constants.py # Enums and constants (categories, roles, etc.)
│
├── models/ # SQLAlchemy ORM models (database schema)
│ ├── competitor.py # Competitor table definition
│ ├── pricing.py # Pricing tier table definition
│ ├── review.py # Review table definition
│ ├── feature.py # Feature table definition
│ └── price_history.py # Price history table definition
│
├── schemas/ # Pydantic validation schemas
│ ├── competitor_schema.py # Request/response validation for competitors
│ ├── pricing_schema.py # Request/response validation for pricing
│ ├── review_schema.py # Request/response validation for reviews
│ ├── feature_schema.py # Request/response validation for features
│ └── price_history_schema.py # Request/response validation for price history
│
├── repository/ # Data access layer (database queries)
│ ├── competitor_repo.py # CRUD operations for competitors
│ ├── pricing_repo.py # CRUD operations for pricing
│ ├── review_repo.py # CRUD operations for reviews
│ ├── feature_repo.py # CRUD operations for features
│ └── price_history_repo.py # CRUD operations for price history
│
├── services/ # Business logic layer
│ ├── competitor_service.py # Competitor business logic
│ ├── pricing_service.py # Pricing business logic
│ ├── review_service.py # Review analysis logic
│ ├── feature_service.py # Feature comparison logic
│ └── price_history_service.py # Pricing analytics logic
│
├── routers/ # API endpoints
│ ├── competitor_router.py # /api/v1/competitors endpoints
│ ├── pricing_router.py # /api/v1/pricing endpoints
│ ├── review_router.py # /api/v1/reviews endpoints
│ ├── feature_router.py # /api/v1/features endpoints
│ └── price_history_router.py # /api/v1/price-history endpoints
│
├── security/ # Authentication and authorization
│ ├── auth.py # JWT token creation and validation
│ └── permissions.py # Role-based access control
│
├── database.py # Database connection and initialization
├── app.py # Main FastAPI application
├── requirements.txt # Python dependencies
├── .env.example # Environment variables template
└── README.md # This file


---

## Prerequisites

### System Requirements
- **Python:** 3.8 or higher
- **PostgreSQL:** 12 or higher
- **RAM:** Minimum 2GB (4GB recommended)
- **Disk Space:** Minimum 5GB
- **OS:** Linux, macOS, or Windows

### Software Requirements
- Git (for version control)
- pip (Python package manager)
- PostgreSQL CLI tools (optional, for database management)

### Knowledge Requirements
- Basic understanding of REST APIs
- Familiarity with Python
- Basic database concepts

---

## Installation Guide

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd veridex
```

### Step 2: Create and Activate Virtual Environment

Creating a virtual environment isolates your project dependencies from system Python.

```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all Python packages needed for both backend and frontend.

### Step 4: Set Up PostgreSQL Database

#### Option A: Using Command Line

```bash
# Create database
createdb veridex

# Create user (optional)
createuser veridex_user -P
```

#### Option B: Using PostgreSQL GUI (pgAdmin)

1. Open pgAdmin
2. Right-click "Databases"
3. Create new database named "veridex"
4. Note the connection details

### Step 5: Configure Environment Variables

Create `.env` file in root directory:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/veridex
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=False
ENVIRONMENT=development


### Step 6: Initialize Database

```bash
python -c "from database import init_db; init_db()"
```

This creates all required tables in PostgreSQL.

### Step 7: Verify Installation

```bash
# Test backend
python -c "from app import app; print('FastAPI OK')"

# Test database connection
python -c "from database import health_check; print('Database OK' if health_check() else 'Database FAILED')"
```

---

## Configuration

### Environment Variables (.env)

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/veridex
DATABASE_ECHO=False
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# API Configuration
API_TITLE=VERIDEX
API_VERSION=1.0.0
API_DESCRIPTION=SaaS Market Research Intelligence Platform

# Security Configuration
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=False
ENVIRONMENT=development
LOG_LEVEL=INFO

# CORS Settings (for frontend)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8501"]
```

### Configuration Hierarchy

1. `.env` file (highest priority)
2. Environment variables
3. Defaults in `core/config.py` (lowest priority)

---

## Running the Application

### Option 1: Run Backend Only (FastAPI)

```bash
# Start FastAPI server on http://localhost:8000
python app.py
```

Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Option 2: Run Frontend Only (Streamlit)

```bash
# Start Streamlit app on http://localhost:8501
streamlit run frontend/streamlit_app.py
```

### Option 3: Run Both (Recommended for Development)

Terminal 1:
```bash
python app.py
```

Terminal 2:
```bash
streamlit run frontend/streamlit_app.py
```

Open browser:
- Backend: http://localhost:8000
- Frontend: http://localhost:8501

---

## API Documentation

### Base URL

http://localhost:8000/api/v1


### Authentication
All endpoints require JWT token in header:

Authorization: Bearer <your-token>


### Endpoints Overview

#### Competitors

POST /competitors - Create competitor
GET /competitors - List all competitors
GET /competitors/{id} - Get competitor by ID
GET /competitors/category/{category} - Filter by category
PUT /competitors/{id} - Update competitor
DELETE /competitors/{id} - Delete competitor


#### Pricing Tiers

POST /pricing - Create pricing tier
GET /pricing - List all pricing tiers
GET /pricing/{id} - Get pricing tier by ID
GET /pricing/competitor/{competitor_id} - Get competitor pricing
PUT /pricing/{id} - Update pricing tier
DELETE /pricing/{id} - Delete pricing tier


#### Reviews

POST /reviews - Create review
GET /reviews - List all reviews
GET /reviews/{id} - Get review by ID
GET /reviews/competitor/{competitor_id} - Get competitor reviews
GET /reviews/competitor/{competitor_id}/average-rating - Average rating
GET /reviews/competitor/{competitor_id}/sentiment-distribution - Sentiment stats
PUT /reviews/{id} - Update review
DELETE /reviews/{id} - Delete review


#### Features

POST /features - Create feature
GET /features - List all features
GET /features/{id} - Get feature by ID
GET /features/competitor/{competitor_id} - Get competitor features
GET /features/competitor/{competitor_id}/tier/{tier} - Features by tier
GET /features/competitor/{competitor_id}/count - Feature count
PUT /features/{id} - Update feature
DELETE /features/{id} - Delete feature


#### Price History

POST /price-history - Create price change record
GET /price-history - List all price changes
GET /price-history/{id} - Get record by ID
GET /price-history/competitor/{competitor_id} - Competitor price history
GET /price-history/competitor/{competitor_id}/tier/{tier} - Tier history
GET /price-history/competitor/{competitor_id}/average-increase - Average increase %
PUT /price-history/{id} - Update record
DELETE /price-history/{id} - Delete record


### Example API Requests

#### Create Competitor
```bash
curl -X POST "http://localhost:8000/api/v1/competitors" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "name": "Salesforce",
    "category": "CRM",
    "website": "https://www.salesforce.com",
    "founded_year": 1999
  }'
```

#### Get All Competitors
```bash
curl "http://localhost:8000/api/v1/competitors" \
  -H "Authorization: Bearer your-token"
```

#### Add Pricing Tier
```bash
curl -X POST "http://localhost:8000/api/v1/pricing" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "competitor_id": 1,
    "tier_name": "Professional",
    "price_usd": 165.00,
    "billing_period": "monthly",
    "description": "For growing teams"
  }'
```

---

## Database Schema

### competitors
Stores SaaS products you track.

Column | Type | Description
──────────────┼───────────┼──────────────────────────────
id | SERIAL | Primary key
name | VARCHAR | Product name (unique)
category | VARCHAR | CRM, Project Management, etc.
website | VARCHAR | Company website URL
founded_year | INTEGER | Year company was founded
created_at | TIMESTAMP | Record creation time
updated_at | TIMESTAMP | Last update time


### pricing_tiers
Tracks pricing plans for competitors.

Column | Type | Description
────────────────┼───────────┼──────────────────────────
id | SERIAL | Primary key
competitor_id | INTEGER | Foreign key to competitors
tier_name | VARCHAR | Plan name (Pro, Enterprise)
price_usd | NUMERIC | Price in USD
billing_period | VARCHAR | monthly, yearly, per user/month
description | VARCHAR | What's included
recorded_date | DATE | When recorded
created_at | DATE | Record creation


### reviews
Stores customer reviews and sentiment.

Column | Type | Description
────────────────┼───────────┼──────────────────────────
id | SERIAL | Primary key
competitor_id | INTEGER | Foreign key to competitors
source | VARCHAR | G2, Capterra, Reddit, etc.
rating | NUMERIC | 0-5 stars
sentiment | VARCHAR | positive, neutral, negative
comment_summary | VARCHAR | Summary of feedback
recorded_date | DATE | When recorded
created_at | DATE | Record creation


### features
Documents competitor features.

Column | Type | Description
────────────────┼───────────┼──────────────────────────
id | SERIAL | Primary key
competitor_id | INTEGER | Foreign key to competitors
feature_name | VARCHAR | Feature name
tier_available | VARCHAR | Which tier(s) include it
recorded_date | DATE | When recorded
created_at | DATE | Record creation


### price_history
Tracks pricing changes over time.

Column | Type | Description
────────────────┼───────────┼──────────────────────────
id | SERIAL | Primary key
competitor_id | INTEGER | Foreign key to competitors
tier_name | VARCHAR | Which tier changed
old_price | NUMERIC | Previous price
new_price | NUMERIC | New price
change_date | DATE | When change occurred
created_at | DATE | Record creation


---

## Security

### Password Security
- Passwords hashed with bcrypt (not stored in plain text)
- Never share database credentials
- Rotate secrets regularly in production

### API Security
- JWT tokens required for all endpoints
- Tokens expire after 30 minutes
- Use HTTPS in production (not HTTP)

### Database Security
- Use strong PostgreSQL password
- Restrict database access to application server only
- Regular backups recommended
- Never commit `.env` file to version control

### Role-Based Access Control

Admin → Full access to all data
Analyst → Can create/edit competitor data
Viewer → Read-only access


---

## Usage Examples

### Scenario 1: Track Salesforce Pricing

1. Add Salesforce as competitor
2. Record all pricing tiers (Starter, Professional, Enterprise)
3. Monitor for price changes monthly
4. Track customer sentiment from G2 reviews

### Scenario 2: Competitive Analysis

1. Add 5 main competitors
2. Record all features each offers
3. Compare feature availability across tiers
4. Identify gaps in competitor offerings

### Scenario 3: Price Intelligence

1. Log initial pricing for all competitors
2. Track price changes monthly
3. Calculate average price increase
4. Identify pricing trends

---

## Troubleshooting

### "Connection refused" Error
**Problem:** Can't connect to PostgreSQL

**Solutions:**
1. Verify PostgreSQL is running: `pg_isready`
2. Check database URL in `.env`
3. Verify database exists: `psql -l`
4. Restart PostgreSQL service

### "ModuleNotFoundError" Error
**Problem:** Missing Python packages

**Solutions:**
```bash
pip install -r requirements.txt
pip list  # Verify all installed
```

### "Authentication failed" Error
**Problem:** Wrong database credentials

**Solutions:**
1. Check `.env` has correct password
2. Verify PostgreSQL user exists
3. Reset password: `ALTER USER postgres WITH PASSWORD 'newpassword';`

### "Port 8000 already in use" Error
**Problem:** FastAPI server won't start

**Solutions:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app:app --port 8001
```

---

## Development

### Adding a New Feature

1. Create model in `models/`
2. Create schema in `schemas/`
3. Create repository in `repository/`
4. Create service in `services/`
5. Create router in `routers/`
6. Include router in `app.py`
7. Test with API docs

### Testing

```bash
# Manual testing
python -c "from database import health_check; health_check()"

# API testing with Swagger
# Visit http://localhost:8000/docs
```

---

## Deployment

### Production Checklist
- Change `SECRET_KEY` in `.env`
- Set `DEBUG=False`
- Set `ENVIRONMENT=production`
- Use strong PostgreSQL password
- Enable HTTPS
- Set `CORS_ORIGINS` appropriately
- Use environment-specific database URL
- Enable database backups
- Set up monitoring/logging

### Deployment Options
- Heroku (PaaS)
- AWS (EC2, RDS)
- Digital Ocean
- Azure
- Docker + Kubernetes

---

## Support & Documentation

- **API Docs:** http://localhost:8000/docs
- **GitHub:** [repository-url]
- **Issues:** [issues-url]

---

## Version History

- **1.0.0** (September 2025) – Initial release

---

**VERIDEX** – Making market intelligence accessible to everyone.