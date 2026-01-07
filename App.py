from flask import Flask, request, send_file, render_template_string
import pandas as pd
import pdfplumber
from pdf2docx import Converter
import os

app = Flask(__name__)

# --- 🎨 LUXURY WEBSITE DESIGN ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>TurboWork AI | Pro Suite</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; text-align: center; padding: 20px; }
        .navbar { background: #2563eb; color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; font-size: 20px; }
        .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 20px auto; max-width: 400px; border-top: 5px solid #2563eb; }
        .btn { background: #2563eb; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; font-size: 16px; transition: 0.3s; }
        .btn:hover { background: #1d4ed8; }
        .price { color: #059669; font-weight: bold; font-size: 18px; display: block; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="navbar">⚡ TurboWork AI Professional</div>
    <div class="card">
        <h3>📊 PDF to Excel</h3>
        <span class="price">Charge: ₹10</span>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required style="margin-bottom: 15px;"><br>
            <button type="submit" name="task" value="excel" class="btn">Convert & Download</button>
        </form>
    </div>
    <div class="card">
        <h3>📝 PDF to Word</h3>
        <span class="price">Charge: ₹5</span>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required style="margin-bottom: 15px;"><br>
            <button type="submit" name="task" value="word" class="btn">Convert & Download</button>
        </form>
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
        elif task == 'word':
            cv = Converter("input_file")
            cv.convert("out.docx")
            cv.close()
            return send_file("out.docx", as_attachment=True)
    except Exception as e: return str(e)
    return "Done"

if __name__ == '__main__':
    app.run()
