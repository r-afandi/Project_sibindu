from typing import Any
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ..models.m_about import About
from ..forms.f_about import FormAbout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ...decorator import auth_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ...views import add_notify
from ...models import Notifikasi

decorators = [login_required,auth_required(required_permissions=['view_about', 'add_about', 'change_about', 'delete_about'], model_class=About)]


@method_decorator(decorators, name='dispatch')
class AboutView(View):
    def get(self, request):
        user=request.user
        about = About.objects.get(id=1)
        form = FormAbout(instance=about)
        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'form': form,
            'menu': request.menu,
            'groups': request.groups,
        }
        return render(request, 'office/about/data_about.html', context)

@method_decorator(decorators, name='dispatch')
class UpdateAbout(View):
    def post(self, request,id=1):
        about = About.objects.get(id=id)
        form = FormAbout(request.POST,instance=about)
        if form.is_valid():
            form.save()
            return redirect("about:about")
        else:
        # Handle form validation errors here
            context = {
                'form': form,
            } 
        return render(request, 'office/about/data_about.html', context)