import os
from ...models.informasi.m_pengumuman import Pengumuman, TipePengumuman
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User,Group



class FormPengumuman(forms.ModelForm):
    judul = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenis = forms.ModelChoiceField(queryset=TipePengumuman.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    tanggal = forms.Field(widget=forms.DateInput(attrs={'class': 'form-control'}))
    waktu = forms.Field(widget=forms.TimeInput(attrs={'class': 'form-control'}))
    tempat = forms.Field(widget=forms.TextInput(attrs={'class': 'form-control'}))
    pengumuman = forms.Field(widget=forms.Textarea(attrs={'class': 'form-control'}))
    petugas=forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Pengumuman
        exclude=['id','deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        for field in self.fields:
            self.fields[field].required = False