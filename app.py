from flask import Flask, request, jsonify
from youtube_transcript_api.formatters import TextFormatter
from flask_cors import CORS
import requests
from youtube_transcript_api._errors import TranscriptsDisabled

app = Flask(__name__)
CORS(app)

SCRAPERAPI_KEY = '56ae0a6c7f65480531d0fcd3b660e33f'

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'YouTube Transcript API is running', 'usage': '/api/transcript/<video_id>'})

@app.route('/api/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        scraper_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}"
        response = requests.get(scraper_url)

        print("\nRAW HTML RESPONSE:\n", response.text[:1000])  # Print first 1000 chars to debug

        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        return jsonify({'transcript': text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.run(host='0.0.0.0', port=3000)
