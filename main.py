from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from flask_cors import CORS
import json
import os
from datetime import datetime
from utils.ai_helper import generate_course_content, generate_product_description, answer_customer_question
from utils.payment_processor import PaymentProcessor
from utils.database import Database

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Initialize database
db = Database()

# Load products and courses data
with open('data/products.json', 'r') as f:
    products = json.load(f)

with open('data/courses.json', 'r') as f:
    courses = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', products=products, courses=courses)

@app.route('/services')
def services():
    return render_template('services.html', products=products)

@app.route('/courses')
def courses_page():
    return render_template('courses.html', courses=courses)

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/courses')
def get_courses():
    return jsonify(courses)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    if 'user' not in session:
        return jsonify({'error': 'Please login first'}), 401
        
    data = request.get_json()
    user_id = session['user']['id']
    
    # Process payment
    payment_processor = PaymentProcessor()
    payment_result = payment_processor.process_payment(
        data['amount'], 
        'ZAR', 
        data['card_details'],
        session['user']
    )
    
    if payment_result['success']:
        # Save order to database
        order_id = db.create_order(user_id, data['items'], data['amount'], payment_result['transaction_id'])
        
        # Grant access to purchased courses
        for item in data['items']:
            if item['type'] == 'course':
                db.grant_course_access(user_id, item['id'])
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Payment processed successfully'
        })
    else:
        return jsonify({
            'success': False,
            'error': payment_result['error']
        }), 400

@app.route('/api/download/<course_id>')
def download_course(course_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Verify user has purchased the course
    if db.has_course_access(session['user']['id'], course_id):
        course_path = f"courses/{course_id}/content.zip"
        if os.path.exists(course_path):
            return send_file(course_path, as_attachment=True)
    
    return jsonify({'error': 'Course not found or access denied'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.get_user_by_email(email)
        if user and db.check_password(user['id'], password):
            session['user'] = user
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if db.get_user_by_email(email):
            flash('Email already registered', 'error')
        else:
            user_id = db.create_user(name, email, password)
            session['user'] = db.get_user(user_id)
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_courses = db.get_user_courses(session['user']['id'])
    user_orders = db.get_user_orders(session['user']['id'])
    
    return render_template('dashboard.html', 
                         user=session['user'],
                         courses=user_courses,
                         orders=user_orders)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    
    response = answer_customer_question(question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
