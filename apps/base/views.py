from django import template
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Case, When, IntegerField
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib import messages
from functools import wraps
from .decorator import get_auth_key
#untuk
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.base.posbindu.models.laporan.m_laporan_sdp import DataSdp, LaporanSdp, Kondisi
from .forms import LoginForm
# home
from django.contrib import messages
from django.views import View
from .models import Menu, MenuHome
#laporan
from .posbindu.models.laporan.m_laporan_kegiatan import LaporanKegiatan as ModelLaporan 
from .posbindu.models.m_about import About as modelAbout
from .posbindu.models.informasi.m_pengumuman import Pengumuman as ModelPengumumuman
from .posbindu.models.informasi.m_artikel import Artikel as ModelArtikel
from django.db.models import Q
from .expert.models.m_kepakaran import Diagnosa,Gejala, Kepakaran
from .posbindu.models.data_suspek.m_data_suspek import DataSuspek, Gender
from .models import Dashboard as AsDashboard
from .forms import DiagnosaFc,FeedbackForm
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .expert.naive_bayes import load_model
import numpy as np
from django.http import JsonResponse
from ..base.posbindu.models.informasi.m_pengumuman import Pengumuman as ModelPengumuman
from ..base.posbindu.models.laporan.m_laporan_kegiatan import LaporanKegiatan as ModelKegiatan
#notification
from functools import wraps

from .models import Notifikasi
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from datetime import datetime
from django.db.models import Max, Count, Sum


class Index(View):

    @method_decorator(cache_page(60 * 15))  # Cache halaman selama 15 menit
    def get(self, request):
        # Cek apakah data ada di cache
        if cache.get('index_data'):
            context = cache.get('index_data')
        else:
            menu_home = MenuHome.objects.all()
            kegiatan = ModelLaporan.objects.filter(validasi=1, foto__isnull=False).select_related().order_by('-created_at')[:3]
            pengumuman = ModelPengumumuman.objects.all().order_by('-created_at')[:3]
            artikel = ModelArtikel.objects.filter(validasi=1, gambar__isnull=False).select_related().order_by('-created_at')[:5]
            about = modelAbout.objects.all()

            for item in about:
                sosmed_array = item.sosmed.split(',')
                item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah

            for item in pengumuman:
                peng_tanggal = datetime.strptime(item.tanggal, '%d/%m/%Y')
                item.month = peng_tanggal.strftime('%b')
                item.day = peng_tanggal.day

            context = {
                'about': about,
                'menu_home': menu_home,
                'kegiatan': kegiatan,
                'pengumuman': pengumuman,
                'artikel': artikel
            }
            
            # Simpan context ke dalam cache
            cache.set('index_data', context, 60 * 15)  # Cache selama 15 menit

        return render(request, 'home/index.html', context)

    @method_decorator(cache_page(60 * 15))  # Cache halaman selama 15 menit
    def get(self, request):
        # Cek apakah data ada di cache
        if cache.get('index_data'):
            context = cache.get('index_data')
        else:
            menu_home = MenuHome.objects.all()
            kegiatan = ModelLaporan.objects.filter(validasi=1, foto__isnull=False).order_by('-created_at')
            pengumuman = ModelPengumumuman.objects.all().order_by('-created_at')[:3]
            artikel = ModelArtikel.objects.filter(validasi=1, gambar__isnull=False).order_by('-created_at')
            about = modelAbout.objects.all()

            for item in about:
                sosmed_array = item.sosmed.split(',')
                item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah

            for item in pengumuman:
                peng_tanggal = datetime.strptime(item.tanggal, '%d/%m/%Y')
                item.month = peng_tanggal.strftime('%b')
                item.day = peng_tanggal.day

            context = {
                'about': about,
                'menu_home': menu_home,
                'kegiatan': kegiatan,
                'pengumuman': pengumuman,
                'artikel': artikel
            }
            
            # Simpan context ke dalam cache
            cache.set('index_data', context, 60 * 15)  # Cache selama 15 menit

        return render(request, 'home/index.html', context)

class Berita(View): 
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        artikel= ModelArtikel.objects.filter(validasi=1 , gambar__isnull=False).order_by('-created_at')
        artikel_first= artikel.first()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(artikel,  3) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        context={
        'about':about,
        'menu_home':menu_home,   
        'artikel':artikel ,
        'artikel_first':artikel_first,
        'paginator':paginator,
        'page_obj':page_obj

        }
        return render(request, 'home/berita.html',context)

class BeritaSatuan(View): 
    def get(self, request,id):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        artikel_id= ModelArtikel.objects.filter(id=id)
        artikel= ModelArtikel.objects.filter(validasi=1, gambar__isnull=False).select_related().order_by('-created_at')
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        context={
        'about':about,
        'menu_home':menu_home,   
        'artikel':artikel,
        'artikel_id':artikel_id,

        }
        return render(request, 'home/berita_satuan.html',context)

class Pengumuman(View): 

    def get(self, request):
        menu_home = MenuHome.objects.all()
        pengumuman= ModelPengumumuman.objects.all().order_by('-id')
        about = modelAbout.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(pengumuman,  3) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
            for item in page_obj:
                peng_tanggal = datetime.strptime(item.tanggal, '%d/%m/%Y')
                item.month= peng_tanggal.strftime('%b')
                item.day= peng_tanggal.day
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        
        context={
        'about':about,
        'menu_home':menu_home,  
        'pengumuman':pengumuman,
        'page_obj':page_obj        
        }
        return render(request, 'home/pengumuman.html',context)
    def search(self,request):
        # Get the search and date query parameters
        #search = request.GET.get('search')
        #date = request.GET.get('tanggal')
        # Create a filter object
        filter = Q(judul__icontains="pasar")

        # Get the filtered pengumuman
        pengumuman = ModelPengumumuman.objects.filter(filter).order_by('-tanggal')

        # Pass data to the template
        return render(request, 'home/pengumuman.html', {
            'pengumuman': pengumuman,
        })

class PengumumanDetailView(View):
    def get(self, request, id):
        pengumuman = get_object_or_404(ModelPengumuman, id=id)
        data = {
            'judul': pengumuman.judul,
            'pengumuman': pengumuman.pengumuman,
            'tanggal': pengumuman.tanggal,
            'waktu': pengumuman.waktu,
            'tempat': pengumuman.tempat
        }
        return JsonResponse(data)

class KegitanDetailView(View):
    def get(self, request, id):
        pengumuman = get_object_or_404(ModelKegiatan, id=id)
        data = {
            'nama': pengumuman.nama,
            'tanggal': pengumuman.tanggal,
            'kegiatan': pengumuman.kegiatan
        }
        return JsonResponse(data)

class CekDiabetes(View):
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        gejala = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by('jenis')
        gejala_first = gejala.first()
        form = DiagnosaFc()
        feedback = FeedbackForm()
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        context = {
            'feedback': feedback,
            'about': about,
            'menu_home': menu_home,
            'form': form,
            'gejala': gejala,
            'current_step': f'{gejala_first}-part',
        }
        return render(request, 'home/cek_diabetes.html', context)

    def post(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        form = DiagnosaFc(request.POST)
        feedback = FeedbackForm(request.POST)
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah

        if form.is_valid():
            # Ambil data dari formulir
            gejala = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by('jenis')
            fields = [i.alias for i in gejala]

            # Validasi data_gejala dan data_khusus
            if fields is None:
                return render(request, 'home/cek_diabetes.html', {'form': form, 'error': 'Data gejala atau data khusus tidak ada.'})

            try:
                # Pisahkan string berdasarkan koma dan ubah ke array numerik
                data_array = [float(request.POST.get(field, 0)) for field in fields]

            except ValueError:
                return render(request, 'home/cek_diabetes.html', {'form': form, 'error': 'Format data gejala atau data khusus tidak valid.'})

            # Gabungkan data gejala dan data khusus menjadi satu array
            input_data = np.array([data_array])
            # Muat model dan lakukan prediksi
            model = load_model()
            prediction = model.predict(input_data)
            diagnosa = Diagnosa.objects.get(id=prediction[0])
            penanganan = diagnosa.penanganan
            tindakan_dict = {gejala.alias: gejala.penanganan.split('\n') for gejala in gejala}

            # Tentukan penanganan yang sesuai berdasarkan gejala yang terdeteksi
            tindakan = {gejala.nama: tindakan_dict[gejala.alias] for gejala in gejala if request.POST.get(gejala.alias, '0') == '1'}
           
            context = {
                'form': form,
                'about': about,
                'menu_home': menu_home,
                'diagnosa': diagnosa,
                'penanganan': penanganan,
                'tindakan': tindakan,
                'feedback': feedback
            }
                
            if feedback.is_valid():
                cd = feedback.cleaned_data
                gejala_fields = Gejala.objects.only('id', 'nama', 'alias').annotate(
                    jenis_order=Case(
                        When(jenis='data_gejala', then=0),
                        When(jenis='data_khusus', then=1),
                        output_field=IntegerField(),
                    )
                ).order_by('jenis_order')

                # Simpan data gejala dan data khusus sebagai dictionary
                data_gejala = [int(request.POST.get(gejala_field.alias, 0)) for gejala_field in gejala_fields if gejala_field.jenis == 'data_gejala']
                data_gejala= ','.join(map(str, data_gejala)) 

                data_khusus = [int(request.POST.get(gejala_field.alias, 0)) for gejala_field in gejala_fields if gejala_field.jenis == 'data_khusus']
                data_khusus = ','.join(map(str, data_khusus)) 
                

                pc = Kepakaran(
                    umur=cd['umur'],
                    alasan=cd['alasan'],
                    diagnosa_sistem=diagnosa,
                    diagnosa_suspek=cd['diagnosa_suspek'],
                    data_gejala=data_gejala,  # Simpan data gejala
                    data_khusus=data_khusus   # Simpan data khusus
                )
                print('Data Kepakaran: ', pc)
                pc.save()
                messages.success(request, "Feedback berhasil dikirim.")
                return HttpResponseRedirect(reverse('sibindu:cek_diabetes'))  
            else:
                print('Data Kepakaran: ', feedback.errors)
                return render(request, 'home/hasil.html', context)
        # Jika formulir tidak valid, tampilkan error
        
        return render(request, 'home/cek_diabetes.html', {'form': form})

class Statistik(View):
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        pengumuman= ModelPengumumuman.objects.filter(jenis_id='1')
        tanggal_pengumuman = pengumuman.values_list('tanggal', flat=True).distinct()
        suspek = DataSuspek.objects.filter(tanggal__in=tanggal_pengumuman).order_by('-tanggal')
        gender = Gender.objects.all()
        diagnosa = Diagnosa.objects.all()

        # Data untuk grafik garis berdasarkan pengumuman
        all_dates = suspek.values_list('tanggal', flat=True).distinct()
        total_by_date = {
            date: suspek.filter(tanggal=date).count() 
            for date in all_dates
        }

        # Total by gender berdasarkan pengumuman
        total_by_gender = {
            g.id: {
                date: suspek.filter(tanggal=date, gender_id=g.id).count() 
                for date in all_dates
            } 
            for g in gender
        }

        # Data berdasarkan diagnosa dan pengumuman
        total_by_diagnosa = {
            d.id: {
                date: suspek.filter(tanggal=date, diagnosa_id=d.id).count() 
                for date in all_dates
            } 
            for d in diagnosa
        }

        # Total by diagnosa dan gender berdasarkan pengumuman
        total_by_diagnosa_gender = {
            d.id: {
                g.id: [
                    suspek.filter(tanggal=date, diagnosa_id=d.id, gender_id=g.id).count() 
                    for date in all_dates
                ] 
                for g in gender
            } 
            for d in diagnosa
        }

        context = {
            'about': about,
            'menu_home': menu_home,
            'total_by_date': total_by_date,
            'total_by_gender': total_by_gender,
            'total_by_diagnosa': total_by_diagnosa,
            'total_by_diagnosa_gender': total_by_diagnosa_gender,
            'all_dates': list(all_dates),
            'gender_labels': [g.nama for g in gender],
            'diagnosa_labels': [d.diagnosa for d in diagnosa],
        }

        return render(request, 'home/statistik.html', context)

class About(View): 
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
                

        context={
        'about':about,
        'menu_home':menu_home,              
        }
        return render(request, 'home/about.html',context)

class CustomLoginView(View):
    template_name = 'layouts/auth/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                if remember:
                    request.session.set_expiry(1209600)  # 2 minggu
                else:
                    request.session.set_expiry(0)  # sesi browser
                return redirect('dashboard')
            else:
                form.add_error(None, 'Username atau password salah')
                messages.error(request, 'Username atau password salah')
        return render(request, self.template_name, {'form': form})   
    
#segera perbaiki secepatnya karena mudah di hack
class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        # Melakukan logout pengguna
        logout(request)
        # Menambahkan pesan setelah logout
        messages.add_message(request, messages.SUCCESS, 'Anda berhasil logout.')
        # Redirect ke halaman index
        return redirect('sibindu:index')

class Search(View):
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        
        # Memecah sosmed menjadi array
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array
        
        query = request.GET.get('q', '')
        # Tambahkan validasi=1 pada filter artikel dan kegiatan
        artikel = ModelArtikel.objects.filter(
            Q(judul__icontains=query) | Q(artikel__icontains=query), 
            validasi=1
        ) if query else ModelArtikel.objects.none()
        
        pengumuman = ModelPengumuman.objects.filter(
            Q(judul__icontains=query) | Q(pengumuman__icontains=query)
        ) if query else ModelPengumuman.objects.none()
        
        kegiatan = ModelKegiatan.objects.filter(
            Q(nama__icontains=query) | Q(kegiatan__icontains=query), 
            validasi=1
        ) if query else ModelKegiatan.objects.none()

        # Pagination untuk artikel
        artikel_page_num = request.GET.get('artikel_page', 1)
        artikel_page_obj = self.get_paginated_objects(artikel, artikel_page_num, 3)

        # Pagination untuk pengumuman
        pengumuman_page_num = request.GET.get('pengumuman_page', 1)
        pengumuman_page_obj = self.get_paginated_objects(pengumuman, pengumuman_page_num, 3)
        
        # Tambahkan pengolahan tanggal untuk pengumuman
        for item in pengumuman_page_obj:
            peng_tanggal = datetime.strptime(item.tanggal, '%d/%m/%Y')
            item.month = peng_tanggal.strftime('%b')
            item.day = peng_tanggal.day

        # Pagination untuk kegiatan
        kegiatan_page_num = request.GET.get('kegiatan_page', 1)
        kegiatan_page_obj = self.get_paginated_objects(kegiatan, kegiatan_page_num, 3)

        context = {
            'menu_home': menu_home,
            'about': about,
            'artikel_page_obj': artikel_page_obj,
            'pengumuman_page_obj': pengumuman_page_obj,
            'kegiatan_page_obj': kegiatan_page_obj,
        }
        return render(request, 'home/search_content.html', context)

    def get_paginated_objects(self, queryset, page_num, per_page):
        paginator = Paginator(queryset, per_page)
        try:
            return paginator.page(page_num)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)


register = template.Library()
@register.filter
def detailed_timesince(value):
    now = datetime.now()
    diff = now - value
    
    periods = (
        (diff.days // 365, "year", "years"),
        (diff.days // 30, "month", "months"),
        (diff.days % 30, "day", "days"),
        (diff.seconds // 3600, "hour", "hours"),
        ((diff.seconds // 60) % 60, "minute", "minutes"),
        (diff.seconds % 60, "second", "seconds"),
    )
    
    time_string = ""
    for period, singular, plural in periods:
        if period > 0:
            time_string += f"{period} {singular if period == 1 else plural} "
    
    if not time_string:
        return "just now"
    
    return time_string + "ago"

def get_universal_url(view_name, *args, **kwargs):
    try:
        url = reverse(view_name)
        return url
    except Exception as e:
        print(f"Error in generating URL: {e}")
        return '#'

def add_notify(feature, view_name=None, model=None, name_field='nama'):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            verb = None
            topik = None

            # Tentukan id objek
            obj_id = kwargs.get('id', None)
            
            # Debugging obj_id dan model
            print(f"Debug: obj_id={obj_id}, model={model}")

            if request.method == 'DELETE' or (request.method == 'POST' and request.POST.get('_method') == 'DELETE'):
                verb = 'menghapus'
            elif request.method == 'POST':
                # Debugging verb untuk POST
                print(f"Debug: POST request, obj_id={obj_id}, method={request.method}")

                # Cek jika obj_id ada dan model ada
                if obj_id is not None and model is not None:
                    try:
                        # Ambil instance dari model
                        instance = model.objects.get(id=obj_id)
                        topik = getattr(instance, name_field, None)
                        if topik is None:
                            topik = 'Nama tidak tersedia'  # Fallback jika nama kosong
                    except model.DoesNotExist:
                        topik = 'Nama tidak ditemukan'  # Fallback jika objek tidak ada

                # Tentukan verb berdasarkan kondisi
                if obj_id is None:
                    verb = 'menambah'
                elif user.groups.filter(id=3).exists():
                    validasi = request.POST.get('validasi')
                    if validasi == '1':
                        verb = 'validasi'
                    elif validasi == '2':
                        verb = 'menolak'
                    else:
                        verb = 'mengubah'
                else:
                    verb = 'mengubah'

            # Debugging verb setelah logika di atas
            print(f"Debug: verb={verb}, topik={topik}")

            # Memanggil fungsi asli dan mendapatkan response
            response = func(request, *args, **kwargs)

            # Debugging sebelum menyimpan notifikasi
            print(f"Creating notification: feature={feature}, verb={verb}, user={user}, topik={topik}")

            # Buat notifikasi jika POST atau DELETE
            if request.method in ['POST', 'DELETE']:
                url = get_universal_url(view_name, *args, **kwargs) if view_name else '#'
                
                # Simpan notifikasi
                Notifikasi.objects.create(
                    fitur=feature,
                    verb=verb or 'Tidak ada aksi',  # Fallback jika verb None
                    user=user.first_name if user else 'Tidak dikenal',  # Fallback jika user None
                    url=url,
                    nama=topik or 'Topik tidak ditemukan'  # Fallback jika topik None
                )
                
            return response
        return wrapper
    return decorator

def show_notifications(request, id=None):
    user = request.user
    if id:
        # Get the specific notification by ID
        notifications = Notifikasi.objects.filter(id=id, is_deleted=False).exclude(read_by=user).order_by('-created_at')
    else:
        # Get all notifications
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')

    jumlah = notifications.count()
    menu, group = get_auth_key(request) 
    context = {
        'notifications': notifications,
        'jumlah': jumlah,
        'menu': menu,
        'group': group,
    }
    return render(request, 'includes/notifikasi.html', context)
@csrf_exempt
@require_http_methods(["POST"])
def mark_as_read(request, id):
    notification = get_object_or_404(Notifikasi, id=id)
    user = request.user

    if user in notification.read_by.all():
        notification.read_by.remove(user)
        if notification.read_by.count() == 0:
            notification.is_read = False
    else:
        notification.read_by.add(user)
        notification.is_read = True

    notification.save()
    return JsonResponse({'status': 'success'})

def delete_notification(request, id):
    notification = get_object_or_404(Notifikasi, id=id)
    user = request.user
    notification.deleted_by.add(user)
    if notification.deleted_by.count() == 0:
        notification.is_deleted = True
    notification.save()
    return JsonResponse({'status': 'success'})

decorators = [login_required]

@method_decorator(decorators, name='dispatch')
class Dashboard(View): 
    def get(self, request):
        user = request.user
        menu, groups = get_auth_key(request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()    
        
        sdp = LaporanSdp.objects.filter(
    Q(kadaluarsa__isnull=False) | Q(kondisi_id__in=[3, 4])
)
        kondisi = Kondisi.objects.all()
        pengelolaan_sdp = DataSdp.objects.annotate(
        total_masuk=Sum('laporansdp__masuk', filter=Q(laporansdp__validasi=1)),
        total_keluar=Sum('laporansdp__keluar', filter=Q(laporansdp__validasi=1)),
        )

        keuangan_sdp = LaporanSdp.objects.filter(validasi=1)
            # Menghitung selisih (masuk - keluar)
        for i in pengelolaan_sdp:
            i.total = (i.total_masuk or 0) - (i.total_keluar or 0)
    
        exp = datetime.now()
        data_sdp = []
        sdp_data = []
        for i in sdp:
            kadaluarsa_str = i.kadaluarsa.strip() if i.kadaluarsa else None  # Periksa dan strip spasi
            bg = None  # Inisialisasi bg
            name = None  # Inisialisasi name
            i_kadaluarsa_date = None  # Inisialisasi kadaluarsa date

            if kadaluarsa_str:  # Jika kadaluarsa_str ada
                try:
                    # Mengubah string kadaluarsa menjadi objek date
                    i_kadaluarsa_date = datetime.strptime(kadaluarsa_str, '%d/%m/%Y').date()
                    if i_kadaluarsa_date < exp.date():  # Jika sudah kadaluarsa
                        bg = 'danger'
                        name = 'Kadaluarsa'
                except ValueError as e:
                    bg = 'warning'
                    name = 'Format Error'
            elif i.kondisi_id in [3, 4]:  # Jika kondisi_id adalah 3 atau 4
                kondisi_obj = kondisi.get(id=i.kondisi_id)
                bg = kondisi_obj.badge
                name = kondisi_obj.nama

            # Pastikan bahwa bg dan name telah diinisialisasi sebelum menambahkannya ke sdp_data
            if bg and name:
                sdp_data.append({'obj': i, 'bg': bg, 'name': name, 'kadaluarsa': i_kadaluarsa_date})
        pengumuman= ModelPengumumuman.objects.filter(jenis_id='1')
        tanggal_pengumuman = pengumuman.values_list('tanggal', flat=True).distinct()
        suspek = DataSuspek.objects.filter(tanggal__in=tanggal_pengumuman).order_by('-tanggal')
        gender = Gender.objects.all()
        diagnosa = Diagnosa.objects.all()
        all_dates = suspek.values_list('tanggal', flat=True).distinct()
        total_by_date = {date: suspek.filter(tanggal=date).count() for date in all_dates}
        total_by_gender = {g.id: {date: suspek.filter(tanggal=date, gender_id=g.id).count() for date in all_dates} for g in gender}
        
        total_by_diagnosa = {d.id: {date: suspek.filter(tanggal=date, diagnosa_id=d.id).count() for date in all_dates} for d in diagnosa}
        total_by_diagnosa_gender = {d.id: {g.id: [suspek.filter(tanggal=date, diagnosa_id=d.id, gender_id=g.id).count() for date in all_dates] for g in gender} for d in diagnosa}

                    
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'menu': menu,
            'groups': groups,
            'user': user,
            'sdp': sdp,
            'suspek': suspek,
            'gender': gender,
            'total_by_date': total_by_date,
            'total_by_gender': total_by_gender,
            'total_by_diagnosa': total_by_diagnosa,
            'total_by_diagnosa_gender': total_by_diagnosa_gender,
            'all_dates': list(all_dates),
            'gender_labels': [g.nama for g in gender],
            'diagnosa_labels': [d.diagnosa for d in diagnosa],
            'pengelolaan_sdp': pengelolaan_sdp,
            'keuangan_sdp': keuangan_sdp,
            'data_sdp': data_sdp,
            'exp': exp,
            'sdp_data': sdp_data,
        } 

        return render(request, 'office/dashboard.html', context)
@method_decorator(decorators, name='dispatch')
class MenuView(View):    
    def get(self, request):

        context={
            'menu': request.menu,
            'groups': request.groups,
            }
        return render(request, 'includes/aside.html', context)
    
@csrf_exempt
def csrfToken(request):
    data = {'csrfToken': 'your-csrf-token-value'}
    return JsonResponse(data)