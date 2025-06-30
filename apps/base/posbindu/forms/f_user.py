from asyncio import FIRST_EXCEPTION
from urllib import request
from django.contrib.auth.models import User,Group
from ...models import WilayahKerja,Satuan
from crispy_forms.helper import FormHelper
from django.contrib.auth.hashers import make_password
from ..user.hasher import hash_password, verify_password
from django import forms

class FormWilayahKerja(forms.ModelForm):
    class Meta:
        model = WilayahKerja
        fields = ['wilayah_kerja']  # Hanya field yang diisi oleh pengguna
        widgets = {
            'wilayah_kerja': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

class FormUser(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        exclude = ['user_permissions', 'last_login', 'is_superuser', 'superuser_status', 'date_joined']
        widgets={
            'groups': forms.SelectMultiple(attrs={'class': 'form-control select2-bs4'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'

class FormProfil(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        exclude=['user_permissions','superuser_status','last_login','groups','is_superuser','is_staff','is_active','date_joined'] 
        widgets={
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'



