from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__, static_folder='.', static_url_path='')

# Knowledge base data parser (Replacing heavy RAG LLM)
KNOWLEDGE_BASE = {
    "papers": "Paper submissions are open until June 30th. Papers can be submitted via the submission link in the Call for Papers section.",
    "accommodations": "Conference accommodations are located at the Grand Hyatt Regency at a discounted rate of $179/night.",
    "pricing": "Registration pricing: Student/Researcher rate is $199, Academic rate is $399, and Industry rate is $699.",
    "payment": "Payments can be made via credit card, PayPal, or wire transfer through our secure payment links in the Pricing section.",
    "schedule": "The conference takes place over 3 days, featuring keynote speeches, paper presentation tracks, and workshops."
}

def parse_data(query: str) -> str:
    query_lower = query.lower()
    
    if any(k in query_lower for k in ["paper", "submit", "call for paper", "author"]):
        return KNOWLEDGE_BASE["papers"]
    elif any(k in query_lower for k in ["hotel", "stay", "accommodation", "room", "location"]):
        return KNOWLEDGE_BASE["accommodations"]
    elif any(k in query_lower for k in ["price", "cost", "fee", "ticket", "pricing"]):
        return KNOWLEDGE_BASE["pricing"]
    elif any(k in query_lower for k in ["pay", "payment", "card", "checkout"]):
        return KNOWLEDGE_BASE["payment"]
    elif any(k in query_lower for k in ["schedule", "date", "agenda", "time"]):
        return KNOWLEDGE_BASE["schedule"]
    else:
        return "I can help with information about paper submissions, accommodations, registration pricing, and payments. What would you like to know?"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')
    
    # Fast deterministic parsing response
    bot_response = parse_data(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)