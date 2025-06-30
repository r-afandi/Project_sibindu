from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....models.data_suspek.m_data_suspek import DataSuspek
from ....models.informasi.m_pengumuman import Pengumuman
from ....models.data_suspek.m_diagnosis import MenuDiagnosis
from .....models import Menu
from datetime import datetime
from ....forms.data_suspek.f_data_suspek import FormRegistrasi
from .....expert.models.m_kepakaran import Gejala
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Min,Max
from django.http import JsonResponse

def search_nik(request):
    nik = request.GET.get('nik', None)
    if nik:
        try:
            suspek = DataSuspek.objects.filter(nik=nik).first()
            data = {
                'success': True,
                'nama': suspek.nama,
                'umur': suspek.umur,
                'alamat': suspek.alamat,
                'gender': suspek.gender.id if suspek.gender else None
            }
        except DataSuspek.DoesNotExist:
            print("DataSuspek.DoesNotExist")  # Debug print statement
            data = {
                'success': False,
                'message': 'Data belum terdaftar'
            }
        except Exception as e:
            print(f"Error: {e}")  # Debug print statement
            data = {
                'success': False,
                'message': str(e)
            }
    else:
        print("NIK not provided")  # Debug print statement
        data = {
            'success': False,
            'message': 'NIK tidak diberikan'
        }
    return JsonResponse(data)
@method_decorator(login_required, name='dispatch')
class Registrasi(View):
    def get(self, request):
        # Annotate each record with the minimum id for each nik   
        ini_tanggal = Pengumuman.objects.filter(jenis=1).filter()
        ini_tanggal = ini_tanggal.aggregate(Min('tanggal'))['tanggal__min']
    
        # Filter data based on the minimum id per nik
        data = DataSuspek.objects.filter(tanggal=ini_tanggal).only(
            'id', 'nik', 'nama', 'gender', 'alamat', 'umur'
        ).select_related('gender').order_by('-id')

        form = FormRegistrasi()
        dummy = Gejala.objects.only('id','nama', 'alias', 'jenis')

        context = {
            'data': data,
            'form': form,
            'dummy': dummy,
        }
        return render(request, 'expert/diagnosis/registrasi/registrasi.html', context)

    def post(self, request):
        form = FormRegistrasi(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diagnosis:registrasi:registrasi')
        else:
            print(form.errors)
        return render(request, 'expert/diagnosis/registrasi/add_registrasi.html', {'form': form})

class UpdateRegistrasi(View):
    def post(self, request, id):      
        data = get_object_or_404(DataSuspek.objects.only(
            'id', 'nik', 'nama','gender', 'alamat', 'umur','tanggal','data_gejala','data_khusus'
        ).prefetch_related('gender'), id=id)
        form = FormRegistrasi(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('diagnosis:registrasi:registrasi')
        return render(request, 'expert/diagnosis/registrasi/edit_registrasi.html', {'form': form})


class DeleteRegistrasi(View):
    def post(self, request, id):
        # Ambil data berdasarkan ID, jika tidak ditemukan akan menampilkan 404
        data = get_object_or_404(DataSuspek, id=id)
        
        # Hapus data
        data.delete()
        
        # Redirect ke halaman registrasi setelah data dihapus
        return redirect("diagnosis:registrasi:registrasi")
