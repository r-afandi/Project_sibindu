from django import template
from django.shortcuts import render,redirect
from django.urls import reverse
#untuk Login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView

from apps.base.posbindu.models.laporan.m_laporan_sdp import DataSdp, LaporanSdp, Kondisi
from .forms import LoginForm
# home
from django.contrib import messages
from django.views import View
from .models import Menu, MenuHome
from django.shortcuts import render, get_object_or_404
#laporan
from .posbindu.models.laporan.m_laporan_kegiatan import LaporanKegiatan as ModelLaporan 
from .posbindu.models.m_about import About as modelAbout
from .posbindu.models.informasi.m_pengumuman import Pengumuman as ModelPengumumuman
from .posbindu.models.informasi.m_artikel import Artikel as ModelArtikel
from django.db.models import Q
from .expert.models.m_kepakaran import Diagnosa,Gejala
from .posbindu.models.data_suspek.m_data_suspek import DataSuspek, Gender
from .models import Dashboard as AsDashboard
from django.db.models import Count,Sum
from .forms import DiagnosaFc
from django.db.models import Subquery, OuterRef
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .expert.naive_bayes import load_data, split_data, train_model, evaluate_model, save_model, load_model
import numpy as np
from django.http import JsonResponse
#notification
from functools import wraps
from .models import Notifikasi
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.utils.timesince import timesince
from django.db.models import Max, Count, Sum

class Index(View): 
    def get(self, request):
        menu_home = MenuHome.objects.all()
        kegiatan=ModelLaporan.objects.filter(validasi=1 , img__isnull=False).order_by('-created_at')
        pengumuman = ModelPengumumuman.objects.all().order_by('-created_at')[:3]
        artikel= ModelArtikel.objects.filter(validasi=1 , img__isnull=False).order_by('-created_at')
        about = modelAbout.objects.all()

        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
    

        context={
        'about':about,
        'menu_home':menu_home,   
        'kegiatan':kegiatan, 
        'pengumuman':pengumuman,
        'artikel':artikel              
        }
        return render(request, 'home/index.html',context)

class Berita(View): 
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        artikel= ModelArtikel.objects.filter(validasi=1 , img__isnull=False).order_by('-created_at')
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
        artikel= ModelArtikel.objects.all()
    
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

class CekDiabetes(View):
    def get(self, request):
        menu_home = MenuHome.objects.all()
        about = modelAbout.objects.all()
        gejala = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by('jenis')
        gejala_first = gejala.first()
        form = DiagnosaFc()
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        context = {
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
        for item in about:
            sosmed_array = item.sosmed.split(',')
            item.sosmed = sosmed_array  # Mengganti nilai data dengan array yang telah dipecah
        if form.is_valid():
            # Ambil data dari formulir
            gejala = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by('jenis')
            fields =[i.alias for i in gejala]



            # Validasi data_gejala dan data_khusus
            if fields is None:
                return render(request, 'home/cek_diabetes.html', {'form': form, 'error': 'Data gejala atau data khusus tidak ada.'})

            try:
                # Pisahkan string berdasarkan koma dan ubah ke array numerik
                data_array = [float(request.POST.get(field,0)) for field in fields]
        
            except ValueError:
                return render(request, 'home/cek_diabetes.html', {'form': form, 'error': 'Format data gejala atau data khusus tidak valid.'})

            # Gabungkan data gejala dan data khusus menjadi satu array
            input_data = np.array([data_array])
            # Muat model dan lakukan prediksi

            model = load_model()
            prediction = model.predict(input_data)
            diagnosa = Diagnosa.objects.get(id=prediction[0])
            penanganan = diagnosa.penanganan
            context = {
                'form': form,
                'about': about,
                'menu_home': menu_home,
                'diagnosis': diagnosa,
                'penanganan': penanganan  # Accuracy dapat diabaikan di sini atau ditambahkan sesuai kebutuhan
            }
            return render(request, 'home/hasil.html', context)

        # Jika formulir tidak valid, tampilkan error
        return render(request, 'home/cek_diabetes.html', {'form': form})

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
class CustomLoginView(LoginView):
    template_name = 'layouts/auth/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Username atau password salah')
                messages.error(request, 'Username atau password salah')
        return render(request, self.template_name, {'form': form})
    
class CustomLogoutView(LogoutView):
    def post(self, request): 
        logout(request)
        return redirect('sibindu:index')
    
@method_decorator(login_required, name='dispatch')
class Dashboard(View): 
    def get(self, request):
        user = request.user
        #group=user.groups.through.objects.get(user_id=user.id)
        menu, group = get_auth_key(request)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()
        suspek = DataSuspek.objects.all().order_by('tanggal')
        gender = Gender.objects.all()
        diagnosa = Diagnosa.objects.all()
        sdp = LaporanSdp.objects.filter(validasi_id='1')
        kondisi=Kondisi.objects.all()
        pengelolaan_sdp = DataSdp.objects.all()
        keuangan_sdp = LaporanSdp.objects.all()
        seen = set()
        nama_tabel = Diagnosa.objects.all()
        exp =  datetime.now()
        data_sdp = []
        sdp_data=[]
        for i in sdp:
            try:
                i_kadaluarsa_datetime = datetime.strptime(i.kadaluarsa, '%d/%m/%Y')

                if i_kadaluarsa_datetime < exp:
                    bg = 'danger'
                    name = 'Kadaluarsa'
                elif i.kondisi_id in [3, 4]:
                    kondisi_obj = kondisi.get(id=i.kondisi_id)
                    bg = kondisi_obj.badge
                    name = kondisi_obj.nama
                else:
                    continue
                sdp_data.append({'obj': i, 'bg': bg, 'name': name})
            except ValueError:  # Handle invalid date format
                print(f"Invalid date format for product: {i}")

        self.hasil = {g.id: [] for g in gender}
        self.diagnosa = []
        
        # Daftar diagnosa diagnosa
        prev_total = {}
        prev_gender = {}
        # Cetak hasil
        for i in diagnosa:
            i.tgl=suspek.filter(diagnosa_id=i.id).values('tanggal')
            last_tanggal = suspek.filter(diagnosa_id=i.id).aggregate(last_date=Max('tanggal'))['last_date']
            
            # Mendapatkan total jumlah suspek untuk diagnosa saat ini pada tanggal terakhir
            i.baru = suspek.filter(diagnosa_id=i.id, tanggal=last_tanggal).count()
           
            # Mendapatkan total jumlah suspek untuk diagnosa saat ini
            i.total = suspek.filter(diagnosa_id=i.id).count()
            
            # Mendapatkan tanggal terakhir dari suspek untuk diagnosa saat ini
            i.tanggal = suspek.filter(diagnosa_id=i).values('tanggal').latest('tanggal')['tanggal']
            
            # Menghitung jumlah total suspek
            i.jumlah = suspek.all().count()
            print(i.tgl)
            # Menghitung persentase untuk diagnosa saat ini
            i.persen = 0 / i.jumlah * 100
            
            # Menentukan tren berdasarkan perbandingan dengan persentase sebelumnya
            if i.id in prev_total:
                if i.total > prev_total[i.id]:
                    trend = 'up'
                elif i.total < prev_total[i.id]:
                    trend = 'down'
                else:
                    trend = 'left'
            else:
                trend = 'up'  # Pada iterasi pertama, anggap tren 'up' jika tidak ada data sebelumnya
    
            # Menambahkan hasil ke dalam daftar diagnosa
            self.diagnosa.append({
                'persen': i.persen,
                'jumlah': i.jumlah,
                'baru': i.baru,
                'tanggal': i.tanggal,
                'total': i.total,
                'label': i.diagnosa,
                'trend': trend,
                

            })
            
            # Memperbarui persentase sebelumnya untuk iterasi berikutnya
            prev_total[i.id] = i.persen
            for j in gender:
                # Loop melalui setiap suspek
                for k in suspek:
                    if j.id == k.gender_id and (k.gender_id, k.diagnosa_id) not in seen:
                        seen.add((k.gender_id, k.diagnosa_id))
                        total_suspek = suspek.all().count()
                        diagnosa_id_counts = suspek.filter(gender_id=k.gender_id, diagnosa_id=k.diagnosa_id,tanggal=k.tanggal).count()
                       
                        last_tanggal = suspek.filter(gender_id=k.gender_id, diagnosa_id=k.diagnosa_id).aggregate(last_date=Max('tanggal'))['last_date']
                        j.baru = suspek.filter(gender_id=k.gender_id, diagnosa_id=k.diagnosa_id, tanggal=last_tanggal).count()
                            
                        persen = 0/ total_suspek * 100
                        if j.id in prev_gender:
                            if total_suspek > prev_gender[j.id]:
                                trend = 'up'
                            elif total_suspek < prev_gender[j.id]:
                                trend = 'down'
                            else:
                                trend = 'left'
                        else:
                            trend = 'up'  # Pada iterasi pertama, anggap tren 'up' jika tidak ada data sebelumnya
                        if diagnosa_id_counts != 0:
                            self.hasil[j.id].append({
                                'gender': k.gender,
                                'baru': j.baru,
                                'label': k.diagnosa,
                                'jumlah': total_suspek,
                                'total': diagnosa_id_counts,
                                'persen': persen,
                                'trend': trend
                            })
                            prev_gender[j.id] = persen
            
        for i in pengelolaan_sdp:  
            data_view = LaporanSdp.objects.filter(jenis=i.id)
            jumlah_masuk = data_view.aggregate(Sum('masuk'))['masuk__sum'] or 0
            jumlah_keluar = data_view.aggregate(Sum('keluar'))['keluar__sum'] or 0
            total = jumlah_masuk - jumlah_keluar
            i.jumlah_masuk = jumlah_masuk
            i.jumlah_keluar = jumlah_keluar
            i.total = total  
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'menu': menu,
            'group': group,
            'user':user,
            'sdp':sdp,
            'suspek': suspek,
            'gender':gender,
            'pengelolaan_sdp': pengelolaan_sdp,
            'keuangan_sdp': keuangan_sdp,
            'data_sdp': data_sdp,
            'exp': exp,
            'nama_tabel': nama_tabel,
            'sdp_data': sdp_data,
            'diagnosa': self.diagnosa,
            'hasil': self.hasil
        }
        return render(request, 'office/dashboard.html', context)
class MenuView(View):    
    def get(self, request):
        user=request.user
        menu,group=get_auth_key(request) 
        group_perm=group.permissions.all()
        check=[perm.codename for perm in group_perm]
        content_type = ContentType.objects.get_for_model(User)
        post_permission = Permission.objects.filter(content_type=content_type)
        perm=[perm.codename for perm in post_permission]
        error_handle=f"untuk {user.first_name} {user.last_name}, Anda tidak bisa mengakses ini"
        if not all(p in check for p in perm):  # Periksa setiap izin secara individual
            context = {
            'menu': menu,
            'group': group,
            'error_handle':error_handle
        }           
            return render(request,'layouts/error/error.html',context)

        context={
            'menu': menu,
            'group': group,
            
            }
        return render(request, 'includes/aside.html', context)

def get_auth_key(request):
    user = request.user
    menu = Menu.objects.all()
    group = Group.objects.get(user=user.id)
    try:
        
        valid_menus = []  # Menyimpan item-menu yang sesuai
        for item in menu:
            if str(group.id) in str(item.group):
                valid_menus.append(item)  # Menambahkan item-menu yang sesuai ke dalam list
        return valid_menus, group
    except Group.DoesNotExist:
        group = None   
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
        print(f'Generated URL: {url}')
        return url
    except Exception as e:
        print(f"Error in generating URL: {e}")
        return '#'
def add_notify(feature, view_name=None, model=None, name_field='name'):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            verb = None
            topik = None

            if request.method == 'POST':
                obj_id = kwargs.get('id', None)
                if obj_id is not None and model is not None:
                    # Fetch the model instance to get the name
                    try:
                        instance = model.objects.get(id=obj_id)
                        topik = getattr(instance, name_field, None)
                    except model.DoesNotExist:
                        pass

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
            elif request.method == 'DELETE':
                verb = 'menghapus'
                obj_id = kwargs.get('id', None)
                if obj_id is not None and model is not None:
                    # Fetch the model instance to get the name
                    try:
                        instance = model.objects.get(id=obj_id)
                        topik = getattr(instance, name_field, None)
                    except model.DoesNotExist:
                        pass
            
            response = func(request, *args, **kwargs)
            
            if request.method in ['POST', 'DELETE']:
                if view_name:
                    url = get_universal_url(view_name, *args, **kwargs)
                else:
                    url = '#'

                print(f"Notification URL: {url}")

                Notifikasi.objects.create(
                    fitur=feature,
                    verb=verb,
                    user=user.first_name if user else '',
                    url=url,
                    nama=topik,  # Add the name of the instance
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
    group_perm = group.permissions.all()
    check = [perm.codename for perm in group_perm]
    content_type = ContentType.objects.get_for_model(User)
    post_permission = Permission.objects.filter(content_type=content_type)
    perm = [perm.codename for perm in post_permission]
    error_handle = f"untuk {user.first_name} {user.last_name}, Anda tidak bisa mengakses ini"
    
    if not all(p in check for p in perm):  # Periksa setiap izin secara individual
        context = {
            'menu': menu,
            'group': group,
            'error_handle': error_handle
        }           
        return render(request, 'layouts/error/error.html', context)

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