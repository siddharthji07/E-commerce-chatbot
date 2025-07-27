from flask import Flask, render_template, request, jsonify
from utils import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/query", methods=["POST"])
def process_message():
    user_message = request.json.get("user_message")
    chat_history=[]
    chat_history.append(user_message)
    print("Received user message:", user_message)
    answer = get_answer(user_message)
    print(answer)
    return jsonify({"message": answer})

if __name__ == '__main__':
    app.run()
