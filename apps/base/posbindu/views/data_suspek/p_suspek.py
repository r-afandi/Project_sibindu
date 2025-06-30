import io
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Frame
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
from django.contrib.staticfiles import finders
from ...models.m_about import About
from reportlab.lib import utils

def generate_receipt(id_suspect, nik, nama, alamat, items, diagnosa, penanganan, petugas, pelaksanaan):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    about = About.objects.get(id=1)

    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")
    filename = f'{id_suspect}_{nama}_hasil_diagnosa_{tanggal}.pdf'

    logo_path = finders.find('ico/sibindu-white.min.png')
    logo = ImageReader(logo_path)
    c.drawImage(logo, 8.5 * cm, 25.5 * cm, width=4 * cm, height=2 * cm, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(10.5 * cm, 24.5 * cm, about.nama)

    c.setFont("Helvetica", 12)
    c.drawCentredString(10.5 * cm, 23.5 * cm, "Tanggal: " + tanggal)
    c.line(1 * cm, 22.5 * cm, 20 * cm, 22.5 * cm)

    c.drawString(2 * cm, 21.5 * cm, f"NIK: {nik}")
    c.drawString(2 * cm, 20.5 * cm, f"Nama: {nama}")
    c.drawString(2 * cm, 19.5 * cm, f"Alamat: {alamat}")
    c.drawString(12 * cm, 21.5 * cm, f"Diagnosa: {diagnosa}")
    c.drawString(12 * cm, 20.5 * cm, f"Petugas: {petugas}")
    c.drawString(12 * cm, 19.5 * cm, f"Pelaksanaan: {pelaksanaan}")
    c.line(1 * cm, 18.5 * cm, 20 * cm, 18.5 * cm)

    y = 17.5 * cm
    col_width = 9 * cm
    col_count = 0
    for i, item in enumerate(items):
        if col_count == 2:
            y -= 1 * cm
            col_count = 0

        if i % 2 == 0:
            c.drawString(2 * cm, y, str(item["gejala"]))
            c.drawString(8 * cm, y, ":")
            c.drawString(9 * cm, y, str(item["hasil"]))
            col_count += 1
        else:
            c.drawString(12 * cm, y, str(item["gejala"]))
            c.drawString(18 * cm, y, ":")
            c.drawString(19 * cm, y, str(item["hasil"]))
            col_count += 1
    c.line(1 * cm, y - 1 * cm, 20 * cm, y - 1 * cm)

    # Prepare the penanganan text
    penanganan_list = [f"- {item}" for item in penanganan.split(" - ")]
    penanganan_style = ParagraphStyle(
        'penanganan_style',
        fontName="Helvetica",
        fontSize=12,
        spaceAfter=6,
        leading=15,
    )
    
    # Convert the pen anganan list to a string with HTML line breaks
    penanganan_text = "<br/>".join(penanganan_list)
    
    # Create a Paragraph object to render the penanganan text
    penanganan_paragraph = Paragraph(penanganan_text, penanganan_style)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y - 2 * cm, "Penanganan:")

    # Create a frame to hold the penanganan paragraph
    penanganan_frame = Frame(2 * cm, y - 8 * cm, 18 * cm, 5 * cm, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    penanganan_frame.addFromList([penanganan_paragraph], c)

    c.showPage()
    c.save()

    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response