from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ...models.data_suspek.m_data_suspek import DataSuspek ,Diagnosa
from ...models.data_suspek.m_diagnosis import MenuDiagnosis
from ...models.informasi.m_pengumuman import Pengumuman
from ....decorator import auth_required
from ....expert.models.m_kepakaran import Gejala
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User,Group
from ....views import add_notify
from ....models import Notifikasi

@method_decorator([login_required,auth_required(required_permissions=['view_data_suspek', 'add_data_suspek', 'change_data_suspek', 'delete_data_suspek'], model_class=DataSuspek), add_notify(feature='Diagnosis')], name='dispatch')
class DiagnosisView(View):
    def get(self, request):
        user=request.user
        data = DataSuspek.objects.all()
        diagnosis= MenuDiagnosis.objects.all()    
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()
        tanggal=Pengumuman.objects.filter(jenis=1).values('tanggal')
        print('tanggal',tanggal)
       
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'tanggal': tanggal,
            'data': data,
            'diagnosis': diagnosis,
            'menu': request.menu,
            'groups': request.groups,
           
        }
        return render(request, 'expert/diagnosis/diagnosis.html', context )