import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SCRAPERAPI_KEY = '56ae0a6c7f65480531d0fcd3b660e33f'

def get_transcript_through_scraperapi(video_id):
    url = f'https://www.youtube.com/api/timedtext?lang=en&v={video_id}'
    scraperapi_url = f'http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={url}'
    
    response = requests.get(scraperapi_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch transcript: HTTP {response.status_code}")
    
    # The transcript comes as XML — parse it:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(response.text)
    transcript_text = ' '.join([elem.text for elem in root.findall('text') if elem.text])
    return transcript_text

@app.route('/api/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id):
    try:
        transcript_text = get_transcript_through_scraperapi(video_id)
        if not transcript_text:
            return jsonify({'error': 'Transcript not available or empty'}), 404
        return jsonify({'transcript': transcript_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
