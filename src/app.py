"""
This is the main script of the application. It makes use of the Chatbot class
to manage the client conversation, look for information into the policy 
documents and answer the questions. The web interface is implemented using
Flask.
"""
import sys
import os

from flask import Flask, render_template, request, jsonify

from modules.document_loader import load_policies
from modules.chatbot import PoliciesChatbot


app = Flask(__name__)

policies_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../policies'))
policies = load_policies(policies_path)

chatbot = PoliciesChatbot(policies, "gpt-4o-mini")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    answer = chatbot.run_step(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
