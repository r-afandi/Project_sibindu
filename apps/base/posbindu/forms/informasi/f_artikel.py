from ...models.informasi.m_artikel import Artikel
from ...models.laporan.m_laporan_sdp import Validasi
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.shortcuts import render

class FormArtikel(forms.ModelForm):
    judul = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tanggal = forms.CharField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    artikel = forms.Field(widget=forms.Textarea(attrs={'class': 'form-control'}))
    gambar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'img-pond '}))
    upload= forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    info= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    validasi= forms.ModelChoiceField(queryset=Validasi.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    validator=forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    petugas=forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Artikel
        exclude = ['id','deleted_at']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)       
        self.helper = FormHelper()
        self.acess_field()
        self.helper.form_tag = True
        for field in self.fields:
            self.fields[field].required = False
        self.fields['gambar'].required = False
        # ... rest of your code ...
                            
    def acess_field(self, group_id=None):
        self.user = self.request.user
        group_ids = list(self.user.groups.values_list('id', flat=True))  # Ambil semua ID grup

        if 3 in group_ids and 4 in group_ids:
            # Jika keduanya ada, tampilkan semua kecuali petugas_id dan validator
            for field in self.fields:
                self.fields[field].widget.attrs['style'] = ''  # Menampilkan semua field
        else:
            if 3 in group_ids:
                # Tampilkan 'validasi' dan 'info'
                self.fields['validasi'].widget.attrs['style'] = ''
                self.fields['info'].widget.attrs['style'] = ''
                for field in self.fields:
                    if field not in ['validasi', 'info']:
                        # Sembunyikan field menggunakan HiddenInput dan set nilai awalnya
                        self.fields[field].widget = forms.HiddenInput()
                        if self.instance:
                            self.fields[field].initial = getattr(self.instance, field)
            else:
                # Sembunyikan 'validasi' dan 'info'
                self.fields['validasi'].widget = forms.HiddenInput()
                self.fields['info'].widget = forms.HiddenInput()
