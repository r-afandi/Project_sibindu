from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, Group
from ..forms.f_user import FormUser, FormProfil,FormWilayahKerja
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ...decorator import auth_required
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from ...models import Menu, Group, Notifikasi, WilayahKerja, Satuan
from django.db.models import OuterRef, Subquery
decorators = [login_required, auth_required(required_permissions=['view_user', 'add_user', 'change_user', 'delete_user'], model_class=User)]

# List wilayah kerja
@method_decorator(decorators, name='dispatch')
class WilayahKerjaListView(View):
    def get(self, request):
        data = WilayahKerja.objects.filter(deleted_at__isnull=True)  # Menampilkan hanya yang tidak dihapus
        form = FormWilayahKerja(request.POST)
        context = {
            'data': data,
            'form': form,
        }
        return render(request, 'office/user/data_wilayah_kerja.html', context)

    def post(self, request):
        form = FormWilayahKerja(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:wilayah_kerja')  # Redirect ke list setelah menambah
        context = {
            'form': form,
        }
        return render(request, 'office/user/add_wilayah_kerja.html', context)

# Edit wilayah kerja
@method_decorator(decorators, name='dispatch')
class UpdateWilayahKerjaView(View):
    def get(self, request, id):
        wilayah_kerja = get_object_or_404(WilayahKerja, id=id)
        form = FormWilayahKerja(instance=wilayah_kerja)
        context = {
            'form': form,
            'wilayah_kerja': wilayah_kerja,
        }
        return render(request, 'wilayah_kerja/edit_wilayah_kerja.html', context)

    def post(self, request, id):
        wilayah_kerja = get_object_or_404(WilayahKerja, id=id)
        form = FormWilayahKerja(request.POST, instance=wilayah_kerja)
        if form.is_valid():
            form.save()
            return redirect('user:wilayah_kerja')
        context = {
            'form': form,
            'wilayah_kerja': wilayah_kerja,
        }
        return render(request, 'wilayah_kerja/edit_wilayah_kerja.html', context)

# Hapus wilayah kerja (soft delete)
@method_decorator(decorators, name='dispatch')
class DeleteWilayahKerjaView(View):
    def post(self, request, id):
        wilayah_kerja = get_object_or_404(WilayahKerja, id=id)
        wilayah_kerja.deleted_at = datetime.now()
        wilayah_kerja.save()
        return redirect('user:wilayah_kerja')
@method_decorator(decorators, name='dispatch')
class UserListView(View):
    def get(self, request):
        user = request.user
        data = User.objects.all()
        form = FormUser()
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

        return render(request, 'office/user/data_user.html', context)

    def post(self, request):
        form = FormUser(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            form.instance.password = make_password(password)
            # Simpan form tetapi jangan commit dulu

            user_instance = form.save(commit=False)

            # Simpan user_instance untuk mendapatkan ID
            user_instance.save()

            # Tangani penyimpanan ManyToManyField `groups` secara manual
            groups = form.cleaned_data.get('groups')
            if groups:
                user_instance.groups.set(groups)  # Atur groups ke instance user

            # Redirect setelah menyimpan
            return redirect("user:user")
        else:
            # Jika form tidak valid, tampilkan form lagi dengan error
            context = {
                'form': form,
            }
            return render(request, 'office/user/add_user.html', context)

@method_decorator(decorators, name='dispatch')
class UpdateUserView(View):

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = FormUser(request.POST, instance=user)

        if form.is_valid():
            new_password = form.cleaned_data['password']
            new_groups = form.cleaned_data['groups']

            # Debugging info
            print('Debug: old_password', user.password)
            print('Debug: new_password', new_password)

            # Update groups if changed
            if new_groups != user.groups.all():
                form.instance.groups.set(new_groups)

            # Update password only if it's provided and different from the current one
            if new_password and not check_password(new_password, user.password)and not new_password.startswith('pbkdf2_sha256'):
                form.instance.password = make_password(new_password)  # Hash the new password
                print('Debug: password changed')
            else:
                # Keep the old password if no new password or if the same password is provided
                form.instance.password = user.password
                print('Debug: password not changed')

            # Save the form (includes updated groups, password if changed)
            form.save()
            return redirect("user:user")
        else:
            context = {
                'form': form,
            }
            return render(request, 'office/user/edit_user.html', context)
@method_decorator(decorators, name='dispatch')
class DeleteUserView(View):
    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return redirect("user:user")

class ProfilListView(View):
    def get(self, request):
        user = request.user
        menu = Menu.objects.all()
        
        # Ambil group dari user yang sedang login
        groups = list(Group.objects.filter(user=user))
        valid_menus = set()

        # Filter menu berdasarkan grup yang dimiliki user
        for group in groups:
            group_menus = [item for item in menu if str(group.id) in str(item.group)]
            valid_menus.update(group_menus)

        # Menampilkan semua group (jika memang diperlukan)
        all_groups = Group.objects.all()

        # Ambil notifikasi yang belum dibaca
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        # Jika form diperlukan, inisialisasi form
        form = FormProfil(instance=user)  # Pastikan `FormUser` di-import dan form memang diperlukan di template
        
        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'form': form,  # Pastikan form dipakai jika ada
            'menu': valid_menus,  # Menampilkan menu yang sesuai dengan grup user
            'groups': groups,  # Jika ingin menampilkan semua grup di template
        }

        return render(request, 'office/user/profil.html', context)

    def post(self, request):
        user = request.user
        form = FormProfil(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Store the hashed password
            return redirect("user:profil")
        else:
            context = {
                'form': form,
            }
            return render(request, 'office/user/profil.html', context)

