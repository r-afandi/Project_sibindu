from urllib import request
from ...models.laporan.m_laporan_sdp import LaporanSdp,DataSdp,Kondisi,Validasi
from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User,Group
   
class FormLapSdp(forms.ModelForm):
    nama = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    jenis=forms.ModelChoiceField(queryset=DataSdp.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    tanggal = forms.Field(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    kadaluarsa = forms.Field(widget=forms.DateInput(attrs={'class': 'form-control'}))
    masuk = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    keluar = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bukti = forms.Field(widget=forms.FileInput(attrs={'class': 'all-pond '}))
    upload = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    keperluan = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))    
    validasi= forms.ModelChoiceField(queryset=Validasi.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    info= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    validator=forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    petugas=forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    class Meta:
        model = LaporanSdp
        exclude=['id','kode','deleted_at']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)       
        self.helper = FormHelper()
        self.acess_field()
        self.helper.form_tag = True
        for field in self.fields:
            self.fields[field].required = False
                    
    def acess_field(self, group_id=None):
        self.user = self.request.user
        group_ids = list(self.user.groups.values_list('id', flat=True))  # Ambil semua ID grup

        if 3 in group_ids and 4 in group_ids:
            # Jika keduanya ada, tampilkan semua kecuali petugas_id dan validator
            for field in self.fields:
                if field in self.fields:
                    self.fields[field].widget.attrs['style'] = ''
        else:
            if 3 in group_ids:
                # Tampilkan 'validasi' dan 'info'
                self.fields['validasi'].widget.attrs['style'] = ''
                self.fields['info'].widget.attrs['style'] = ''
                for field in self.fields:
                    if field not in ['validasi', 'info']:
                        self.fields[field].widget = forms.HiddenInput()
            else:
                # Sembunyikan 'validasi' dan 'info' menggunakan HiddenInput
                self.fields['validasi'].widget = forms.HiddenInput()
                self.fields['info'].widget = forms.HiddenInput()

class FormSdp(forms.ModelForm):
    kode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nama = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    satuan = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    info = forms.CharField(label='informasi',widget=forms.Textarea(attrs={'class': 'form-control'}))    

    class Meta:
        model = DataSdp
        exclude=['id','produk','kondisi','jumlah_masuk','jumlah_keluar','total','kadaluarsa','deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.helper = FormHelper()
        self.helper.form_tag = True
        for field in self.fields:
            self.fields[field].required = False
