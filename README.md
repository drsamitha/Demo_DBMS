# Database Management System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.0%2B-green)

A powerful, intuitive web interface for managing database connections, executing ORM queries, and visualizing data with ease.

<!-- ![Database Management System Screenshot](/screenshots/dashboard.png) -->

## Features

- **Database Connection Management**: Configure and switch between multiple database connections
- **ORM Console**: Execute database queries through an intuitive ORM interface
- **Model Explorer**: View and modify your database models with ease
- **Data Export**: Export your data to various formats (CSV, JSON, SQL)
- **Data Visualization**: Create charts and graphs from your database data
- **Migration Management**: Run and track database migrations
- **Security & Access Controls**: Manage permissions and track access logs

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Demo_DBMS.git
   cd Demo_DBMS
   ```

2. Install dependencies from requirements file:
   ```bash
   pip install -r requrements.txt
   ```

3. Setup and start the server using the provided script:
   ```bash
   bash restart_and_setup.sh
   ```

4. Access the application at:
   ```
   http://localhost:8000/
   ```

### Manual Setup (if not using the script)

1. Create and setup virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install requirements:
   ```bash
   pip install -r requrements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```
<!--
## Configuration

### Database Connections

You can configure multiple database connections through the interface or by editing `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'postgres_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    # Add more database connections as needed
}
```

### Environment Variables

Create a `.env` file in the project root with the following settings:

```
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Usage Guide

### Database Models Management

Navigate to "Database Models" to view and explore your database models structure. From here you can:

- View model details including fields, relationships, and constraints
- Create new models
- Modify existing models
- Generate migrations based on model changes

### ORM Console

The ORM Console allows you to execute database queries using Django's ORM syntax:

1. Select the target database connection
2. Write your query using Django ORM syntax
3. Execute and view results
4. Save queries for future use

Example query:
```python
from app.models import Product
Product.objects.filter(price__gt=10.0).order_by('-created_at')[:10]
```

### Data Export

Export your data in various formats:

1. Navigate to "Data Export"
2. Select the models/tables to export
3. Choose export format (CSV, JSON, SQL)
4. Configure any format-specific options
5. Generate and download the export file

### Data Visualization

Create charts and graphs based on your database data:

1. Navigate to "Data Visualization"
2. Select data source and fields
3. Choose chart type
4. Configure visualization options
5. Save or export the visualization

## API Documentation

The system provides a REST API for programmatic access:

```
/api/v1/databases/ - List all database connections
/api/v1/models/ - List all models
/api/v1/query/ - Execute ORM queries
/api/v1/export/ - Export data
```

See the [API Documentation](/docs/api.md) for detailed information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django framework
- Bootstrap for the frontend components
- Font Awesome for icons
- All contributors who have helped improve this project

## Contact

Project Link: [https://github.com/yourusername/database-management-system](https://github.com/yourusername/database-management-system)

---

Made with ❤️ by [Your Name/Organization]
