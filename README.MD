
# 🛒 Grocery-Scout

  

## 📄Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
	- [Installation](#installation)
- [Tech Stack](#tech-stack)
- [Development](#development)
	- [Project Structure](#project-structure)
	- [Database Management](#database-management)
	- [Running Tests](#running-tests)
- [API Features](#api-features)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Overview

Grocery Scout is a web appplication that scrapes product details from Canadian Grocery chain and compares similar products to help you make the most rational choices in your day to day grocery shopping.

## Prerequisites

- Python 3.10+
- Poetry (for Dependency Management)
### Installation
1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Run the application:**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

3. **Access the application:**
   - **Web App**: http://localhost:8000/app
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative API Docs**: http://localhost:8000/redoc
## ⚙️Techstack

-  **Backend:** Python (FastAPI)

-  **Database:** PostgreSQL (SQLAlchemy ORM)

-  **Frontend:** Next.js

-  **Testing:** Pytest / Unittest

-  **Other Tools:** Alembic for migrations, Docker

## 🛠️ Development
### Project Structure
```
grocery-scout/
├── alembic/									# Database migrations
├── app/
│   ├── __init__.py
│   ├── models/
│       ├── __init__.py				
│       ├── metro_cookie.py	 	# Metro Cookie SQLAlchemy model
│       ├── province_price.py 	# Province Price SQLAlchemy model
│       └── store_product.py	# Store, Product, and Price SQLAlchemy model
│   ├── routers/
│       ├── __init__.py
│       ├── prices.py			# Prices endpoints
│       ├── products.py			# Products endpoints
│       ├── province_price.py   # Province prices endpoints
│       └── stores.py      		# Store endpoints
│   ├── schemas/
│       ├── metro_cookie.py		# Metro cookie pydantic schemas
│       ├── province_price.py 	#	Province price pydantic schemas
│       └── store_product.py	# Store, Product, and Price pydantic schemas
│   ├── services/
│       ├── cookies.py			# Metro cookies db operations
│       ├── geocode.py			# Geocode db operations
│       ├── prices.py			# Prices db operations
│       ├── products.py			# Products db operations
│       ├── province_prices.py	# Province prices db operations
│       └── stores.py			# Stores db operations
│   └── tests/
│       ├── routers/ 
│       ├── services/
│           ├── test_products.py # Products db operations unit tests
│           ├── test_stores.py 	# Stores db operations unit tests
│       ├── __init__.py
│       └── test_main.py		# Root integration test
│        
│   ├── __init__.py
│   ├── main.py              	# FastAPI application
│   ├── database.py          	# Database configuration
├── frontend/   
├── scrapers/
│   ├── loblaw
│       ├── config.py 			# Scraper configuration
│       ├── product_scraper.py 	# Product scraper
│       ├── store_info_scraper.py # Store scraper
│   ├── metro
│       ├── config.py 			# Scraper configuration
│       ├── cookie_collector.py # Scrape cookies 
│       ├── product_scraper.py 	#	Product scraper
│       ├── store_info_scraper.py # Store scraper
│   ├── urban fare
│   ├── walmart
│       ├── scraper/
│       		├── __init__.py
│       		├── main.py		# Scrape script
│       		├── parsers.py	# Parse data
│       		├── requests.py	# Get request
│       		├── savers.py	# Save data 
│       		├── scrapers.py	# Scrape categories and pages
│       ├── __init__.py
│       ├── config.py 			# Scraper configuration
│       ├── cookie_generator.py # Generate walmart cookie for scraping
│       ├── store_id_scraper.py # Scrape all walmart store Ids
│   ├── db_writer.py			# Save store info to API
├── pyproject.toml           # Poetry configuration
└── README.md
```
### Database Management

**Create a new migration:**
```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**
```bash
poetry run alembic upgrade head
```
### Running Tests
```bash
poetry run pytest
```
## 🎯 API Features

- **Validation**: Comprehensive input validation using Pydantic
- **Error Handling**: Proper HTTP status codes and error messages
- **Documentation**: Automatic API documentation with Swagger UI
- **CORS**: Configured for cross-origin requests
- **Search**: Full-text search across product names and categories
- **Filtering**: Filter products by store, category, price range

## 🚀 Future Enhancements

- [ ] User authentication and favorites
- [ ] Price history tracking
- [ ] Email price alerts
- [ ] Shopping list features
- [ ] Mobile app
- [ ] Real-time price updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
