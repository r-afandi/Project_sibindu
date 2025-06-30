from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....models.data_suspek.m_data_suspek import DataSuspek ,Diagnosa
from ....models.data_suspek.m_diagnosis import MenuDiagnosis
from .....expert.models.m_kepakaran import Gejala
from .....models import Menu
from ....forms.data_suspek.f_data_suspek import FormPengecekanDalam
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import Max,Min
from ....models.informasi.m_pengumuman import Pengumuman
@method_decorator(login_required, name='dispatch')

class PengecekanDalam(View):
    def get(self, request):
        ini_tanggal = Pengumuman.objects.filter(jenis=1).filter()
        ini_tanggal = ini_tanggal.aggregate(Min('tanggal'))['tanggal__min']
        data = DataSuspek.objects.filter(tanggal=ini_tanggal).only(
            'id', 'nik', 'nama','data_dalam'
        ).order_by('-id')
        nama_tabel= Gejala.objects.filter(jenis='data_dalam').only('id','nama', 'alias')
        form =  FormPengecekanDalam()
        # loop data data_dalam
        for i in data:
            if i.data_dalam  is not None:
                i.data_dalam = i.data_dalam.split(",")
            else:
                i.data_dalam = []
        context = {
            'data': data,
            'nama_tabel':nama_tabel,
            'form': form,
        }
        return render(request, 'expert/diagnosis/pengecekan_dalam/pengecekan_dalam.html', context)

class UpdatePengecekanDalam(View):
    def post(self, request, id):
        data = get_object_or_404(DataSuspek.objects.only(
        'id','data_dalam'
        ), id=id)
        form = FormPengecekanDalam(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('diagnosis:pengecekan_dalam:pengecekan_dalam')
        else:
      
            return render(request, 'expert/diagnosis/pengecekan_dalam/edit_pengecekan_dalam.html', {'form': form})
