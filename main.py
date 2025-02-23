from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store tasks in memory (you might want to use a database in production)
tasks = []
task_id_counter = 1

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
