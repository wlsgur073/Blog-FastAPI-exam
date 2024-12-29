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
   check [`requirements.txt`](https://github.com/wlsgur073/Blog_FastAPI/blob/main/Blog/requirements.txt)

4. Set up the database:

   - Ensure your MySQL database is running.
   - Create a new database for the blog application.
   - Update the database connection settings in the project configuration.

5. Run the application:

   ```bash
   cd /Blog
   uvicorn app.main:app --reload
   ```

   Replace `app.main` with the actual path to your FastAPI application if different.

6. Access the application


## Dependencies

- **SQLAlchemy**: ORM for database interactions.
- **mysql-connector-python**: MySQL connector for Python.
- **aiomysql**: Asynchronous MySQL driver.
- **FastAPI**: Web framework for building APIs and web applications.
- **Jinja2**: Templating engine for rendering HTML.
