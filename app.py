from flask import Flask, render_template, request, send_file, jsonify
from pdf2docx import Converter
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document

app = Flask(__name__)

# Halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Konversi PDF ke Word
@app.route('/convert-pdf-to-word', methods=['POST'])
def convert_pdf_to_word():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Mendapatkan nama file asli
    filename = file.filename
    # Membuat file sementara untuk PDF yang diupload
    pdf_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(pdf_file.name)

    # Membuat nama file Word hasil konversi dengan nama asli
    word_filename = os.path.splitext(filename)[0] + '.docx'

    # Mengonversi PDF ke Word
    word_file = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    cv = Converter(pdf_file.name)
    cv.convert(word_file.name, start=0, end=None)
    cv.close()

    # Mengirimkan file hasil konversi dengan nama yang sesuai
    return send_file(word_file.name, as_attachment=True, download_name=word_filename)

# Konversi Word ke PDF
@app.route('/convert-word-to-pdf', methods=['POST'])
def convert_word_to_pdf():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Mendapatkan nama file asli
    filename = file.filename
    # Menyimpan file Word sementara
    word_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(word_file.name)

    # Membuat nama file PDF hasil konversi dengan nama asli
    pdf_filename = os.path.splitext(filename)[0] + '.pdf'

    # Mengonversi Word ke PDF
    pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    c = canvas.Canvas(pdf_file.name, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)

    doc = Document(word_file.name)

    # Menulis isi dokumen Word ke dalam PDF
    for para in doc.paragraphs:
        text_object.textLine(para.text)

    c.drawText(text_object)
    c.showPage()
    c.save()

    # Mengirimkan file PDF hasil konversi dengan nama yang sesuai
    return send_file(pdf_file.name, as_attachment=True, download_name=pdf_filename)

if __name__ == "__main__":
    app.run(debug=True)

