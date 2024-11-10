from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import os
from scraper import scrape_and_refine_arxiv_paper

app = Flask(__name__, static_folder='frontend', static_url_path='/')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Serve the frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoint to scrape and extract text from arXiv HTML
@app.route('/api/scrape', methods=['POST'])
def scrape_arxiv():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided."}), 400

    try:
        refined_text = scrape_and_refine_arxiv_paper(url)
        if refined_text:
            return jsonify({"text": refined_text})
        else:
            return jsonify({"error": "Failed to extract text."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Endpoint for Text-to-Speech (TTS) conversion
@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided."}), 400

    try:
        tts = gTTS(text)
        output_file = 'output.mp3'
        tts.save(output_file)
        return jsonify({"file": output_file})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to serve the generated audio file
@app.route('/output.mp3')
def get_audio():
    return send_from_directory('.', 'output.mp3')

if __name__ == '__main__':
    app.run(debug=True)
