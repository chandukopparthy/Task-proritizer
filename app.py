from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from config import MONGOURI
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient(MONGOURI)
db = client["task_db"]
tasks = db["tasks"]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        "title": data['title'],
        "description": data['description'],
        "due_date": data['due_date'],
        "due_time": data.get('due_time', ''),
        "priority": data.get('priority', '').strip()
    }
    result = tasks.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return jsonify(task)

@app.route('/get_tasks')
def get_tasks():
    sort_by = request.args.get('sort_by', 'due_date')
    all_tasks = list(tasks.find().sort(sort_by, 1))
    for task in all_tasks:
        task['_id'] = str(task['_id'])
    return jsonify(all_tasks)

@app.route('/delete/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks.delete_one({'_id': ObjectId(task_id)})
    return jsonify({"deleted": result.deleted_count > 0})

if __name__ == '__main__':
    app.run(debug=True,host="192.168.200.235")
