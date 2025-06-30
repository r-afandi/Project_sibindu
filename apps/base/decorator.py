from functools import wraps
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Menu, Group, Notifikasi

def auth_required(required_permissions=None, model_class=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return login_required(view_func)(request, *args, **kwargs)
            # Dapatkan menu valid dan grup pengguna
            valid_menus, groups = get_auth_key(request)
            
            if groups:
                all_group_permissions = set()
                for group in groups:
                    group_permissions = group.permissions.all()
                    group_perm_codenames = [perm.codename for perm in group_permissions]
                    all_group_permissions.update(group_perm_codenames)

                if model_class and required_permissions:
                    content_type = ContentType.objects.get_for_model(model_class)
                    post_permission = Permission.objects.filter(content_type=content_type, codename__in=required_permissions)
                    perm_codenames = [perm.codename for perm in post_permission]

                    if not all(perm in all_group_permissions for perm in perm_codenames):
                        error_handle = f"{request.user.first_name} {request.user.last_name}, Anda tidak memiliki akses ini"
                        print('error_handle:', error_handle)
                        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=request.user).order_by('-created_at')
                        jumlah = notifications.count()

                        context = {
                            'notifications': notifications,
                            'jumlah': jumlah, 
                            'menu': valid_menus,
                            'error_handle': error_handle
                        }
                        return render(request, 'layouts/error/error.html', context)
                request.menu = valid_menus  # Pastikan tidak ada duplikat
                request.groups = groups
                request.group_permissions = all_group_permissions
            else:
                error_handle = f"{request.user.first_name} {request.user.last_name}, Anda tidak masuk dalam role apapun. Silahkan hubungi Admin"
                print('error_handle:', error_handle)
                context = {
                    'menu': valid_menus,
                    'error_handle': error_handle
                }
                return render(request, 'layouts/error/error.html', context)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def get_auth_key(request):
    user = request.user
    menu = Menu.objects.all()
    
    groups = list(Group.objects.filter(user=user))
    valid_menus = set()

    for group in groups:
        group_menus = [item for item in menu if str(group.id) in str(item.group)]
        valid_menus.update(group_menus)
    
    return list(valid_menus), groups
