# Blog Project with FastAPI

This project contains a blog application built using FastAPI, SQLAlchemy, and Jinja2. The application is designed to demonstrate the use of modern Python web development practices with asynchronous database handling and template rendering.

## Features

- Create, read, update, and delete blog posts.
- MySQL database integration using SQLAlchemy.
- Asynchronous database handling with aiomysql.
- Jinja2 templates for rendering HTML pages.

## Prerequisites

- Python 3.8 or higher
- MySQL database instance

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install SQLAlchemy==2.0.32 mysql-connector-python==9.0.0 aiomysql==0.2.0 fastapi==0.111.0 jinja2==3.1.4
   ```

4. Set up the database:

   - Ensure your MySQL database is running.
   - Create a new database for the blog application.
   - Update the database connection settings in the project configuration.

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

   Replace `app.main` with the actual path to your FastAPI application if different.

6. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Project Structure

```
<project-root>/
├── app/
│   ├── main.py          # Entry point of the application
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── routes/          # FastAPI route definitions
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # Static files (CSS, JavaScript, images)
├── tests/               # Unit and integration tests
└── README.md            # Project documentation
```

## Dependencies

- **SQLAlchemy**: ORM for database interactions.
- **mysql-connector-python**: MySQL connector for Python.
- **aiomysql**: Asynchronous MySQL driver.
- **FastAPI**: Web framework for building APIs and web applications.
- **Jinja2**: Templating engine for rendering HTML.
