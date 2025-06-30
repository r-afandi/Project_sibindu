from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ..posbindu.models.data_suspek.m_data_suspek import DataSuspek
from ..models import Menu
from .forms import FormRegistrasi, FormGejalaLuar,FormGejalaDalam
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class RegistrasiView(View):
    
    def get(self, request):
        data = DataSuspek.objects.all()
        menu = Menu.objects.all()

        context = {
            'data': data,
            'menu': menu,
        }
        return render(request, 'home/dump/dump_list.html', context)
class AddRegistrasiView(View):
    def post(self, request):
        form = FormRegistrasi(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        return render(request, 'home/dump/add_dump.html', {'form': form})
    


class EditDumpView(View):
    def get(self, request, id):
        dump = get_object_or_404(Dump, id=id)
        return render(request, 'home/dump/edit_dump.html', {'dump': dump})

class UpdateDumpView(View):
    def post(self, request, id):
        dump = get_object_or_404(Dump, id=id)
        form = FormSelectDump(request.POST, instance=dump)
        if form.is_valid():
            form.save()
            return redirect("/dump")
        return render(request, 'home/dump/edit_dump.html', {'form': form})
class DeleteDumpView(View):
    def post(self, request, id):
        dump = get_object_or_404(Dump, id=id)
        dump.delete()
        return redirect("/dump")



class AddGejalaLuarView(View):
    def post(self, request):
        form = FormGejalaLuar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        return render(request, 'home/dump/add_dump.html', {'form': form})
class AddGejalaDalamView(View):
    def post(self, request):
        form = FormGejalaDalam(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
        return render(request, 'home/dump/add_dump.html', {'form': form})



