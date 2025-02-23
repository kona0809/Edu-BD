from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure your .env file has this key

# Store tasks in memory (you might want to use a database in production)
tasks = []
task_id_counter = 1

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    data = request.json
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data['description'],
        'time': data['time'],
        'completed': False
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task)

@app.route('/api/ai-help', methods=['POST'])
def ai_help():
    try:
        data = request.json
        question = data['question']
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": question}
            ]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Removed app.run() line for Gunicorn

