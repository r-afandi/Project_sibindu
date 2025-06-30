from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.db import transaction
from django.core.cache import cache
from ...models.m_kepakaran import Diagnosa, Pakar,Kepakaran,Gejala
from django.db.models import Case, When, IntegerField
from ....decorator import auth_required
from ...forms.data_pakar.f_data_pakar import FormKepakaran,FormPakar
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ....views import add_notify
from ....models import Notifikasi,Menu
from django.contrib.auth.models import Group
from sklearn.naive_bayes import GaussianNB
import numpy as np
import joblib

decorators = [login_required, auth_required(required_permissions=['view_pakar', 'add_pakar', 'change_pakar', 'delete_pakar'], model_class=Pakar)]

@method_decorator(decorators, name='dispatch')
class PakarListView(View):
    def get(self, request):
        user = request.user
        data = Kepakaran.objects.only('id', 'umur', 'data_gejala', 'data_khusus','alasan', 'diagnosa_suspek', 'diagnosa_sistem')
        form = FormKepakaran()
        nama_tabel = Gejala.objects.only('id', 'nama', 'alias','jenis').annotate(
            jenis_order=Case(
                When(jenis='data_gejala', then=0),
                When(jenis='data_khusus', then=1),
                output_field=IntegerField(),
            )
        ).filter(jenis_order__lt=2).order_by('jenis_order')
    
        for item in data:
            item.gejala = (item.data_gejala + "," + item.data_khusus).split(",")

        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'nama_tabel': nama_tabel,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
        }
        return render(request, 'expert/data_pakar/data_pakar.html', context)

    def post(self, request):
        form = FormKepakaran(request.POST)
        if form.is_valid():
            form.save()
            return redirect("data_pakar:data_pakar")
        return render(request, 'expert/data_pakar/add_pakar.html', {'form': form})
@method_decorator(decorators, name='dispatch')
class UpdatePakarView(View):
    def post(self, request, id):
        pakar = get_object_or_404(Kepakaran, id=id)
        form = FormKepakaran(request.POST, instance=pakar)
        if form.is_valid():
            form.save()
            return redirect("data_pakar:data_pakar")
        return render(request, 'expert/data_pakar/edit_pakar.html', {'form': form})
    
class InputPakar(View):
    def get(self, request):
        # Ambil data dari model Pakar
        pakar_data = Pakar.objects.only('data_gejala', 'data_khusus', 'diagnosa_id')

        # Siapkan list untuk menyimpan fitur dan label
        X = []
        y = []

        # Ekstrak data dari queryset dan simpan dalam list X (fitur) dan y (label)
        for pakar in pakar_data:
            gejala = pakar.data_gejala.split(',') + pakar.data_khusus.split(',')
            gejala = [int(g) for g in gejala]  # Konversi data gejala menjadi integer
            X.append(gejala)
            y.append(pakar.diagnosa_id)

        # Konversi list ke dalam numpy array
        X = np.array(X)
        y = np.array(y)

        # Inisialisasi dan latih model Naive Bayes
        model = GaussianNB()
        model.fit(X, y)

        # Simpan model ke dalam file joblib
        joblib_file = "naive_bayes_model.joblib"  
        joblib.dump(model, joblib_file)

        # Render halaman atau redirect ke halaman yang sesuai
        return redirect("data_pakar:data_pakar")
    def post(self, request, id):
        pakar = get_object_or_404(Kepakaran, id=id)

        if pakar:
            try:
                with transaction.atomic():
                    new_pakar = Pakar.objects.create(
                        umur=pakar.umur,
                        diagnosa_id=pakar.diagnosa_suspek.id,
                        data_gejala=pakar.data_gejala,
                        data_khusus=pakar.data_khusus
                    )
                    
                    new_pakar.save()
                    print('success', new_pakar)

                    # Hapus data setelah berhasil disimpan
                    pakar.delete()
                    print('Kepakaran deleted')
                    
            except Exception as e:
                print('failed', e)
        else:
            print('failed')

        return redirect("data_pakar:data_pakar")
class TrainNaiveBayesView(View):
    def get(self, request):
        # Ambil data dari model Pakar
        pakar_data = Pakar.objects.only('data_gejala', 'data_khusus', 'diagnosa_id')

        # Siapkan list untuk menyimpan fitur dan label
        X = []
        y = []

        # Ekstrak data dari queryset dan simpan dalam list X (fitur) dan y (label)
        for pakar in pakar_data:
            gejala = pakar.data_gejala.split(',') + pakar.data_khusus.split(',')
            gejala = [int(g) for g in gejala]  # Konversi data gejala menjadi integer
            X.append(gejala)
            y.append(pakar.diagnosa_id)

        # Konversi list ke dalam numpy array
        X = np.array(X)
        y = np.array(y)

        # Inisialisasi dan latih model Naive Bayes
        model = GaussianNB()
        model.fit(X, y)

        # Simpan model ke dalam file joblib
        joblib_file = "naive_bayes_model.joblib"  
        joblib.dump(model, joblib_file)

        # Render halaman atau redirect ke halaman yang sesuai
        return redirect("data_pakar:data_pakar")

@method_decorator(decorators, name='dispatch')
class DeletePakarView(View):
    def post(self, request, id):
        pakar = get_object_or_404(Kepakaran, id=id)
        pakar.delete()
        return redirect("data_pakar:data_pakar")