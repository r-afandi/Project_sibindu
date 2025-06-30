
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

#from distutils.command.upload import upload
from ...models.informasi.m_artikel import Artikel
from ....decorator import auth_required
from ...forms.informasi.f_artikel import FormArtikel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django_drf_filepond.api import store_upload,delete_stored_upload
from django_drf_filepond.models import TemporaryUpload, StoredUpload
from django.contrib.auth.models import User
from datetime import datetime
from ....views import add_notify
from ....models import Notifikasi
import logging

# Setup logging
logger = logging.getLogger(__name__)
decorators = [login_required,auth_required(required_permissions=['view_artikel', 'add_artikel', 'change_artikel', 'delete_artikel'], model_class=Artikel), add_notify(feature='artikel', view_name='artikel:artikel',model=Artikel, name_field='judul')]

@method_decorator(decorators, name='dispatch')
class ArtikelListView(View):
    def get(self, request):
        group_id = [group.id for group in request.groups]
        data = Artikel.objects.all()
        form=FormArtikel(request=request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=request.user).order_by('-created_at')
        jumlah = notifications.count()
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
            'group_id':group_id

        }

        return render(request, 'office/informasi/artikel/data_artikel.html', context)
        
@method_decorator(decorators, name='dispatch')
class AddArtikelView(View):
    def get(self, request):
        form = FormArtikel( request=request)
        group_id = [group.id for group in request.groups]
        context = {
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
            'group_id':group_id
        }

        return render(request, 'office/informasi/artikel/add_artikel.html', context)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            form = FormArtikel(request.POST, request.FILES,request=request)
            if form.is_valid():
                date = datetime.now().strftime('%Y-%m-%d')
                upload_id = request.POST.get('filepond')

                if upload_id:
                    try:
                        temp = TemporaryUpload.objects.filter(upload_id=upload_id).order_by('-uploaded').first()
                    except TemporaryUpload.DoesNotExist:
                        raise ValueError("File tidak ditemukan")

                    # Jika ada file baru, proses upload
                    filename = temp.upload_name
                    form.instance.upload = temp.upload_id
                    destination_file_path =f'artikel/{date}_{filename}'
                    store_upload(upload_id=temp.upload_id, destination_file_path=destination_file_path)
                    form.instance.gambar = destination_file_path  # Simpan path file ke form
                else:
                    # Jika tidak ada file baru, pertahankan file gambar yang lama (jika ada)
                    form.instance.gambar = form.instance.gambar or None
            form.save()
            return redirect('artikel:artikel')
        else:
            context = {
                    'form': form,
                }
            return render(request, 'office/informasi/artikel/add_artikel.html', context)

@method_decorator(decorators, name='dispatch')
class ValidasiArtikelView(View):
    def get(self, request, id):
        artikel = get_object_or_404(Artikel, id=id)
        form = FormArtikel(instance=artikel, request=request)

        context={
            'form': form,
            'artikel': artikel,
        }

        return render(request, 'office/informasi/artikel/validasi_artikel.html', context)
@method_decorator(decorators, name='dispatch')
class DetailArtikelView(View):
    def get(self, request, id):
        artikel = get_object_or_404(Artikel, id=id)
        group_id = [group.id for group in request.groups]
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=request.user).order_by('-created_at')
        jumlah = notifications.count()
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'artikel': artikel,
            'menu': request.menu,
            'groups': request.groups,
            'group_id':group_id

        }

        return render(request, 'office/informasi/artikel/detail_artikel.html', context)
@method_decorator(decorators, name='dispatch')
class UpdateArtikelView(View):
    def get(self, request, id):
        group_id = [group.id for group in request.groups]
        artikel = get_object_or_404(Artikel, id=id)
        form = FormArtikel(instance=artikel, request=request)
        
        # Debugging log
        logger.debug(f"GET request for artikel ID: {id}")
        logger.debug(f"Group IDs: {group_id}")
        
        context = {
            'form': form,
            'artikel': artikel,
            'menu': request.menu,
            'groups': request.groups,
            'group_id': group_id
        } 

        return render(request, 'office/informasi/artikel/edit_artikel.html', context)

    def post(self, request, id):
        user = request.user
        artikel = get_object_or_404(Artikel, id=id)
        form = FormArtikel(request.POST, request.FILES, instance=artikel, request=request)
        temp = TemporaryUpload.objects.filter(uploaded_by=user.id).order_by('-uploaded').first()

        # Debugging log
        logger.debug(f"POST request for artikel ID: {id}")
        logger.debug(f"Form data: {request.POST}")
        logger.debug(f"Temporary upload: {temp}")

        try:
            data = StoredUpload.objects.get(upload_id=artikel.upload)
        except StoredUpload.DoesNotExist:
            data = None
            logger.warning(f"No stored upload found for artikel ID: {id}")

        if form.is_valid():
            date = datetime.now().strftime('%Y-%m-%d')
            upload_id = request.POST.get('filepond')
            
            logger.debug(f"Form is valid. Upload ID: {upload_id}")

            if upload_id:
                if temp is not None:
                    if data is not None:
                        delete_stored_upload(upload_id=data.upload_id, delete_file=True)
                # Jika ada file baru, proses upload
                filename = temp.upload_name
                form.instance.upload = temp.upload_id
                destination_file_path = f'artikel/{date}_{filename}'
                store_upload(upload_id=temp.upload_id, destination_file_path=destination_file_path)
                form.instance.gambar = destination_file_path  # Simpan path file ke form
            else:
                # Jika tidak ada file baru, pertahankan file gambar yang lama (jika ada)
                form.instance.gambar = form.instance.gambar or None

            form.save()
            logger.info(f"Artikel ID: {id} updated successfully.")
            return redirect('artikel:artikel')
        else:
            logger.error(f"Form errors: {form.errors}")
            context = {
                'form': form,
            }
            return render(request, 'office/informasi/artikel/edit_artikel.html', context)

@method_decorator(decorators, name='dispatch')
class DeleteArtikelView(View):

    def post(self, request, id):
        artikel = get_object_or_404(Artikel, id=id)
        data=StoredUpload.objects.get(upload_id=artikel.upload)
        delete_stored_upload(upload_id=data.upload_id, delete_file=True)
        if artikel.gambar:
            artikel.gambar.delete(save=False) 
        artikel.delete()
        return redirect("artikel:artikel")

    

# jangan menggunakan first, lebih baik masukan user_id di setiap tabel yang memerlukan upload file/img

