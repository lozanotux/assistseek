from flask import (
    Flask,
    request,
    jsonify,
    render_template
)
import requests
import json
import re


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def call(text):
    """
    This function calls the API deepseek model with a given text to geberate
    a response based on a text prompt.

    Args:
        text (str): input text

    Returns:
        str: response
    """
    url = "http://localhost:11434/api/generate" #  Deepseek API URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-r1:1.5b",
        "prompt": text,
        "stream": False, #  Needed to return the response in a single string
        "options": {
            "temperature": 0 #  Higher temperature, output more random text
        }
    }
    # HTTP Request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_text = json.loads(response.text)['response']
    # Remove the <think> tag from the response using a regular expression
    filtered_text = re.sub(
        r'<think>.*?</think>', '',
        response_text, flags=re.DOTALL
    )
    return filtered_text.strip()


@app.route('/chatbase', methods=['POST'])
def chatbase():
    """
    Chatbase endpoint, this function receive a input text to be processed
    by deepseek model and return the output.

    Returns:
        json: response
    """
    user_message = request.json.get('message', '')
    prompt = (
        "Always keep answering in Spanish and fully attend the the next"
        f" user's query: {user_message}"
    )
    output = call(prompt)

    return jsonify({'response': output})


if __name__ == '__main__':
    app.run(debug=True)
