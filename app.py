from flask import Flask, request, jsonify, render_template
import re
import random
from datetime import datetime
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'api key '

# Simple pattern-response pairs for basic interactions
patterns = [
    (r'\b(hi|hello|hey)\b', ['Hello!', 'Hi there!', 'Hey!']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Bye!']),
    (r'thank you|thanks', ['You\'re welcome!', 'Glad I could help!', 'My pleasure!']),
    (r'who are you', ['I am assistant designed by Madhurjya']),
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message', '')
    bot_response = generate_response(user_message)
    return jsonify({
        'response': bot_response,
        'timestamp': datetime.now().strftime('%H:%M')
    })

def generate_response(message):
    # Check for simple patterns first
    for pattern, responses in patterns:
        if re.search(pattern, message.lower()):
            return random.choice(responses)
    
    # If no pattern matches, use GPT-3.5-turbo
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named AdvancedBot."},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error in GPT-3 API call: {e}")
        return "I'm having trouble processing that request. Can you try asking something else?"

if __name__ == '__main__':
    app.run(debug=True)