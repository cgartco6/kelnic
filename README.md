# Kelnic Solutions - AI-Powered E-Commerce Platform

A fully responsive e-commerce website with AI integration, offering digital services and courses tailored for the South African market.

## Features

- AI-powered content generation and customer support
- Real-time shopping cart and checkout
- Downloadable courses with instant access after payment
- Responsive design for all devices
- South African payment integration
- User authentication and dashboard

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (copy .env.example to .env and update values)
6. Initialize the database: `python -c "from utils.database import init_db; init_db()"`
7. Run the application: `python app.py`

## Environment Variables

- `SECRET_KEY`: Flask secret key for session management
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `PAYMENT_API_KEY`: Payment gateway API key
- `PAYMENT_API_URL`: Payment gateway API URL

## Project Structure

- `app.py`: Main Flask application
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `utils/`: Utility modules (AI, payment processing, database)
- `courses/`: Course content files
- `data/`: JSON data files
- `instance/`: Database file
