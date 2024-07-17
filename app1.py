from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the generative model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Create a Flask app
app = Flask(__name__)

# Function to get response from the Gemini model
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return [chunk.text for chunk in response]

# Define a route for the chatbot API
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    question = data.get('question', '')
    if question:
        response = get_gemini_response(question)
        return jsonify({'response': response})
    return jsonify({'error': 'No question provided'}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
