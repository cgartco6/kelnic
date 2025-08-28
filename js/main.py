from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load products and courses data
with open('data/products.json', 'r') as f:
    products = json.load(f)

with open('data/courses.json', 'r') as f:
    courses = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/courses')
def get_courses():
    return jsonify(courses)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    # Process payment here (integrate with payment gateway)
    # For now, we'll simulate successful payment
    order_id = generate_order_id()
    
    # Save order to database
    save_order(data, order_id)
    
    return jsonify({
        'success': True,
        'order_id': order_id,
        'message': 'Payment processed successfully'
    })

@app.route('/api/download/<course_id>')
def download_course(course_id):
    # Verify user has purchased the course
    course_path = f"courses/{course_id}/content.zip"
    if os.path.exists(course_path):
        return send_file(course_path, as_attachment=True)
    else:
        return jsonify({'error': 'Course not found'}), 404

def generate_order_id():
    return f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"

def save_order(order_data, order_id):
    # Save order to database or file
    order_data['order_id'] = order_id
    order_data['order_date'] = datetime.now().isoformat()
    
    with open(f'orders/{order_id}.json', 'w') as f:
        json.dump(order_data, f, indent=2)

if __name__ == '__main__':
    app.run(debug=True)
