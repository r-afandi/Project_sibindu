from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....models.data_suspek.m_data_suspek import DataSuspek
from ....models.data_suspek.m_diagnosis import MenuDiagnosis
from .....expert.models.m_kepakaran import Gejala
from ....forms.data_suspek.f_data_suspek import  FormPelacakanGejala
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Case, When, IntegerField
from django.db.models import Max,Min
from ....models.informasi.m_pengumuman import Pengumuman
@method_decorator(login_required, name='dispatch')
class PelacakanGejala(View):
    def get(self, request):
        ini_tanggal = Pengumuman.objects.filter(jenis=1).filter()
        ini_tanggal = ini_tanggal.aggregate(Min('tanggal'))['tanggal__min']
                # Annotate each record with the minimum id for each nik
        #min_id_per_nik = DataSuspek.objects.values('nik').annotate(min_id=Min('id')).values('min_id')

        # Filter data based on the minimum id per nik
        data = DataSuspek.objects.filter(tanggal=ini_tanggal).only(
            'id', 'nik', 'nama','data_gejala','data_khusus'
        ).order_by('-id')
        # Convert the queryset to a list before caching
       
        nama_tabel= Gejala.objects.filter(jenis__in=['data_gejala','data_khusus']).only('id','nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')
        diagnosis= MenuDiagnosis.objects.all()
        form =  FormPelacakanGejala()
        
        # loop data data_gejala
        transformed_data_suspek = []

        for suspek in data:
            suspek.gejala = f'{suspek.data_gejala},{suspek.data_khusus}'
            suspek.gejala = suspek.gejala.split(',')
            transformed_data_suspek.append(suspek)

        context = {
            'data': data,
            'nama_tabel':nama_tabel,
            'diagnosis': diagnosis,
            'form': form,
        }
        return render(request, 'expert/diagnosis/pelacakan_gejala/pelacakan_gejala.html', context)

class UpdatePelacakanGejala(View):
    def post(self, request, id):
        data_suspek = get_object_or_404(DataSuspek, id=id)
        form = FormPelacakanGejala(request.POST, instance=data_suspek)
        
        if form.is_valid():
            form.save()
            return redirect('diagnosis:pelacakan_gejala:pelacakan_gejala')
        
        context = {
            'form': form
        }
        return render(request, 'expert/diagnosis/pelacakan_gejala/edit_pelacakan_gejala.html', context)

       
