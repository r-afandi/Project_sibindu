import io
import base64
from ....models.data_suspek.m_data_suspek import DataSuspek ,Diagnosa
from .....expert.models.m_kepakaran import Gejala
from django.http import HttpResponse,FileResponse
from django.template.loader import render_to_string
from ctypes import alignment
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from datetime import datetime

def generate_receipt(id_suspect,nama,alamat,items, diagnosa,penanganan,petugas):

    w=200
    h=580
    logo = ImageReader('/static/ico/sibindu.png')
    # Buat objek canvas
    tanggal=datetime.now().strftime("%d-%m-%Y-%H:%M")
    filename = f'{id_suspect}_{nama}_hasil_diagnosa_{tanggal}.pdf'
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer,pagesize=(w,h))

    # Atur font dan ukuran font
    c.setFont("Helvetica", 12)

    # Cetak judul struk
    c.drawImage(logo,cm * 2, h-cm , mask='auto')
    c.drawString(cm * 4.5, h - cm,"POSBINDU Desa Gogik")

    # Cetak tanggal dan waktu
    c.drawString(cm * 4.5, h - cm * 2, "Tanggal: " + tanggal)
    # Cetak garis pemisah
    c.line(0, h-cm * 3,w, h-cm * 3)
    c.drawString(cm, h-cm * 4, "Nama: " + str(nama))
    c.drawString(cm * 21, h-cm *4, "Diagnosa: " + str(diagnosa))
    c.drawString(cm * 21, h-cm *5, "Petugas: " + str(petugas))
    c.drawString(cm, h-cm * 5, "Alamat: " + str(alamat))

    # Cetak garis pemisah
    c.line(0, h-cm * 6,w, h-cm * 6)
    # Cetak daftar item

    y = h - cm * 7
    # Cetak daftar item
    for item in items:
        c.drawString(cm, y, str(item["gejala"]))
        c.drawString(cm * 5, y, ":")
        c.drawString(cm * 7, y, str(item["hasil"]) )
        y -= cm 

    # Cetak garis total
    c.line(0, h-cm * 14,w, h-cm * 14)

    # Cetak total harga

    c.drawString(cm, h-cm * 15, "Penanganan: ")
    c.drawString(cm, h-cm * 16, str(penanganan))
    c.showPage()
    c.save()

    buffer.seek(0)
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode to Base64 string
    buffer.close()  # Close the buffer after use
    #html = render_to_string('layouts/hasil_diagnosa.html', {'base64_data': base64_data})
    pdf_bytes = base64.b64decode(base64_data)

    # Prepare HTTP headers
    headers = {
        'title':'Hasil-Diagnosa',
        'Content-Type': 'application/pdf',
        'Content-Disposition':  f'inline; filename="{filename}"',

    }

    # Return HTTP response with PDF content and headers
    return HttpResponse(pdf_bytes, headers=headers)
    



