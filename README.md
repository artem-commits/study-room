# Study App

A Django-based web application for educational purposes.

## Project Overview

This is a Django web application that provides a platform for educational content and user interaction. The project uses Django 4.2 and includes various features for user authentication and content management.

## Features

- User authentication and authorization
- REST API support with Django REST Framework
- Social authentication integration
- Media file handling
- Static file management

## Tech Stack

- Python 3.x
- Django 4.2.21
- Django REST Framework 3.16.0
- SQLite Database
- Social Authentication (social-auth-app-django)
- Pillow for image processing

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd study_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
study_app/
├── apps/               # Application modules
├── media/             # User-uploaded files
├── static/            # Static files
├── staticfiles/       # Collected static files
├── templates/         # HTML templates
├── study_app/         # Project configuration
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## API Documentation

The project uses DRF Spectacular for API documentation. Access the API documentation at:
- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/study_app](https://github.com/yourusername/study_app) 