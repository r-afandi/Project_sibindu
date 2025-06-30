from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            # Mendapatkan grup pengguna pengguna saat ini
            groups = Group.objects.filter(user=user)
            # Mendapatkan level tertinggi dari semua grup pengguna
            highest_level = max([group.groups for group in groups])
            request.session['user_level'] = highest_level
        else:
            request.session['user_level'] = None
