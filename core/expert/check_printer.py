

from ctypes import alignment
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def generate_receipt(items, diagnosa,penanganan):

    w=400
    h=580
    print(f'w={w}, h={h}, cm={cm}')
    # Buat objek canvas
    c = canvas.Canvas("receipt.pdf",pagesize=(w,h))

    # Atur font dan ukuran font
    c.setFont("Helvetica", 12)

    # Cetak judul struk

    c.drawString(cm, h - cm * 2,"POSBINDU PTM DESA GOGIK")

    # Cetak tanggal dan waktu
    c.drawString(cm, h - cm * 3, "Tanggal: " + datetime.now().strftime("%d/%m/%Y %H:%M"))

    # Cetak garis pemisah
    c.line(0, h-cm * 4, w, h-cm * 4)

    # Cetak daftar item
    y = h - cm * 5
    for item in items:
        c.drawString(cm, y, item["gejala"])
        c.drawString(cm * 5, y, item["hasil"])
        y -= cm 

    # Cetak garis total
    c.line(0, h-cm * 9,w, h-cm * 9)

    # Cetak total harga
    c.drawString(cm, h-cm * 10, "Diagnosa: " + str(diagnosa))
    c.drawString(cm, h-cm * 11, "penanganan: " + str(penanganan))


    # Simpan file PDF
    c.save()

# Contoh penggunaan
diagnosa= 'Diabetes'

penanganan='Periksa ke dokter'



# Ambil data dari queryset
items = [
    {
        "gejala":"sakit","hasil":'30'
    }
]

generate_receipt(items, diagnosa, penanganan)
