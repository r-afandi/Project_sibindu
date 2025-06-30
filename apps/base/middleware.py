import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from .models import Menu

logger = logging.getLogger(__name__)

class AuthMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Retrieve required permissions and model class from view_func
        required_permissions = getattr(view_func, 'required_permissions', None)
        model_class = getattr(view_func, 'model_class', None)

        # Debug prints to check the state
        print('Processing view:', view_func.__name__)
        print('required_permissions:', required_permissions)
        print('model_class:', model_class)

        if not request.user.is_authenticated:
            print('User is not authenticated')
            return None  # Let other authentication middleware handle this

        # If no required permissions or model class, proceed as normal
        if not required_permissions or not model_class:
            print('No required permissions or model class')
            return None

        try:
            valid_menus, group = get_auth_key(request)
            print('valid_menus:', valid_menus)
            print('group:', group)

            if group:
                group_permissions = group.permissions.all()
                group_perm_codenames = [perm.codename for perm in group_permissions]
                content_type = ContentType.objects.get_for_model(model_class)
                post_permission = Permission.objects.filter(content_type=content_type, codename__in=required_permissions)
                perm_codenames = [perm.codename for perm in post_permission]
                print('group_permission',group_permissions)
                print('group_perm_codenames',group_perm_codenames)
                print('content_type',content_type)
                print('post_permission',post_permission)
                print('perm_codenames',perm_codenames)

                if not all(perm in group_perm_codenames for perm in perm_codenames):
                    error_handle = f"Untuk {request.user.first_name} {request.user.last_name}, Anda tidak memiliki akses ini"
                    print('error_handle',error_handle)
                    context = {
                        'menu': valid_menus,
                        'group': group,
                        'error_handle': error_handle
                    }
                    return render(request, 'layouts/error/error.html', context)

                request.menu = valid_menus
                request.group = group
                request.group_permissions = group_permissions
                print('request.menu',request.menu)
                print('request.group',request.group)
                print('request.group_permissions',request.group_permissions)
            else:
                # Handle case when group is not found
                error_handle = f"Untuk {request.user.first_name} {request.user.last_name}, grup tidak ditemukan"
                context = {
                    'menu': valid_menus,
                    'error_handle': error_handle
                }
                return render(request, 'layouts/error/error.html', context)

        except Exception as e:
            logger.error(f"Error in AuthMiddleware: {e}", exc_info=True)
            print('Error:', e)
            raise e

        return None

def get_auth_key(request):
    user = request.user
    menu = Menu.objects.all()
    try:
        group = Group.objects.get(user=user)
        valid_menus = [item for item in menu if str(group.id) in str(item.group)]
        print('valid_menus:', valid_menus)
        print('group:', group)
        return valid_menus, group
    
    except Group.DoesNotExist:
        return [], None




    