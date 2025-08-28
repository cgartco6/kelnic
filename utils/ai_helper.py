import openai
import os
import json
from datetime import datetime

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_course_content(topic, level="beginner", duration="4 weeks"):
    """
    Generate course content using AI
    """
    prompt = f"""
    Create a comprehensive course outline for {topic} at {level} level.
    The course should be {duration} long and include:
    1. Learning objectives
    2. Weekly breakdown
    3. Key concepts
    4. Practical exercises
    5. Assessment criteria
    
    Topic: {topic}
    """
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating course content: {e}")
        return f"# {topic.title()} Course\n\nA comprehensive course on {topic} for {level} level students."

def generate_product_description(product_name, features):
    """
    Generate product description using AI
    """
    prompt = f"""
    Write a compelling product description for {product_name} with these features: {', '.join(features)}.
    The description should be engaging, highlight benefits, and include a call to action.
    Target audience: South African businesses.
    """
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating product description: {e}")
        return f"{product_name} - A premium service offering {', '.join(features)}."

def answer_customer_question(question, context=""):
    """
    Answer customer questions using AI
    """
    prompt = f"""
    As a customer service representative for Kelnic Solutions, answer this question: {question}
    Context: {context}
    Company: Kelnic Solutions - AI-powered digital services and courses for South African businesses.
    Services: AI content creation, algorithm development, security scripts, marketing campaigns, responsive websites.
    Courses: AI programming, cybersecurity, data science.
    Provide a helpful, friendly, and professional response.
    """
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I apologize, but I'm having trouble processing your request right now. Please contact our support team at 084 543 7641 or info@kelnic.co.za for assistance."
