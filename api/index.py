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
    HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Is Power</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
	<style>
        * {
            font-family: "Poppins", sans-serif;
            box-sizing: border-box;
        }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f8f9fa;
            overflow-x: hidden;
            padding: 20px;
            flex-direction: column;
        }
        .container {
            text-align: center;
            width: 100%;
            max-width: 600px;
            transition: transform 0.5s ease-out;
        }
        h1 {
            color: #202124;
            font-size: 3rem;
            margin-bottom: 20px;
        }
        #topicInput {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #dfe1e5;
            border-radius: 24px;
            outline: none;
            transition: box-shadow 0.3s, transform 0.5s ease-out;
        }
        #topicInput:focus {
            box-shadow: 0 1px 6px rgba(32,33,36,.28);
            border-color: rgba(223,225,229,0);
        }
        #generateBtn {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 14px;
            color: #202124;
            background-color: #f8f9fa;
            border: 1px solid #f8f9fa;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        #generateBtn:hover {
            box-shadow: 0 1px 1px rgba(0,0,0,.1);
            border: 1px solid #dadce0;
            color: #202124;
        }
        #generateBtn:active {
            box-shadow: 0 3px 3px rgba(0,0,0,.1);
        }
        #generateBtn:disabled {
            background-color: #e0e0e0;
            color: #9e9e9e;
            border: 1px solid #e0e0e0;
            cursor: not-allowed;
            box-shadow: none;
        }
        #loadingScreen {
            display: none;
            margin-top: 20px;
        }
        .timer {
            font-size: 14px;
            color: #5f6368;
            margin-top: 10px;
        }
		.content-info .timer {
			text-align: right;
		}
        #contentContainer {
            display: none;
            opacity: 0;
            transition: opacity 0.5s ease-out;
            width: 80%;
            max-width: 800px;
            text-align: center;
        }
        #contentContainer.visible {
            opacity: 1;
        }
        .content-info {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .content-text {
            font-size: 1rem;
            color: #5f6368;
            text-align: left;
            margin-top: 15px;
        }
        .content-text h1 {
            font-size: 24px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Knowledge Is Power</h1>
        <input type="text" id="topicInput" placeholder="Enter a topic and press Enter" autocomplete="off">
        <button id="generateBtn">Generate Info</button>
        <div id="loadingScreen">
            Generating Information... Please wait.
            <div id="generationTimer" class="timer"></div>
        </div>
    </div>
    <div id="contentContainer">
        <div class="content-info">
            <div id="completionTime" class="timer"></div>
            <div id="contentText" class="content-text"></div>
        </div>
    </div>

    <script>
        const topicInput = document.getElementById('topicInput');
        const generateBtn = document.getElementById('generateBtn');
        const loadingScreen = document.getElementById('loadingScreen');
        const contentContainer = document.getElementById('contentContainer');
        const container = document.querySelector('.container');
        const generationTimer = document.getElementById('generationTimer');
        const completionTime = document.getElementById('completionTime');
        const contentText = document.getElementById('contentText');

        let startTime;
        let timerInterval;

        function updateTimer() {
            const elapsed = Date.now() - startTime;
            const seconds = (elapsed / 1000).toFixed(1);
            generationTimer.textContent = `Time elapsed: ${seconds}s`;
        }

        function generateContent() {
            const topic = topicInput.value.trim();
            if (topic) {
                startTime = Date.now();
                timerInterval = setInterval(updateTimer, 100);
                
                topicInput.disabled = true;
                generateBtn.disabled = true;
                loadingScreen.style.display = 'block';
                contentContainer.style.display = 'none';
                contentContainer.classList.remove('visible');

                fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ topic: topic }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        clearInterval(timerInterval);
                        const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
                        completionTime.textContent = `Generation completed in ${totalTime} seconds`;
                        
                        contentText.innerHTML = marked.parse(data.text);
                        
                        loadingScreen.style.display = 'none';
                        contentContainer.style.display = 'block';
                        
                        setTimeout(() => {
                            contentContainer.classList.add('visible');
                        }, 100);
                    }
                })
                .catch(error => {
                    clearInterval(timerInterval);
                    console.error('Error:', error);
                    loadingScreen.style.display = 'none';
                    generationTimer.textContent = 'Generation failed';
                })
                .finally(() => {
                    topicInput.disabled = false;
                    generateBtn.disabled = false;
                });
            }
        }

        topicInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                generateContent();
            }
        });

        generateBtn.addEventListener('click', generateContent);
    </script>
</body>
</html>
    """
    return HTML

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