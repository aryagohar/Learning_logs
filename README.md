# Learning Logs

A web application built with **Django** that allows users to organize
and track their learning journey. Users can create topics, add entries,
manage their personal learning logs, and optionally make topics public
for other visitors to view.

## Features

- User registration and authentication
- Create, edit, and delete topics
- Create, edit, and delete entries
- Public and private topics
- Search topics and entries
- Responsive interface using Bootstrap 5
- Django admin interface

## Technologies Used

- Python
- Django
- Bootstrap 5
- SQLite (development)
- HTML/CSS

## Installation

Clone the repository:

    git clone https://github.com/aryagohar/learning_logs.git
    cd learning_logs

Create and activate a virtual environment:

    python -m venv .venv

Windows:

    .venv\Scripts\activate

Linux/macOS:

    source .venv/bin/activate

Install the dependencies:

    pip install -r requirements.txt

Apply database migrations:

    python manage.py migrate

Create an administrator account (optional):

    python manage.py createsuperuser

Run the development server:

    python manage.py runserver

Open your browser and visit:

    http://127.0.0.1:8000/

## Project Structure

    learning_logs/
    ├── accounts/
    ├── learning_logs/
    ├── ll_project/
    ├── templates/
    ├── manage.py
    └── requirements.txt

## About

This project was originally developed while studying Django and has been
gradually extended with additional functionality as part of my journey
toward becoming a professional Python and Django developer.

## License

This project is intended for educational and portfolio purposes.

## 👤 Author

**(GitHub: aryagohar)**

I am continuously improving my skills in Python, Django, automation, and
AI integration while building practical projects for my professional
portfolio.

## ⭐ Support

If you found this project useful or interesting, consider giving it a ⭐
on GitHub.
