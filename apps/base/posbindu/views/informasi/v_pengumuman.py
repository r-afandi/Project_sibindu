from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ...models.informasi.m_pengumuman import Pengumuman
from ....decorator import auth_required
from ...forms.informasi.f_pengumuman import FormPengumuman
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
#notifikasi
from ....views import add_notify
from ....models import Notifikasi
from django.http import JsonResponse
decorators = [login_required,auth_required(required_permissions=['view_pengumuman', 'add_pengumuman', 'change_pengumuman', 'delete_pengumuman'], model_class=Pengumuman), add_notify(feature='pengumuman', view_name='pengumuman:pengumuman',model=Pengumuman, name_field='judul')]
@method_decorator(decorators, name='dispatch')
class PengumumanDetailView(View):
    def get(self, request, id):
        pengumuman = get_object_or_404(Pengumuman, id=id)
        data = {
            'judul': pengumuman.judul,
            'pengumuman': pengumuman.pengumuman,
            'tanggal': pengumuman.tanggal,
            'waktu': pengumuman.waktu,
            'tempat': pengumuman.tempat
        }
        return JsonResponse(data)
@method_decorator(decorators, name='dispatch')
class PengumumanListView(View):
    def get(self, request):
        user=request.user
        data = Pengumuman.objects.all()
        form = FormPengumuman()
        notifications = Notifikasi.objects.filter(is_read=False).order_by('-created_at')
        jumlah=notifications.count()
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
            'group_permissions': request.group_permissions,
        }

        return render(request, 'office/informasi/pengumuman/data_pengumuman.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = FormPengumuman(request.POST)
            if form.is_valid():
                form.save()
                return redirect("pengumuman:pengumuman") 
            else:
                # Handle form validation errors here
                context = {
                    'form': form,
                }           

            return render(request, 'office/informasi/pengumuman/add_pengumuman.html',context)

@method_decorator(decorators, name='dispatch')
class UpdatePengumumanView(View):
    def get(self, request, id):
        pengumuman = get_object_or_404(Pengumuman, id=id)
        form = FormPengumuman(instance=pengumuman)
        notifications = Notifikasi.objects.filter(is_read=False).order_by('-created_at')
        print('check:',notifications)
        context = {
            'notifications': notifications,
            'form': form,
        }

        return render(request, 'office/informasi/pengumuman/edit_pengumuman.html',context)
    def post(self, request, id):
        pengumuman = get_object_or_404(Pengumuman, id=id)
        form = FormPengumuman(request.POST, instance=pengumuman)
        if form.is_valid():
            form.save()
            return redirect("pengumuman:pengumuman")
        return render(request, 'office/informasi/pengumuman/edit_pengumuman.html', {'form': form})

@method_decorator(decorators, name='dispatch')
class DeletePengumumanView(View):
    def post(self, request, id):
        pengumuman = get_object_or_404(Pengumuman, id=id)
        pengumuman.delete()
        return redirect("pengumuman:pengumuman")