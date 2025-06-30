from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....models.data_suspek.m_data_suspek import DataSuspek ,Diagnosa
from ....models.data_suspek.m_diagnosis import MenuDiagnosis
from .....expert.models.m_kepakaran import Gejala
from .....models import Menu
from ....forms.data_suspek.f_data_suspek import  FormPengecekanLuar
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from ....models.informasi.m_pengumuman import Pengumuman
from django.db.models import Max,Min
@method_decorator(login_required, name='dispatch')

class PengecekanLuar(View):
    
    def get(self, request):
        ini_tanggal = Pengumuman.objects.filter(jenis=1).filter()
        ini_tanggal = ini_tanggal.aggregate(Min('tanggal'))['tanggal__min']
        #min_id_per_nik = DataSuspek.objects.values('nik').annotate(min_id=Min('id')).values('min_id')
        data = DataSuspek.objects.filter(tanggal=ini_tanggal).only(
            'id', 'nik', 'nama','data_luar'
        ).order_by('-id')
        nama_tabel= Gejala.objects.filter(jenis='data_luar').only('id','nama', 'alias')
        
        form = FormPengecekanLuar()
        for i in data: 
            if i.data_luar  is not None:
                i.data_luar = i.data_luar.split(",")
            else:
                i.data_luar = []
        context = {
            'data': data,
            'nama_tabel':nama_tabel,
            'form': form
  
        }
        return render(request, 'expert/diagnosis/pengecekan_luar/pengecekan_luar.html', context)
class UpdatePengecekanLuar(View):
    def post(self, request, id):
        data = get_object_or_404(DataSuspek.objects.only(
            'id','data_luar'
        ), id=id)
        form = FormPengecekanLuar(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('diagnosis:pengecekan_luar:pengecekan_luar')
        else:
            return render(request, 'expert/diagnosis/pengecekan_luar/edit_pengecekan_luar.html', {'form': form})

       
