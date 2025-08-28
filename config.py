import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///instance/kelnic.db'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PAYMENT_API_KEY = os.environ.get('PAYMENT_API_KEY')
    PAYMENT_API_URL = os.environ.get('PAYMENT_API_URL') or 'https://api.paymentgateway.com/v1/'
