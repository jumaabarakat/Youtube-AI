from flask import Flask, request, jsonify
from youtube_generator import extract_video_id, get_video_transcript, generate_summary

# Initialize Flask app
app = Flask(__name__)

@app.route('/generate-summary', methods=['POST'])
def generate_summary_api():
    try:
        data = request.json
        url = data.get('youtube_url')
        language = data.get('language', 'English')
        type_of_summary = data.get('type_of_summary', 'Short')

        # Validate inputs
        if not url or language not in ['Arabic', 'English'] or type_of_summary not in ['Detailed', 'Short']:
            return jsonify({"error": "Invalid input"}), 400
        
        # Extract video ID from the URL
        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400
        
        # Get video transcript
        transcript_text = get_video_transcript(video_id,language)
        
        # Generate summary based on the transcript
        summary = generate_summary(transcript_text, language, type_of_summary)
        
        # Return the summary as a JSON response
        return jsonify({
            "summary": summary,
            "language": language,
            "type_of_summary": type_of_summary
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
