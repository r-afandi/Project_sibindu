from os import path
from re import U, escape
from urllib import response
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.cache import cache
from django.db.models import Max,Min
from django.contrib.auth.models import User
from numpy import save
from ...models.informasi.m_pengumuman import Pengumuman
from ...models.data_suspek.m_data_suspek import DataSuspek,Diagnosa
from ....expert.models.m_kepakaran import Gejala
from ....decorator import auth_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ....models import Menu
from django.contrib.auth.models import User,Group
from ...forms.data_suspek.f_data_suspek import FormDataSuspek
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .p_suspek import generate_receipt
from collections import defaultdict
from ....views import add_notify
from ....models import Notifikasi
from django.db.models import Case, When, IntegerField
#print
from ...models.m_about import About
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
from reportlab.lib.utils import ImageReader
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

decorators = [login_required,auth_required(required_permissions=['view_data_suspek', 'add_data_suspek', 'change_data_suspek', 'delete_data_suspek'], model_class=DataSuspek), add_notify(feature='data suspek', view_name='data_suspek:data_suspek',model=DataSuspek, name_field='nama')]

@method_decorator(decorators, name='dispatch')
class DataSuspekListView(View):
    def get(self, request):
        user = request.user
        # Annotate each record with the minimum id for each nik
        min_id_per_nik = DataSuspek.objects.values('nik').annotate(min_id=Min('id')).values('min_id')

        # Filter data based on the minimum id per nik
        data = DataSuspek.objects.filter(id__in=min_id_per_nik).only(
            'id', 'nik', 'nama', 'gender', 'alamat', 'umur', 'diagnosa'
        ).select_related('gender', 'diagnosa').order_by('-id')

        # Convert the queryset to a list before caching
        data = list(data)
        form = FormDataSuspek()
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()
        pengumuman = Pengumuman.objects.filter(jenis_id=1).order_by('-tanggal')
        # Mendapatkan tanggal pengumuman yang unik
        tanggal_pengumuman = pengumuman.values_list('tanggal', flat=True).distinct()


        # Filter data suspek sesuai tanggal pengumuman
        suspek = DataSuspek.objects.filter(tanggal__in=tanggal_pengumuman).only(
            'id', 'nik', 'nama', 'gender', 'alamat', 'umur', 'diagnosa'
        ).select_related('gender', 'diagnosa').order_by('-tanggal')
        gejala_data = Gejala.objects.only('id', 'nama', 'alias', 'jenis').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                )
            ).order_by('jenis_order')
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'pengumuman_list': pengumuman,
            'suspek_list': suspek,
            'menu': request.menu,
            'groups': request.groups,
   
        }
        return render(request, 'office/data_suspek/data_suspek.html', context)

    def post(self, request):
        user=request.user
        print('user',user.id)
        if request.method == 'POST':
            form = FormDataSuspek(request.POST)
            if form.is_valid(): 

                form.instance.petugas_id = user.id
                form.save()
                return redirect('data_suspek:data_suspek')
        return render(request, 'office/data_suspek/add_data_suspek.html')

class PrintDataSuspekView(View):
    def get(self, request, id):
        try:
            # Mengambil objek data_suspek berdasarkan id
            data_suspek = get_object_or_404(DataSuspek, id=id)

            # Mengambil data gejala dengan pengurutan sesuai jenis
            gejala_data = Gejala.objects.only('id', 'nama', 'alias', 'jenis').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                )
            ).order_by('jenis_order')

            # Fungsi untuk mengganti nilai 1 menjadi "Ya" dan 2 menjadi "Tidak"
            def ganti_nilai(nilai):
                return "Ya" if nilai == 1 else "Tidak" if nilai == 2 else nilai

            # Gabungkan data gejala yang ada
            data = f"{data_suspek.data_gejala},{data_suspek.data_khusus},{data_suspek.data_luar},{data_suspek.data_dalam}".split(',')

            # Kumpulkan nama gejala
            gejala = [gejala_item.nama for gejala_item in gejala_data]

            # Persiapkan daftar items yang akan dicetak
            items = []
            for i in range(len(gejala)):
                try:
                    # Pastikan hanya nilai yang valid diproses
                    nilai_hasil = int(data[i])  # Coba ubah ke integer
                    hasil = ganti_nilai(nilai_hasil)
                except (ValueError, IndexError):
                    # Jika gagal konversi atau tidak ada nilai, tetap gunakan nilai aslinya
                    hasil = data[i] if i < len(data) else 'N/A'

                # Buat pasangan gejala dan hasil
                items.append({
                    "gejala": gejala[i],
                    "hasil": hasil,
                })

            # Cek apakah penanganan kosong, jika ya ambil dari Diagnosa
            if not data_suspek.penanganan:
                diagnosa = get_object_or_404(Diagnosa, id=data_suspek.diagnosa_id)
                penanganan = mark_safe(diagnosa.penanganan)  # Mark as safe
            else:
                penanganan = mark_safe(data_suspek.penanganan)  # Mark as safe

            # Cetak hasil receipt
            print_hasil = generate_receipt(
                data_suspek.id, 
                data_suspek.nik, 
                data_suspek.nama, 
                data_suspek.alamat, 
                items, 
                data_suspek.diagnosa, 
                penanganan,  # Menggunakan penanganan yang sudah dicek
                data_suspek.petugas, 
                data_suspek.tanggal
            )

            return print_hasil
        except Exception as e:
            error_handle = f"Data belum sempurna, silahkan restart page. Error: {e}"
            return render(request, 'error_template.html', {'error': error_handle})
@method_decorator(decorators, name='dispatch')
class DataSuspekView(View):
    def get(self,request,nik):
        user = request.user
     
        data = DataSuspek.objects.filter(nik=nik).order_by('-tanggal')
        data_dict = defaultdict(list)
            
        diagnosa = Diagnosa.objects.all()
        nama_tabel=Gejala.objects.only('id','nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=2),
                    When(jenis='data_khusus', then=3),
                    When(jenis='data_luar', then=0),
                    When(jenis='data_dalam', then=1),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')
        nama=Gejala.objects.all()
        form = FormDataSuspek()

        for idx, record in enumerate(data):
            data_values = f'{record.data_luar},{record.data_dalam}'
            data_values=data_values.split(',')
            data_values = [float(value) for value in data_values  if value]

            for gejala, value in zip(nama_tabel, data_values ):
                data_dict[gejala.alias].append([idx, value])
          
        transformed_data_suspek = []
        for suspek in data:
            suspek.gejala = f'{suspek.data_luar},{suspek.data_dalam},{suspek.data_gejala},{suspek.data_khusus}' # type: ignore
            suspek.gejala = suspek.gejala.split(',') # type: ignore
            transformed_data_suspek.append(suspek)
            
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'data_luar':dict(data_dict),
            'menu': request.menu,
            'groups': request.groups,
            'nama_tabel':nama_tabel,
            'nama':nama,
            'form': form,
            'diagnosa': diagnosa,
        }
        return render(request, 'office/data_suspek/view_data_suspek.html', context)

@method_decorator(decorators, name='dispatch')
class UpdateDataSuspekView(View):
    def post(self, request, id):
        user = request.user
        try:
            data = DataSuspek.objects.get(id=id)
        except DataSuspek.DoesNotExist:
            return redirect('data_suspek:data_suspek')

        form = FormDataSuspek(request.POST, instance=data)
        if form.is_valid():
            # Mengambil tinggi dan berat badan dari form
            tb = form.cleaned_data.get('tb')  # Tinggi badan dalam cm
            bb = form.cleaned_data.get('bb')  # Berat badan dalam kg
            bb=50
            # Konversi tb dan bb dari string ke float
            try:
                tb = float(tb) / 100  # Konversi cm ke meter
                bb = float(bb)
            except (ValueError, TypeError):
                tb = 0
                bb = 0
            print(bb)
            # Hitung IMT jika tb dan bb lebih dari 0
            if tb > 0 and bb > 0:
                imt = round(bb / (tb ** 2), 1)
                form.instance.imt = 55  # Set nilai IMT pada objek data
                print(f"IMT yang dihitung dan akan disimpan: {imt}")  # Debugging untuk memastikan nilai IMT
            else:
                form.instance.imt = None

            # Penanganan Diagnosa
            diagnosa = form.cleaned_data.get('diagnosa')
            if diagnosa:
                try:
                    penanganan = Diagnosa.objects.get(id=diagnosa.id).penanganan
                    data.penanganan = 'coba penanganan'
                except Diagnosa.DoesNotExist:
                    data.penanganan = None
            else:
                data.penanganan = None

            # Set petugas_id jika belum ada atau berbeda
            if data.petugas_id is None or data.petugas_id != user.id:
                data.petugas_id = user.id

            # Simpan data menggunakan form save
            form.save()  # Ini akan memanggil form.save() yang sudah dimodifikasi di atas

            return redirect('data_suspek:view_suspek', nik=data.nik)

        # Jika form tidak valid, tampilkan ulang form dengan pesan kesalahan
        return render(request, 'office/data_suspek/edit_data_suspek.html', {'form': form})

@method_decorator(decorators, name='dispatch')
class DeleteDataSuspekView(View):
    def post(self, request, id):
        
        data_suspek = DataSuspek.objects.filter(id=id).only(
                'id', 'nik', 'nama', 'gender', 'alamat', 'umur', 'penanganan', 'diagnosa', 'petugas'
            ).select_related('gender', 'diagnosa', 'petugas')
        data_suspek.delete()
        return redirect('data_suspek:data_suspek')

class LaporanDataSuspekView(View):
    def get(self, request):
        # Filter pengumuman dengan jenis_id='1'
        pengumuman = Pengumuman.objects.all()
        # Mendapatkan tanggal pengumuman yang unik
        tanggal_pengumuman = pengumuman.values_list('tanggal', flat=True).distinct()

        # Debugging: cetak hasil tanggal_pengumuman di console
        print("Tanggal Pengumuman:", tanggal_pengumuman)

        # Filter data suspek sesuai tanggal pengumuman
        suspek = DataSuspek.objects.filter(tanggal__in=tanggal_pengumuman).order_by('-tanggal')

        context = {
            'pengumuman_list': tanggal_pengumuman,
            'suspek_list': suspek
        }

        return render(request, 'office/laporan/kegiatan/pengumuman_modal.html', context)

class CetakSuspekView(View):
    def get(self, request):
        tanggal_param = request.GET.get('tanggal', None)
        if not tanggal_param:
            return redirect('laporan_data_suspek')

        # Memisahkan tanggal menjadi list berdasarkan koma
        tanggal_list = [t.strip() for t in tanggal_param.split(',')]

        # Mendapatkan data gejala
        gejala_data = Gejala.objects.only('id', 'nama', 'alias', 'jenis').annotate(
            jenis_order=Case(
                When(jenis='data_gejala', then=0),
                When(jenis='data_khusus', then=1),
                When(jenis='data_luar', then=2),
                When(jenis='data_dalam', then=3),
                output_field=IntegerField(),
            )
        ).order_by('jenis_order')

        # Fungsi untuk mengganti nilai hasil
        def ganti_nilai(nilai):
            return "✔" if nilai == 1 else "-" if nilai == 2 else nilai

        # Fungsi aman untuk konversi nilai
        def aman_konversi(nilai):
            try:
                return ganti_nilai(int(float(nilai)))
            except ValueError:
                return 'N/A'

        # Menggunakan timestamp saat ini untuk nama file
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        buffer = BytesIO()
        filename = f'hasil_diagnosa_{timestamp}.pdf'
        
        # Fungsi untuk menggambar header di setiap halaman
        def gambar_header(p, about, tanggal):
            logo_path = finders.find('ico/sibindu-white.min.png')
            if logo_path:
                logo = ImageReader(logo_path)
                logo_width = 50
                logo_height = 50
                total_width = logo_width + 10 + p.stringWidth(about.nama, "Helvetica-Bold", 14)
                width, height = landscape(A4)
                center_x = (width - total_width) / 2

                # Menampilkan logo dan teks di tengah halaman
                logo_x = center_x
                logo_y = height - 60
                p.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)

                p.setFont("Helvetica-Bold", 14)
                text_x = logo_x + logo_width + 10
                text_y = logo_y + 20
                p.drawString(text_x, text_y, about.nama)

                # Tampilkan keterangan "Rekapitulasi Kegiatan POSBINDU"
                p.setFont("Helvetica", 12)
                text_y -= 15
                p.drawString(text_x, text_y, "Rekapitulasi Kegiatan POSBINDU")

                # Tampilkan tanggal pelaksanaan untuk halaman saat ini
                p.setFont("Helvetica", 10)
                p.drawString(20, height - 70, f'Tempat: Gogik')
                p.drawString(20, height - 90, f'Pelaksanaan: {tanggal}')

        # Siapkan buffer PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        # Gambar header untuk halaman pertama
        about = About.objects.get(id=1)
        y_start = height - 140
        data_tabel = [['No', 'NIK', 'Nama', 'JK', 'Diagnosa'] + [gejala_item.alias for gejala_item in gejala_data]]
        print("data tabel:",data_tabel)
        # Iterasi untuk setiap tanggal
        for tanggal in tanggal_list:
            suspek_list = DataSuspek.objects.filter(tanggal=tanggal).order_by('-tanggal')

            # Jika tidak ada data yang cocok, lewati tanggal ini
            if not suspek_list.exists():
                continue

            # Gambar header yang sesuai untuk halaman baru
            gambar_header(p, about, tanggal)

            # Tentukan max_rows_per_page berdasarkan jumlah data
            if len(suspek_list) > 25:
                max_rows_per_page = 25
            else:
                max_rows_per_page = len(suspek_list)

            for i, suspek in enumerate(suspek_list, start=1):
                data = f"{suspek.data_gejala},{suspek.data_khusus},{suspek.data_luar},{suspek.data_dalam}".split(',')
                items = [aman_konversi(data[j]) if j < len(data) else 'N/A' for j in range(len(data_tabel[0]) - 5)]
                row = [str(i), suspek.nik, suspek.nama, suspek.gender.alias, suspek.diagnosa.diagnosa] + items
                data_tabel.append(row)
             

                # Cek apakah perlu menambah halaman baru
                if len(data_tabel) > max_rows_per_page + 1:  # +1 untuk header
                    # Gambar tabel dan pindah halaman
                    table = Table(data_tabel)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8.6),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                        ('TOPPADDING', (0, 0), (-1, 0), 4),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ]))

                    table.wrapOn(p, width, height)
                    table.drawOn(p, 20, y_start - (len(data_tabel) - 1) * 17)

                    p.showPage()  # Pindah ke halaman berikutnya
                    # Gambar header untuk halaman baru
                    gambar_header(p, about, tanggal)
                    data_tabel = [['No', 'NIK', 'Nama', 'JK', 'Diagnosa'] + [gejala_item.alias for gejala_item in gejala_data]]

            # Gambar tabel untuk sisa data jika ada
            if len(data_tabel) > 1:  # Pastikan ada data untuk ditampilkan
                table = Table(data_tabel)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8.6),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                    ('TOPPADDING', (0, 0), (-1, 0), 4),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))

                table.wrapOn(p, width, height)
                table.drawOn(p, 20, y_start - (len(data_tabel) - 1) * 17)

                p.showPage()  # Tambahkan halaman baru jika ada data
                data_tabel = [['No', 'NIK', 'Nama', 'JK', 'Diagnosa'] + [gejala_item.alias for gejala_item in gejala_data]]

        p.save()

        buffer.seek(0)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
