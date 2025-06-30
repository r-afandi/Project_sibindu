from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ...models.m_kepakaran import Gejala,Diagnosa,Pakar,Kepakaran
from ....decorator import auth_required
from ...forms.data_diagnosa.f_data_diagnosa import FormGejala
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ....views import add_notify
from ....models import Notifikasi
import logging

# Konfigurasi logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG) 
decorators = [login_required, auth_required(required_permissions=['view_gejala', 'add_gejala', 'change_gejala', 'delete_gejala'], model_class=Gejala), add_notify(feature='data gejala', view_name='diagnosa:gejala', model=Gejala, name_field='alias')]

@method_decorator(decorators, name='dispatch')
class GejalaListView(View):
    def get(self, request):
        user = request.user
        data = Gejala.objects.all()
        form = FormGejala()
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'menu': getattr(request, 'menu', None),
            'groups': getattr(request, 'groups', None),
        }

        return render(request, 'expert/data_gejala/data_gejala.html', context)

    def post(self, request):
        logger.debug("Masuk ke fungsi POST GejalaListView")
        form = FormGejala()
        if request.method == 'POST':
            form = FormGejala(request.POST)
            if form.is_valid():
                gejala_baru = form.save()
                logger.debug(f"Gejala baru berhasil ditambahkan: {gejala_baru}")

                # Menambahkan nilai default ke setiap Diagnosa
                jenis_gejala = gejala_baru.jenis
                default_value_list = '2'
                default_value = '0'
                diagnosa_list = Diagnosa.objects.all()
                pakar_list = Kepakaran.objects.all()
                logger.debug(f"Menambahkan nilai default untuk gejala jenis: {jenis_gejala}")

                for diagnosa in diagnosa_list:
                    logger.debug(f"Proses menambahkan nilai default pada Diagnosa ID: {diagnosa.id}")
                    if jenis_gejala == 'data_gejala':
                        data_list = diagnosa.data_gejala.split(',')
                        data_list.append(default_value_list)
                        diagnosa.data_gejala = ','.join(data_list)
                    elif jenis_gejala == 'data_khusus':
                        data_list = diagnosa.data_khusus.split(',')
                        data_list.append(default_value_list)
                        diagnosa.data_khusus = ','.join(data_list)
                    elif jenis_gejala == 'data_luar':
                        data_list = diagnosa.data_luar.split(',')
                        data_list.append(default_value)
                        diagnosa.data_luar = ','.join(data_list)
                    elif jenis_gejala == 'data_dalam':
                        data_list = diagnosa.data_dalam.split(',')
                        data_list.append(default_value)
                        diagnosa.data_dalam = ','.join(data_list)

                    # Simpan perubahan
                    diagnosa.save()
                    logger.debug(f"Diagnosa ID {diagnosa.id} berhasil diperbarui dengan data baru")
                
                for pakar in pakar_list:
                    logger.debug(f"Proses menambahkan nilai default pada Kepakaran ID: {pakar.id}")
                    if jenis_gejala == 'data_gejala':
                        list = pakar.data_gejala.split(',')
                        list.append(default_value_list)
                        pakar.data_gejala = ','.join(list)
                    elif jenis_gejala == 'data_khusus':
                        list = pakar.data_khusus.split(',')
                        list.append(default_value_list)
                        pakar.data_khusus = ','.join(list)

                    # Simpan perubahan
                    pakar.save()
                return redirect("diagnosa:gejala")

        logger.debug("Form tidak valid atau tidak ada data POST")
        return render(request, 'expert/data_gejala/add_gejala.html')
@method_decorator(decorators, name='dispatch')
class UpdateGejalaView(View):
    def post(self, request, id):
        gejala = get_object_or_404(Gejala, id=id)
        form = FormGejala(request.POST, instance=gejala)
        if form.is_valid():
            form.save()
            return redirect("diagnosa:gejala")
        return render(request, 'expert/data_gejala/edit_gejala.html')

@method_decorator(decorators, name='dispatch')
class DeleteGejalaView(View):
    def post(self, request, id):
        logger.debug(f"Masuk ke fungsi POST DeleteGejalaView untuk Gejala ID: {id}")
        gejala = get_object_or_404(Gejala, id=id)
        jenis_gejala = gejala.jenis
        logger.debug(f"Gejala yang akan dihapus: {gejala} dengan jenis: {jenis_gejala}")

        # Menentukan indeks gejala yang dihapus berdasarkan posisinya di dalam queryset
        all_gejala = list(Gejala.objects.filter(jenis=jenis_gejala).order_by('id'))
        index_to_remove = all_gejala.index(gejala)
        logger.debug(f"Indeks gejala yang akan dihapus: {index_to_remove}")

        # Menghapus elemen array dari setiap Diagnosa berdasarkan jenis data
        diagnosa_list = Diagnosa.objects.all()
        pakar_list = Kepakaran.objects.all()
        for diagnosa in diagnosa_list:
            logger.debug(f"Proses menghapus nilai pada Diagnosa ID: {diagnosa.id}")
            if jenis_gejala == 'data_gejala':
                data_list = diagnosa.data_gejala.split(',')
                if 0 <= index_to_remove < len(data_list):
                    del data_list[index_to_remove]
                    diagnosa.data_gejala = ','.join(data_list)
            elif jenis_gejala == 'data_khusus':
                data_list = diagnosa.data_khusus.split(',')
                if 0 <= index_to_remove < len(data_list):
                    del data_list[index_to_remove]
                    diagnosa.data_khusus = ','.join(data_list)
            elif jenis_gejala == 'data_luar':
                data_list = diagnosa.data_luar.split(',')
                if 0 <= index_to_remove < len(data_list):
                    del data_list[index_to_remove]
                    diagnosa.data_luar = ','.join(data_list)
            elif jenis_gejala == 'data_dalam':
                data_list = diagnosa.data_dalam.split(',')
                if 0 <= index_to_remove < len(data_list):
                    del data_list[index_to_remove]
                    diagnosa.data_dalam = ','.join(data_list)

            # Simpan perubahan ke model Diagnosa
            diagnosa.save()
            logger.debug(f"Diagnosa ID {diagnosa.id} berhasil diperbarui setelah penghapusan gejala")

        for pakar in pakar_list:
            logger.debug(f"Proses menghapus nilai pada pakar ID: {pakar.id}")
            if jenis_gejala == 'data_gejala':
                pakar_data_list = pakar.data_gejala.split(',')
                if 0 <= index_to_remove < len(pakar_data_list):
                    del pakar_data_list[index_to_remove]
                    pakar.data_gejala = ','.join(pakar_data_list)
            elif jenis_gejala == 'data_khusus':
                pakar_data_list = pakar.data_khusus.split(',')
                if 0 <= index_to_remove < len(pakar_data_list):
                    del pakar_data_list[index_to_remove]
                    pakar.data_khusus = ','.join(pakar_data_list)

            # Simpan perubahan ke model Pakar
            pakar.save()
            logger.debug(f"Pakar ID {pakar.id} berhasil diperbarui setelah penghapusan gejala")

        # Hapus gejala setelah memperbarui Diagnosa dan Pakar
        gejala.delete()
        logger.debug(f"Gejala ID {id} berhasil dihapus dari database")
        return redirect("diagnosa:gejala")
