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
        model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=system_prompt)
        generate_content_config = types.GenerateContentConfig(
	        thinking_config = types.ThinkingConfig(
	            thinking_budget=0,
	        ),
	    )
        response = model.generate_content(prompt, config=generate_content_config)
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
    <link rel="icon" href="https://files.catbox.moe/t7lp7o.webp" />
    <meta name="description" content="Knowpedia: Your ultimate knowledge source. A better, more accurate, and user-friendly alternative to Wikipedia. Find reliable information, in-depth articles, and curated facts across a wide range of topics, all in one place." />
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Knowledge Is Power">
    <meta name="twitter:site" content="@itsnikity">
    <meta name="twitter:description" content="Knowpedia: Your ultimate knowledge source. A user-friendly alternative to Wikipedia. Find reliable information.">
    <meta name="twitter:image" content="https://files.catbox.moe/esn66w.jpeg">
    <meta name="twitter:image:alt" content="Knowpedia">
    <meta property="og:title" content="Knowledge Is Power">
    <meta property="og:site_name" content="Knowpedia">
    <meta property="og:description" content="Knowpedia: Your ultimate knowledge source. A user-friendly alternative to Wikipedia. Find reliable information.">
    <meta property="og:image" content="https://files.catbox.moe/esn66w.jpeg">
    <meta property="og:image:alt" content="Knowpedia">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://knowpedia.vercel.app/">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
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
        padding-bottom: 60px;
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
        padding: 10px 15px;
        font-size: 16px;
        border: 1px solid #dfe1e5;
        border-radius: 24px;
        outline: none;
        box-shadow: 0 1px 6px rgba(32, 33, 36, .0);
        transition: box-shadow 0.3s, transform 0.5s ease-out;
      }

      #topicInput:focus {
        box-shadow: 0 1px 6px rgba(32, 33, 36, .28);
      }

      #generateBtn {
        margin-top: 20px;
        padding: 10px 20px;
        font-size: 14px;
        color: #202124;
        background-color: #f8f9fa;
        border-radius: 20px;
        cursor: pointer;
        box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
        border: 1px solid #dadce0;
        color: #202124;
        transition: all 0.3s ease-out;
      }

      #generateBtn:hover {
        background-color: white;
        box-shadow: 0 2px 2px rgba(0, 0, 0, .4);
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
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

      .footer {
        position: fixed;
        bottom: 0;
        width: auto;
        background-color: white;
        padding: 15px;
        border-top-left-radius: 30px;
        border-top-right-radius: 30px;
        text-align: center;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
      }

      .footer a {
        color: #202124;
        text-decoration: none;
        margin: 0 15px;
        transition: color 0.3s ease;
      }

      .footer a:hover {
        color: #000000;
      }

      .hover-underline-animation {
        display: inline-block;
        position: relative;
      }

      .hover-underline-animation::after {
        content: '';
        position: absolute;
        width: 100%;
        transform: scaleX(0);
        height: 1px;
        bottom: 0;
        left: 0;
        background-color: #000000;
        transform-origin: bottom right;
        transition: transform 0.25s ease-out;
      }

      .hover-underline-animation:hover::after {
        transform: scaleX(1);
        transform-origin: bottom left;
      }

      .input-container {
        position: relative;
        width: 100%;
        margin-bottom: 20px;
      }

      #topicInput {
        padding-right: 50px;
      }

      .pdf-button {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background-color 0.3s ease;
      }

      .pdf-button:hover {
        background-color: rgba(0, 0, 0, 0.05);
      }

      #fileInput {
        display: none;
      }

      .pdf-status {
        position: absolute;
        right: 40px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 12px;
        color: #4CAF50;
        display: none;
      }

      .pdf-status.active {
        display: block;
      }

      #pdf2 {
        display: none;
      }
	  
      .support.hover-underline-animation::after  {
        height: 2px;
      }
	  
	  .support {
		font-weight: bold;
	  }

      @media (max-width: 768px) {
        #contentContainer {
          width: 100%;
        }
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Knowledge Is Power</h1>
      <div class="input-container">
        <input type="text" id="topicInput" placeholder="Enter a topic" autocomplete="off">
        <span class="pdf-status" id="pdfStatus">PDF loaded</span>
        <input type="file" id="fileInput" accept=".pdf">
        <button id="pdf1" class="pdf-button" onclick="document.getElementById('fileInput').click()">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <mask id="lineMdFilePlus0">
              <g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                <path stroke-dasharray="64" stroke-dashoffset="64" d="M13.5 3l5.5 5.5v11.5c0 0.55 -0.45 1 -1 1h-12c-0.55 0 -1 -0.45 -1 -1v-16c0 -0.55 0.45 -1 1 -1Z">
                  <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.6s" values="64;0" />
                </path>
                <path d="M14.5 3.5l2.25 2.25l2.25 2.25z" opacity="0">
                  <animate fill="freeze" attributeName="d" begin="0.6s" dur="0.2s" values="M14.5 3.5l2.25 2.25l2.25 2.25z;M14.5 3.5l0 4.5l4.5 0z" />
                  <set fill="freeze" attributeName="opacity" begin="0.6s" to="1" />
                </path>
                <path fill="#000" fill-opacity="0" stroke="none" d="M19 13c3.31 0 6 2.69 6 6c0 3.31 -2.69 6 -6 6c-3.31 0 -6 -2.69 -6 -6c0 -3.31 2.69 -6 6 -6Z">
                  <set fill="freeze" attributeName="fill-opacity" begin="0.8s" to="1" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M16 19h6">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.8s" dur="0.2s" values="8;0" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M19 16v6">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="1s" dur="0.2s" values="8;0" />
                </path>
              </g>
            </mask>
            <rect width="24" height="24" fill="#333333" mask="url(#lineMdFilePlus0)" />
          </svg>
        </button>
        <button id="pdf2" class="pdf-button" onclick="removePDF()">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <mask id="lineMdFileRemove0">
              <g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                <path stroke-dasharray="64" stroke-dashoffset="64" d="M13.5 3l5.5 5.5v11.5c0 0.55 -0.45 1 -1 1h-12c-0.55 0 -1 -0.45 -1 -1v-16c0 -0.55 0.45 -1 1 -1Z">
                  <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.6s" values="64;0" />
                </path>
                <path d="M14.5 3.5l2.25 2.25l2.25 2.25z" opacity="0">
                  <animate fill="freeze" attributeName="d" begin="0.6s" dur="0.2s" values="M14.5 3.5l2.25 2.25l2.25 2.25z;M14.5 3.5l0 4.5l4.5 0z" />
                  <set fill="freeze" attributeName="opacity" begin="0.6s" to="1" />
                </path>
                <path fill="#000" fill-opacity="0" stroke="none" d="M19 13c3.31 0 6 2.69 6 6c0 3.31 -2.69 6 -6 6c-3.31 0 -6 -2.69 -6 -6c0 -3.31 2.69 -6 6 -6Z">
                  <set fill="freeze" attributeName="fill-opacity" begin="0.8s" to="1" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M17 17l4 4">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.8s" dur="0.2s" values="8;0" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M21 17l-4 4">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="1s" dur="0.2s" values="8;0" />
                </path>
              </g>
            </mask>
            <rect width="24" height="24" fill="#333333" mask="url(#lineMdFileRemove0)" />
          </svg>
        </button>
      </div>
      <button id="generateBtn">Generate Info</button>
      <div id="loadingScreen"> Generating Information... Please wait. <div id="generationTimer" class="timer"></div>
      </div>
    </div>
    <div id="contentContainer">
      <div class="content-info">
        <div id="completionTime" class="timer"></div>
        <div id="contentText" class="content-text"></div>
      </div>
    </div>
    <footer class="footer">
      <a class="hover-underline-animation" href="https://github.com/nikityyy/knowpedia" target="_blank">GitHub</a>
	  <a class="hover-underline-animation support" href="https://buymeacoffee.com/nikity" target="_blank">Support me</a>
      <a class="hover-underline-animation" href="mailto:bergernikita1807@gmail.com">Contact</a>
    </footer>
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
      let PDFText = ""
      let hasText = false;

      function updateTimer() {
        const elapsed = Date.now() - startTime;
        const seconds = (elapsed / 1000).toFixed(1);
        generationTimer.textContent = "Time elapsed: " + seconds + "s";
      }
      document.getElementById('fileInput').addEventListener('change', async function() {
        try {
          const file = this.files[0];
          if (!file) {
            togglePDFDisplay(false);
            return;
          }
          togglePDFDisplay(true);
          if (!file.type.includes('pdf')) {
            throw new Error('Please select a PDF file');
          }
          const fileName = file.name;
          const fileType = fileName.slice(-4);
          const truncatedFileName = fileName.slice(0, 5) + fileType;
          PDFText = `You have access to an extracted PDF file titled '${fileName}', which provides additional knowledge for your responses. When referencing information from this PDF, please specify the exact page number where the information can be found. Ensure that your citations are clear and accurate.\n\n`;
          const arrayBuffer = await readFileAsArrayBuffer(file);
          const pdf = await pdfjsLib.getDocument({
            data: arrayBuffer
          }).promise;
          PDFText += `The PDF has ${pdf.numPages} page(s). You are always given the page you are currently at.\n\n`;
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const text = textContent.items.map(item => item.str).join(' ').trim();
            if (text) {
              hasText = true;
            }
            PDFText += `Page ${i}: ${text}\n\n`;
          }
          if (!hasText) {
            PDFText = "";
          }
        } catch (error) {
          console.error('Error processing PDF:', error);
          togglePDFDisplay(false);
        }
      });

      function readFileAsArrayBuffer(file) {
        return new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.onerror = () => reject(reader.error);
          reader.readAsArrayBuffer(file);
        });
      }

      function togglePDFDisplay(showPDF2) {
        document.getElementById('pdf1').style.display = showPDF2 ? "none" : "flex";
        document.getElementById('pdf2').style.display = showPDF2 ? "flex" : "none";
      }

      function removePDF() {
        document.getElementById('fileInput').value = '';
        document.getElementById('pdf1').style.display = "flex";
        document.getElementById('pdf2').style.display = "none";
        document.getElementById('pdfStatus').classList.remove('active');
        PDFText = "";
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
          fullTopic = PDFText + "The topic the user wants to gain knowledge of is: '" + topic + "'";
          fetch('/generate', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              topic: fullTopic
            }),
          }).then(response => response.json()).then(data => {
            if (data.status === 'success') {
              clearInterval(timerInterval);
              const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
              completionTime.textContent = "Generation completed in " + totalTime + " seconds";
              contentText.innerHTML = marked.parse(data.text);
              loadingScreen.style.display = 'none';
              contentContainer.style.display = 'block';
              setTimeout(() => {
                contentContainer.classList.add('visible');
              }, 100);
            }
          }).catch(error => {
            clearInterval(timerInterval);
            console.error('Error:', error);
            loadingScreen.style.display = 'none';
            generationTimer.textContent = 'Generation failed';
          }).finally(() => {
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
        text_prompt = f"""
		You are writing an encyclopedic article for a Wikipedia-style knowledge base called "Knowpedia."
		Your goal is to produce a clear, factual, and neutral article about the topic: "{topic}".
		
		Follow these rules:
		1. **Language** – Write entirely in the same language as the topic is provided in. If the topic is in multiple languages, use the dominant one.
		2. **Tone** – Neutral, formal, and precise. Avoid opinions, speculation, or promotional language.
		3. **Structure** – Use Markdown with:
		   - A top-level heading (#) for the article title (exact topic name).
		   - An introductory paragraph summarizing the topic in 2–4 sentences.
		   - 2–6 thematic sections (##) covering:
		     - Overview / Definition
		     - History or Origin (if applicable)
		     - Key Concepts, Components, or Features
		     - Related Topics or Impact
		     - Controversies / Criticism (if notable)
		   - A **See also** section with bullet-pointed related topics.
		4. **Content** – Present verified, widely accepted information first. If disputed views exist, describe them with attribution.
		5. **Formatting** – Use lists, tables, or bold keywords when they improve clarity. No excessive formatting.
		6. **Length** – Aim for the depth of a standard Wikipedia article for a mid-sized topic (roughly 500–1000 words).
		
		Return only the Markdown-formatted article, without any extra commentary or system notes.
		"""
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
