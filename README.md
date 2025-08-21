# Clothing Store API (Backend)

This is the **backend** of a Clothing Store application, built with **FastAPI**, **SQLAlchemy**, and tested with **pytest**.  
It provides endpoints for managing **users** and **products**, including registration, authentication, and product CRUD operations.


## Features

- User authentication and authorization (JWT)
- Product management (create, read, update, delete)
- Database integration using SQLAlchemy
- Tested with pytest

## Requirements

- Python 3.12
- SQLite (default, can be changed via `DB_URL`)
- All required Python libraries are listed in `requirements.txt`

## Setup and Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/phdepaula/clothing-store.git
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the virtual environment

- On Windows:
  ```bash
  .\env\Scripts\activate
  ```

- On macOS / Linux:
  ```bash
  source env/bin/activate
  ```

### 4. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Create a .env file in the root directory with the following variables:
```bash
DB_URL=sqlite:///clothing-store.db
API_TITLE="Clothing Store API"
API_VERSION="1.0.0"
API_DESCRIPTION="API for managing a store, including products and users."
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY="CLOTHING_STORE_SECRET"
ALGORITHM="HS256"
```

### 6. Run the application
```bash
python main.py
```

## Running Tests
To run tests with pytest:

```bash
pytest
```

> Make sure your virtual environment is active and dependencies are installed.

## Notes

**Make sure your database file exists or the SQLite URL points to a valid path.**

**All environment variables must be set in the .env file before running the application.**