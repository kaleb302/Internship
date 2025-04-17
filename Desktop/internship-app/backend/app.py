from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

def log_request():
    """Log incoming request details"""
    print(f"\n{'='*40}\nNew Request: {request.method} {request.url}")
    print("Headers:", dict(request.headers))
    print("Form Data:", dict(request.form))
    print("Files:", {k: v.filename for k, v in request.files.items()})

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        log_request()  # Log request details
        
        # Validate file upload
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Secure filename and save
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        print(f"File saved to: {save_path}")

        # Return enhanced mock response
        return jsonify({
            "status": "success",
            "message": "File processed successfully",
            "jobs": [
                {
                    "title": "Software Engineer Intern",
                    "company": "Tech Corp",
                    "location": request.form.get('location', 'Remote'),
                    "skills": ["Python", "JavaScript"],
                    "link": "#"
                }
            ],
            "file_details": {
                "original_name": file.filename,
                "saved_name": filename,
                "size": os.path.getsize(save_path)
            }
        })

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = 8000  # Changed from 6000
    app.run(debug=True, port=port, use_reloader=False)
from ai.resume_parser import parse_resume

@app.route('/upload', methods=['POST'])
def upload_resume():
    # ... existing file handling code ...
    resume_data = parse_resume(filepath)
    return jsonify({
        "jobs": [],  # We'll implement this next
        "resume_data": resume_data
    })
    