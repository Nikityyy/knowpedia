from flask import Flask, render_template, request, jsonify, send_file
import os
import warnings
import traceback
import google.generativeai as genai

warnings.filterwarnings('ignore')

app = Flask(__name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
def generate_llm_content_google(prompt, system_prompt="Only answer with the output, no other text before or after the output."):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-8b', system_instruction=system_prompt)
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"LLM Generation error: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400
    
    topic = request.json.get('topic')
    if not topic:
        return jsonify({"status": "error", "message": "Topic is required"}), 400

    try:
        text_prompt = f"Compose a thorough, informative text about '{topic}' that presents the subject neutrally and factually. Include essential details, background information, and any key components or related concepts for a well-rounded explanation. Add a title. Structure the text in Markdown format to enhance readability."
        # text = generate_llm_content(text_prompt)
        text = generate_llm_content_google(text_prompt)

        response = {
            "status": "success",
            "text": text,
        }

        return jsonify(response)

    except Exception as e:
        print(f"Content generation error: {e}")
        raise
    finally:
        pass

if __name__ == '__main__':
    app.run(debug=False, threaded=True)