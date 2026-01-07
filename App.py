from flask import Flask, request, send_file, render_template_string
import pandas as pd
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pdf2docx import Converter
from PIL import Image
import os

app = Flask(__name__)

# --- 🎨 ULTRA-LUXURY WEBSITE DESIGN ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboWork AI | Professional Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #2563eb; --dark: #1e293b; --bg: #f8fafc; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); margin: 0; color: var(--dark); }
        .navbar { background: white; padding: 1rem 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-size: 22px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 8px; }
        .wallet { background: #10b981; color: white; padding: 6px 15px; border-radius: 20px; font-weight: 600; font-size: 14px; }
        .hero { text-align: center; padding: 60px 20px; }
        .hero h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; padding: 20px; }
        .card { background: white; width: 300px; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: 0.3s; border-top: 4px solid var(--primary); }
        .card:hover { transform: translateY(-10px); }
        .price { color: var(--primary); font-weight: 700; margin-bottom: 15px; display: block; }
        input[type=file] { width: 100%; margin-bottom: 20px; font-size: 12px; }
        .btn { background: var(--primary); color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: 700; cursor: pointer; }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo"><i class="fa-solid fa-bolt"></i> TurboWork AI</div>
        <div class="wallet">💰 Balance: ₹500</div>
    </div>
    <div class="hero">
        <h1>Professional Tools for Modern Freelancers</h1>
        <p>Convert your files instantly with AI power.</p>
    </div>
    <div class="container">
        <div class="card">
            <h3>📊 PDF to Excel</h3>
            <span class="price">₹10 / File</span>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit" name="task" value="excel" class="btn">Start Conversion</button>
            </form>
        </div>
        <div class="card">
            <h3>👁️ Image to Text</h3>
            <span class="price">₹20 / File</span>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit" name="task" value="ocr" class="btn">Extract Text</button>
            </form>
        </div>
        <div class="card">
            <h3>📝 PDF to Word</h3>
            <span class="price">₹5 / File</span>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit" name="task" value="word" class="btn">Convert to Docx</button>
            </form>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    task = request.form.get('task')
    file.save("input_file")
    try:
        if task == 'excel':
            data = []
            with pdfplumber.open("input_file") as pdf:
                for p in pdf.pages:
                    table = p.extract_table()
                    if table: data.extend(table)
            pd.DataFrame(data).to_excel("out.xlsx", index=False)
            return send_file("out.xlsx", as_attachment=True)
        elif task == 'ocr':
            # Note: Cloud deployment needs tesseract installed
            text = pytesseract.image_to_string(Image.open("input_file"))
            with open("out.txt", "w") as f: f.write(text)
            return send_file("out.txt", as_attachment=True)
        elif task == 'word':
            cv = Converter("input_file")
            cv.convert("out.docx")
            cv.close()
            return send_file("out.docx", as_attachment=True)
    except Exception as e: return str(e)

if __name__ == '__main__':
    app.run(debug=True)
