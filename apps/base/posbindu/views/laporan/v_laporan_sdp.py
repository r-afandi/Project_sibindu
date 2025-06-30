from django.db.models import Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ....decorator import auth_required
from ...models.laporan.m_laporan_sdp import LaporanSdp,DataSdp,Kondisi
from ...forms.laporan.f_laporan_sdp import FormLapSdp, FormSdp
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django_drf_filepond.api import store_upload,get_stored_upload,get_stored_upload_file_data,delete_stored_upload
from django_drf_filepond.models import TemporaryUpload, StoredUpload
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime
from django.utils import timezone
from ....views import add_notify
from ....models import Notifikasi
import logging

# Setup logging
logger = logging.getLogger(__name__)

decorators1 = [login_required, auth_required(required_permissions=['view_sdp', 'add_sdp', 'change_sdp', 'delete_sdp'], model_class=LaporanSdp),add_notify(feature='Data SDP', view_name='sdp:sdp_list',model=LaporanSdp, name_field='nama')]
@method_decorator(decorators1, name='dispatch')
class LaporanSdpListView(View):
    def get(self, request):
        group_id = [group.id for group in request.groups]
        data = LaporanSdp.objects.all()
        kondisi = Kondisi.objects.all()
        form = FormLapSdp(request=request)
        exp =  datetime.now().date()
        kadaluarsa = []
        for i in data:
            if i.kadaluarsa:  # Check if kadaluarsa field is not empty
                try:
                    i_kadaluarsa_datetime = datetime.strptime(i.kadaluarsa, '%d/%m/%Y').date()
                    if i_kadaluarsa_datetime < exp:
                        bg = 'danger'
                        name = 'Kadaluarsa'
                    else:
                        bg = 'success'
                        name = 'Tidak Kadaluarsa'
                except ValueError:  # Handle invalid date format
                    bg = 'warning'
                    name = 'Tanggal tidak valid'
            else:
                bg = 'secondary'
                name = 'Tidak ada'

            kadaluarsa.append({'obj': i, 'bg': bg, 'name': name})
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=request.user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,  
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
            'group_id': group_id,
            'kondisi': kondisi,
            'data': kadaluarsa,
            'exp': exp,
        }

        return render(request, 'office/laporan/laporan_sdp/laporan_sdp.html', context)
    def post(self, request):
        if request.method == 'POST':
            form = FormLapSdp(request.POST, request.FILES, request=request)
            date = datetime.now().strftime('%d%m%Y')
            if form.is_valid():
                jenis_id = request.POST.get('jenis')
                sdp = DataSdp.objects.filter(id=jenis_id).values_list('kode', flat=True).first()

                if sdp is None:
                    raise ValueError("Kode tidak ditemukan untuk jenis_id tersebut")


                # Cari entry terbaru yang memiliki kode dengan prefix yang sesuai
                latest_entry = LaporanSdp.objects.filter(kode__startswith=f'{sdp}{date}').aggregate(Max('kode'))

                if latest_entry['kode__max']:
                    max_code = latest_entry['kode__max']
                    last_urut = int(max_code.split('')[-1])  # Ambil nomor urut terakhir
                    new_urut = last_urut + 1
                else:
                    new_urut = 1

                # Format urutan dengan 4 digit angka
                urut = f'{new_urut:04d}'
                # Set nilai kode pada instance form
                form.instance.kode = f'{sdp}-{date}{urut}'

                # Penanganan upload file
                upload_id = request.POST.get('filepond')

                if upload_id:
                    try:
                        temp = TemporaryUpload.objects.filter(upload_id=upload_id).order_by('-uploaded').first()
                    except TemporaryUpload.DoesNotExist:
                        raise ValueError("File tidak ditemukan")

                    # Jika ada file baru, proses upload
                    filename = temp.upload_name
                    form.instance.upload = temp.upload_id
                    destination_file_path = f'bukti_sdp/{date}_{filename}'
                    store_upload(upload_id=temp.upload_id, destination_file_path=destination_file_path)
                    form.instance.bukti = destination_file_path  # Simpan path file ke form
                else:
                    # Jika tidak ada file baru, pertahankan file bukti yang lama (jika ada)
                    form.instance.bukti = form.instance.bukti or None

                # Simpan form dengan data terbaru
                form.save()

            return redirect('sdp:sdp_list')

@method_decorator(decorators1, name='dispatch')
class DetailSdpView(View):
    def get(self, request, kode):
        group_id = [group.id for group in request.groups]
        user = request.user
        data = LaporanSdp.objects.filter(kode=kode)
        kondisi = Kondisi.objects.all()
        exp =  datetime.now().date()
        kadaluarsa = []
        for i in data:
            if i.kadaluarsa:  # Check if kadaluarsa field is not empty
                try:
                    i_kadaluarsa_datetime = datetime.strptime(i.kadaluarsa, '%d/%m/%Y').date()
                    
                    if i_kadaluarsa_datetime < exp:
                        bg = 'danger'
                        name = 'Kadaluarsa'
                    else:
                        bg = 'success'
                        name = 'Tidak Kadaluarsa'
                except ValueError:  # Handle invalid date format
                    bg = 'warning'
                    name = 'Tanggal tidak valid'
            else:
                bg = 'secondary'
                name = 'Tidak ada'

            kadaluarsa.append({'obj': i, 'bg': bg, 'name': name})

        form = FormLapSdp(request=request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'form': form,
            'menu': request.menu,
            'group': request.groups,
            'group_id': group_id,
            'kondisi': kondisi,
            'data': kadaluarsa,
            'exp': exp,
            'is_detail': True
        }
        return render(request, 'office/laporan/laporan_sdp/laporan_sdp.html', context)

@method_decorator(decorators1, name='dispatch')
class UpdateLaporanSdpView(View):
    def get(self, request, id):
        user = request.user
        data = LaporanSdp.objects.filter(id=id)
        kondisi = Kondisi.objects.all()
        exp = datetime.now().date()
        kadaluarsa = []
        print('sdp 1 :',data.jenis_id)
        for i in data:
            if i.kadaluarsa:  # Check if kadaluarsa field is not empty
                try:
                    i_kadaluarsa_datetime = datetime.strptime(i.kadaluarsa, '%d/%m/%Y').date()
                    
                    if i_kadaluarsa_datetime < exp:
                        bg = 'danger'
                        name = 'Kadaluarsa'
                    else:
                        bg = 'success'
                        name = 'Tidak Kadaluarsa'
                except ValueError:  # Handle invalid date format
                    bg = 'warning'
                    name = 'Tanggal tidak valid'
            else:
                bg = 'secondary'
                name = 'Tidak ada'

            if i.id:
                kadaluarsa.append({'obj': i, 'bg': bg, 'name': name})
            print('id =', i.id)
        print('kadaluarsa =', kadaluarsa)

        form = FormLapSdp(request=request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'form': form,
            'menu': request.menu,
            'group': request.groups,
            'kondisi': kondisi,
            'data': kadaluarsa,
            'exp': exp,
        }
        return render(request, 'office/laporan/laporan_sdp/laporan_sdp.html', context)

    def post(self, request, id):
        user = request.user
        sdp = get_object_or_404(LaporanSdp, id=id)
        form = FormLapSdp(request.POST, instance=sdp, request=request)
        old_jenis=sdp.jenis_id
        
        try:
            data = StoredUpload.objects.get(upload_id=sdp.upload)
        except StoredUpload.DoesNotExist:
            data = None

        temp = TemporaryUpload.objects.filter(uploaded_by=user.id).order_by('-uploaded').first()
        
        if form.is_valid():
            jenis = form.cleaned_data.get('jenis')
            date_str = datetime.now().strftime('%d%m%Y')
            if jenis.id != old_jenis:
                prefix = jenis.kode.split('-')[0]  # Ambil prefix sebelum tanda "-"

                latest_entry = LaporanSdp.objects.filter(
                    kode__startswith=f'{prefix}-'
                ).order_by('-kode').first()

                if latest_entry:
                    kode_parts = latest_entry.kode.split('-')
                    tanggal_lama = kode_parts[1][:8]
                    last_urut = int(kode_parts[1][8:])
                    new_urut = last_urut + 1
                    urut_baru = f'{new_urut:04d}'
                    new_kode = f'{prefix}-{date_str}{urut_baru}'
                else:
                    urut_baru = '0001'
                    new_kode = f'{prefix}-{date_str}{urut_baru}'

                if sdp.kode != new_kode:
                    form.instance.kode = new_kode
            if temp is not None:
                if data is not None:
                    delete_stored_upload(upload_id=data.upload_id, delete_file=True)

                filename = temp.upload_name
                form.instance.upload = temp.upload_id
                date = datetime.now().strftime('%Y-%m-%d')
                store_upload(upload_id=temp.upload_id, destination_file_path=f'bukti_sdp/{date}_{filename}')
                form.instance.bukti = f'bukti_sdp/{date}_{filename}'

            # Save form and debug after save
            form.save()
            return redirect("sdp:sdp_list")

        # If form is not valid, debu

        context = {'form': form}
        return render(request, 'office/laporan/laporan_sdp/edit_sdp.html', context)
@method_decorator(decorators1, name='dispatch')
class DeleteLaporanSdpView(View):
    def post(self, request, id):
        sdp = get_object_or_404(LaporanSdp, id=id)
        data= StoredUpload.objects.get(upload_id=sdp.upload)
        delete_stored_upload(upload_id=data.upload_id, delete_file=True)  
        if sdp.bukti:
            sdp.bukti.delete(save=False)
        sdp.delete()
        return redirect("sdp:sdp_list")

decorators2 = [login_required, auth_required(required_permissions=['view_data_sdp', 'add_data_sdp', 'change_data_sdp', 'delete_data_sdp'], model_class=DataSdp),add_notify(feature='Data SDP', view_name='sdp:data_sdp',model=DataSdp, name_field='nama')]
@method_decorator(decorators2, name='dispatch')
class SdpListView(View):
    def get(self, request):
        user = request.user
        data = DataSdp.objects.all()
        form = FormSdp()
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
        }
        return render(request, 'office/laporan/data_sdp/data_sdp.html', context)
    def post(self, request):
        if request.method == 'POST':
            form = FormSdp(request.POST)
            if form.is_valid():
                form.save()
                return redirect("sdp:data_sdp") 
            else:
                # Handle form validation errors here
                context = {
                    'form': form,
                }           

            return render(request, 'office/laporan/data_sdp/add_sdp.html',context)
    def search(self,request):
        data_view = LaporanSdp.objects.all()
        data = DataSdp.objects.all()


@method_decorator(decorators2, name='dispatch')
class UpdateSdpView(View):
    def get(self, request, id):
        sdp = get_object_or_404(DataSdp, id=id)
        form = FormSdp(request=request)
        context = {
            'sdp': sdp,
            'form': form,
        }
        return render(request, 'office/laporan/data_sdp/edit_sdp.html', context)

    def post(self, request, id):
        sdp = get_object_or_404(DataSdp, id=id)
        form = FormSdp(instance=sdp,data=request.POST or None)
        if form.is_valid():
            form.save()
            laporan_sdps = LaporanSdp.objects.filter(jenis_id=id)

            # Ambil awalan kode yang baru dari DataSdp setelah disimpan
            new_prefix = sdp.kode  # Misal ambil karakter pertama dari kode di DataSdp

            # Update awalan kode di setiap entri LaporanSdp yang terkait
            for laporan_sdp in laporan_sdps:
                # Pecah kode menjadi prefix dan bagian lainnya (tanggal dan nomor urut)
                kode_parts = laporan_sdp.kode.split('-')
                if len(kode_parts) > 1:
                    # Ganti awalan kode dengan prefix yang baru
                    kode_parts[0] = new_prefix
                    # Gabungkan kembali bagian-bagian kode dengan tanda "-"
                    laporan_sdp.kode = '-'.join(kode_parts)
                    # Simpan perubahan pada LaporanSdp
                    laporan_sdp.save()

            return redirect("sdp:data_sdp") 
        return render(request, 'office/laporan/data_sdp/data_sdp.html')
    
@method_decorator(decorators2, name='dispatch')
class DeleteSdpView(View):
    def post(self, request, id):
        sdp = get_object_or_404(DataSdp, id=id)
        sdp.delete()
        return redirect("sdp:data_sdp") 
