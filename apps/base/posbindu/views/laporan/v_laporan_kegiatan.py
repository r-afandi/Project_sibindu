from io import BytesIO
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ...models.laporan.m_laporan_kegiatan import LaporanKegiatan
from ...forms.laporan.f_laporan_kegiatan import FormLapKegiatan
from django.contrib.auth.models import User,Group
from ....decorator import auth_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django_drf_filepond.api import store_upload,get_stored_upload,get_stored_upload_file_data,delete_stored_upload

from django_drf_filepond.models import TemporaryUpload, StoredUpload
from django.contrib.auth.models import User
from datetime import datetime
from django.http import JsonResponse
from django.dispatch import receiver
from ....views import add_notify
from ....models import Notifikasi
decorators = [
    add_notify(feature='kegiatan', view_name='kegiatan:kegiatan', model=LaporanKegiatan, name_field='nama'), 
    auth_required(required_permissions=['view_kegiatan', 'add_kegiatan', 'change_kegiatan', 'delete_kegiatan'], model_class=LaporanKegiatan), 
    login_required
]
@method_decorator(decorators, name='dispatch')
class KegiatanListView(View):
    def get(self, request):

        group_id = [group.id for group in request.groups]
        data = LaporanKegiatan.objects.all()

        form = FormLapKegiatan(request=request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=request.user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
            'group_id': group_id
        }

        return render(request, 'office/laporan/kegiatan/data_kegiatan.html', context)

    def post(self, request):
        form = FormLapKegiatan(request.POST, request.FILES, request=request)
        if form.is_valid(): 
            upload_id = request.POST['filepond']
            temp = TemporaryUpload.objects.get(upload_id=upload_id)
            filename = temp.upload_name
            form.instance.upload = temp.upload_id
            date = datetime.now().strftime('%Y-%m-%d')
            store_upload(upload_id=temp.upload_id, destination_file_path='kegiatan/' + date + '_' + filename) 
            form.instance.foto = 'kegiatan/' + date + '_' + filename
            form.save()
            return redirect('kegiatan:kegiatan')
        else:
            # Handle form validation errors here
            context = {
                'form': form,
            }
        return render(request, 'office/laporan/kegiatan/add_kegiatan.html', context)

@method_decorator(decorators, name='dispatch')
class UpdateKegiatanView(View):
    def post(self, request, id):
        user = request.user
        kegiatan = get_object_or_404(LaporanKegiatan, id=id)
        form = FormLapKegiatan(request.POST, instance=kegiatan, request=request)
        data = StoredUpload.objects.get(upload_id=kegiatan.upload)
        temp = TemporaryUpload.objects.filter(uploaded_by=user.id).order_by('-uploaded').first()

        if temp is not None:
                # Hapus file lama jika ada file baru diunggah
                if kegiatan.foto:  # Periksa apakah ada file foto yang tersimpan sebelumnya
                    kegiatan.foto.delete(save=False)  # Hapus file dari storage
                    delete_stored_upload(upload_id=data.upload_id, delete_file=True)  # Hapus metadata di StoredUpload
                    form.instance.foto = None  # Set foto menjadi None

                # Upload file baru dari temp
                filename = temp.upload_name  # Ambil nama file baru
                form.instance.upload = temp.upload_id  # Set temp.upload_id sebagai upload baru
                date = datetime.now().strftime('%Y-%m-%d')  # Format tanggal untuk penamaan file
                destination_file_path = 'kegiatan/' + date + '_' + filename  # Tentukan path penyimpanan baru
                store_upload(upload_id=temp.upload_id, destination_file_path=destination_file_path)  # Simpan file ke destination
                form.instance.foto = destination_file_path  # Set path baru ke instance form

            # Jika tidak ada file baru diunggah (temp kosong), jangan hapus file yang ada
        else:
            form.instance.foto = kegiatan.foto  # Pertahankan foto yang ada
        form.save()
        return redirect('kegiatan:kegiatan')


@method_decorator(decorators, name='post')
class DeleteKegiatanView(View):
    def post(self, request, id):
        kegiatan = get_object_or_404(LaporanKegiatan, id=id)
        data = StoredUpload.objects.get(upload_id=kegiatan.upload)
        delete_stored_upload(upload_id=data.upload_id, delete_file=True)
        if kegiatan.foto:
            kegiatan.foto.delete(save=False) 
        kegiatan.delete()
        return redirect("kegiatan:kegiatan")

