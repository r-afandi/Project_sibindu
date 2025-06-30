from re import escape
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ...models.m_kepakaran import Diagnosa,Gejala, TipePenyakit
from ....decorator import auth_required
from ...forms.data_diagnosa.f_data_diagnosa import FormDiagnosa
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ....views import add_notify
from ....models import Notifikasi
from django.db.models import Case, When, IntegerField
from django.db.models import Max,Min
decorators = [login_required,auth_required(required_permissions=['view_diagnosa', 'add_diagnosa', 'change_diagnosa', 'delete_diagnosa'], model_class=Diagnosa), add_notify(feature='data diagnosa', view_name='diagnosa:diagnosa',model=Diagnosa, name_field='diagnosa')]

@method_decorator(decorators, name='dispatch')
class DiagnosaListView(View):
    def get(self, request):
        user=request.user
        data = Diagnosa.objects.all()
        
        nama_tabel=Gejala.objects.only('id','nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')
        


        form = FormDiagnosa()
        transformed_data_suspek = []
        for suspek in data:
            suspek.gejala = f'{suspek.data_gejala},{suspek.data_khusus},{suspek.data_luar},{suspek.data_dalam}'
            suspek.gejala = suspek.gejala.split(',')
            transformed_data_suspek.append(suspek)

        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'nama_tabel': nama_tabel,
            'menu': request.menu,
            'groups': request.groups,

        }

        return render(request, 'expert/data_diagnosa/data_diagnosa.html', context)

    def post(self, request):
        form = FormDiagnosa(request.POST)
        tipe=TipePenyakit.objects.values_list('kode', flat=True)
        tipe=tipe.aggregate(Max('kode'))['kode__max']
        print(tipe)
        # Mencari entri dengan kode yang paling besar yang dimulai dengan sdp dan date
        latest_entry = Diagnosa.objects.filter(kode__startswith=f'{tipe}').aggregate(Max('kode'))
        print(latest_entry)
        # Jika ada entri yang sudah ada, ambil bagian urutan dari kode tersebut dan tambahkan 1
        if latest_entry['kode__max']:
            max_code = latest_entry['kode__max']
    
            # Ekstrak angka urutan terakhir dari kode
            last_urut = int(max_code.split('-')[-1])
            new_urut = last_urut + 1
        else:
            # Jika tidak ada entri, mulai dengan 1
            new_urut = 1

        # Format angka urut menjadi 4 digit
        urut = f'{new_urut:04d}'


        if form.is_valid():
            # Menghasilkan kode baru dengan nomor urut yang benar
            form.instance.kode = f'{tipe}-{urut}'
            form.save()
            # Kembali ke halaman diagnosa
            return redirect("diagnosa:diagnosa")

        context = {
            'form': form,
        }

        return render(request, 'expert/data_diagnosa/add_diagnosa.html',context)

@method_decorator(decorators, name='dispatch') 
class UpdateDiagnosaView(View):
    def post(self, request, id):
        diagnosa = get_object_or_404(Diagnosa, id=id)
        form = FormDiagnosa(request.POST, instance=diagnosa)
        tipe=TipePenyakit.objects.values_list('kode', flat=True)
        tipe=tipe.aggregate(Max('kode'))['kode__max']
        print('tipe',tipe)
        # Mencari entri dengan kode yang paling besar yang dimulai dengan sdp dan date
        latest_entry = Diagnosa.objects.filter(kode__startswith=f'{tipe}').aggregate(Max('kode'))
        print('last',latest_entry)
        # Jika ada entri yang sudah ada, ambil bagian urutan dari kode tersebut dan tambahkan 1
        if latest_entry['kode__max']:
            max_code = latest_entry['kode__max']
    
            # Ekstrak angka urutan terakhir dari kode
            last_urut = int(max_code.split('-')[-1])
            new_urut = last_urut + 1
        else:
            # Jika tidak ada entri, mulai dengan 1
            new_urut = 1

        # Format angka urut menjadi 4 digit
        urut = f'{new_urut:04d}'

        if form.is_valid():
            if diagnosa.kode == None:
                form.instance.kode = f'{tipe}-{urut}'
            form.save()
            return redirect("diagnosa:diagnosa")
        return render(request, 'admin/expert/data_diagnosa/edit_diagnosa.html')

@method_decorator(decorators, name='dispatch')
class DeleteDiagnosaView(View):
    def post(self, request, id):
        diagnosa = get_object_or_404(Diagnosa, id=id)
        diagnosa.delete()
        return redirect("diagnosa:diagnosa")
