from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....models.data_suspek.m_data_suspek import DataSuspek ,Diagnosa
from ....models.data_suspek.m_diagnosis import MenuDiagnosis
from .....expert.models.m_kepakaran import Gejala,Pakar,Diagnosa

from ....forms.data_suspek.f_data_suspek import FormPenanganan
from .....models import Menu
from core.expert.f_chaining.fc import Diagnosis
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import pandas as np
import joblib
from ..p_suspek import generate_receipt
from django.core.cache import cache
from django.db.models import Case, When, IntegerField
from django.db.models import Max,Min
from ....models.informasi.m_pengumuman import Pengumuman
@method_decorator(login_required, name='dispatch')
class Penanganan(View):
    
    def get(self, request):
        ini_tanggal = Pengumuman.objects.filter(jenis=1).filter()
        ini_tanggal = ini_tanggal.aggregate(Min('tanggal'))['tanggal__min']
        # Annotate each record with the minimum id for each nik
        #min_id_per_nik = DataSuspek.objects.values('nik').annotate(min_id=Min('id')).values('min_id')

        # Filter data based on the minimum id per nik
        data = DataSuspek.objects.filter(tanggal=ini_tanggal).only(
            'id', 'nik', 'nama', 'gender', 'alamat', 'diagnosa','penanganan','petugas'
        ).select_related('gender','diagnosa','petugas').order_by('-id')
        nama_tabel=  Gejala.objects.all().only('id','nama', 'alias')
        form=FormPenanganan()

        context = {
            'data': data,
            'nama_tabel':nama_tabel,
            'form':form,
        }
        return render(request, 'expert/diagnosis/penanganan/penanganan.html', context)

class EditPenanganan(View):
    def get(self, request, id):
        user=request.user
        data = get_object_or_404(DataSuspek.objects.only(
        'id', 'nik', 'nama', 'data_gejala', 'data_khusus', 'data_luar', 'data_dalam', 'diagnosa', 'penanganan', 'petugas'
        ).select_related('diagnosa', 'petugas'), id=id)
        form = FormPenanganan(instance=data)
        nama_tabel = Gejala.objects.only('id', 'nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')
        data_gejala = [int(x) for x in data.data_gejala.split(',') if x]
        data_khusus = [int(x) for x in data.data_khusus.split(',') if x]
        data_luar = [float(x) for x in data.data_luar.split(',') if x]
        data_dalam = [float(x) for x in data.data_dalam.split(',') if x]
        combined_results = Diagnosis.diagnose(data_gejala, data_khusus, data_luar, data_dalam)

        print('Data gejala:', data.data_gejala)
        print('Data khusus:', data.data_khusus)
        print('Data luar:', data.data_luar)
        print('Data dalam:', data.data_dalam)
    # Kirim hasil ke template


        context = {
            'data': data,
            'nama_tabel': nama_tabel,
            'form': form,
            'user':user,
            'combined_results': combined_results
            }
        return render(request, 'expert/diagnosis/penanganan/edit_penanganan.html', context)

class UpdatePenanganan(View):
    def post(self, request, id):
        # Mendapatkan pengguna yang sedang login
        user = request.user
        
        # Mengambil data dari DataSuspek berdasarkan ID yang diberikan
        data = get_object_or_404(DataSuspek.objects.only(
            'id', 'nik', 'nama', 'data_gejala', 'data_khusus', 'data_luar', 'data_dalam', 'diagnosa', 'penanganan', 'petugas'
        ).select_related('diagnosa', 'petugas'), id=id)  # Mengambil data terkait dengan diagnosis dan petugas
        
        # Membuat instance form dengan data yang diambil
        form = FormPenanganan(request.POST, instance=data) 
        
        # Mengubah data gejala, khusus, luar, dan dalam menjadi list numerik
        data_gejala = [int(x) for x in data.data_gejala.split(',') if x]
        data_khusus = [int(x) for x in data.data_khusus.split(',') if x]
        data_luar = [float(x) for x in data.data_luar.split(',') if x]
        data_dalam = [float(x) for x in data.data_dalam.split(',') if x]
        
        # Menerapkan kode dari class diagnose untuk mendapatkan hasil diagnosis
        combined_results = Diagnosis.diagnose(data_gejala, data_khusus, data_luar, data_dalam)

        # Memeriksa apakah form valid
        if form.is_valid():
            # Inisialisasi variabel untuk menyimpan diagnosis yang valid
            valid_diagnosis = False
            final_diagnosis = None
            final_penanganan = None
            
            # Variabel untuk menyimpan diagnosis terbaik berdasarkan status
            best_diagnosis = None
            
            # Iterasi melalui hasil gabungan untuk menemukan diagnosis terbaik
            for result in combined_results:
                # Mengonversi status menjadi integer untuk perbandingan
                status_value = int(result['status'])  # Mengonversi status ke integer
                # Memeriksa apakah ini adalah diagnosis terbaik yang ditemukan
                if best_diagnosis is None or status_value < int(best_diagnosis['status']):
                    best_diagnosis = result  # Menyimpan diagnosis terbaik
            
            # Debugging: Mencetak status dari hasil terakhir dan diagnosis terbaik
            print(result['status'])
            print(best_diagnosis['status'])
            
            # Jika diagnosis yang valid ditemukan
            if best_diagnosis:
                final_diagnosis = best_diagnosis['id']  # Menyimpan ID diagnosis terbaik
                final_penanganan = best_diagnosis['penanganan']  # Menyimpan penanganan terbaik
                valid_diagnosis = True  # Menandai bahwa diagnosis valid ditemukan

            # Jika diagnosis valid ditemukan, simpan data
            if valid_diagnosis:
                data.diagnosa_id = final_diagnosis  # Menyimpan ID diagnosis ke objek data
                data.penanganan = final_penanganan  # Menyimpan penanganan ke objek data
                data.petugas_id = user.id  # Menyimpan ID petugas yang melakukan diagnosis
                form.save()  # Menyimpan perubahan ke database
                return redirect('diagnosis:penanganan:edit_penanganan', id=id)  # Mengalihkan ke halaman edit penanganan
            else:
                # Jika tidak ada diagnosis yang valid, tambahkan error ke form
                form.add_error(None, 'Diagnosis tidak valid.')
                print("Diagnosis tidak valid.")
                return render(request, 'expert/diagnosis/penanganan/edit_penanganan.html', {'form': form, 'data': data})
        else:
            # Jika form tidak valid, cetak error dan kembalikan ke halaman edit
            print("Form errors:", form.errors)
            return render(request, 'expert/diagnosis/penanganan/edit_penanganan.html', {'form': form, 'data': data})

class PrintPenanganan(View):
    def get(self, request, id):
        try:
            data_suspek = get_object_or_404(DataSuspek.objects.only('id', 'nik', 'nama','tanggal', 'data_gejala', 'data_khusus', 'data_luar', 'data_dalam', 'diagnosa', 'penanganan', 'petugas'), id=id)
            gejala_data = Gejala.objects.only('id','nama', 'alias', 'jenis').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')

            def ganti_nilai(nilai):
                return "Ya" if nilai == 1 else "Tidak" if nilai == 2 else nilai

            # Mengumpulkan gejala dari masing-masing kategori data
            d_gejala = [ganti_nilai(val) for val in data_suspek.data_gejala]
            d_khusus = [ganti_nilai(val) for val in data_suspek.data_khusus]
            d_luar = [ganti_nilai(val) for val in data_suspek.data_luar]
            d_dalam = [ganti_nilai(val) for val in data_suspek.data_dalam]

            # Gabungkan semua data dalam satu array untuk dicetak
            hasil= d_gejala + d_khusus + d_luar + d_dalam
            
            gejala = []
            for data_gejala in gejala_data:
                gejala.append(data_gejala.nama)

            # Menyusun item untuk dicetak
            items = []
            for i in range(len(gejala)):
                items.append({
                    "gejala": gejala[i],
                    "hasil": hasil[i],
                })

            # Generate receipt and redirect
            print_hasil = generate_receipt(data_suspek.id, data_suspek.nik, data_suspek.nama, data_suspek.alamat, items, data_suspek.diagnosa_id, data_suspek.penanganan, data_suspek.petugas_id, data_suspek.tanggal)
        
            return print_hasil
        except Exception as e:
            error_handle = f"data belum sempurna silahkan restart page. Error: {e}"
            return render(request, 'error_template.html', {'error': error_handle})

