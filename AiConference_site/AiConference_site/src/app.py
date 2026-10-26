from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
#import ollama
from rag_engine import TwoLlamaEngine

#python backend server, responsible for answering pull requests with push requests

# static_url_path='' allows serving css/, js/, and img/ directly without needing a /static/ folder prefix
app = Flask(__name__, static_folder='.', static_url_path='', template_folder='.')
CORS(app)
#configures Flask web app and instantiates TwoLlamaEngine when the backend app starts.
engine = TwoLlamaEngine(data_dir="./data", db_path="./chroma_db")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')
#defines /api/chat route and extracts user message and mode selection "rag" or "direct"
    mode = data.get('mode','rag')

#Validates inputs, routes request to ask_direct() or ask_rag() based on the mode the user has chose and returns output to JSON
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        # Update 'llama3' to match the model installed on your machine (e.g. 'llama3.2', 'mistral', 'phi3')
        #old response made a raw call to ollama.chat() directly
        # response = ollama.chat(
        #     model='llama3',
        #     messages=[{'role': 'user', 'content': user_message}]
        # )
        # return jsonify({'response': response['message']['content']})

        if mode == 'direct':
             answer = engine.ask_direct(user_message)
        else:
             answer = engine.ask_rag(user_message)

        return jsonify({'response': answer})

    except Exception as e:
        return jsonify({'error': f"Ollama connection error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)