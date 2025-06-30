from dataclasses import fields
from urllib import request
from ...models.data_suspek.m_data_suspek import DataSuspek, Gender
from ...models.laporan.m_laporan_sdp import Validasi
from ....expert.models.m_kepakaran import Gejala, Diagnosa
from ...models.informasi.m_pengumuman import Pengumuman
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from django.core.cache import cache
from crispy_forms.layout import Layout, Row, Column, Field, HTML, ButtonHolder, Submit
from datetime import datetime
from django.db.models import Case, When, IntegerField
from django.db.models import Max,Min
class FormDataSuspek(forms.ModelForm):
    
    #nik = forms.ModelChoiceField(label='NIK',queryset=DataSuspek.objects.only('id', 'nik'),required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select-bs4'}))
    nik = forms.CharField(label='NIK',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tanggal = forms.Field(label='Pelaksanaan', required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    nama = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ModelChoiceField(label='Jenis Kelamin', queryset=Gender.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    umur = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    alamat = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    diagnosa = forms.ModelChoiceField(queryset=Diagnosa.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    petugas = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.HiddenInput(attrs={'class': 'form-control', 'disabled': 'true'}))
    class Meta:
        model = DataSuspek
        exclude = ['data_gejala', 'data_khusus', 'data_luar', 'data_dalam', 'penanganan', 'deleted_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = False

        gejala_fields = cache.get('gejala_fields')
        if not gejala_fields:
            gejala_fields = list(Gejala.objects.only('id','nama', 'alias', 'jenis'))
            cache.set('gejala_fields', gejala_fields, timeout=60*15)

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias  # Gantilah dengan nama atribut yang sesuai
            field_label = gejala_field.nama or gejala_field.pernyataan # Gantilah dengan label yang sesuai
            widget_attrs = {'class': 'form-control'}
            if gejala_field.jenis in ['data_gejala','data_khusus']:
                self.fields[field_name] = forms.ChoiceField(required=False,label=f'{field_label}',  choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs)) # type: ignore
            else:    
                self.fields[field_name] = forms.CharField(required=False,label=field_label,widget=forms.TextInput(attrs=widget_attrs)) # type: ignore

    def clean(self):
        cleaned_data = super().clean()
        gejala_fields = cache.get('gejala_fields')
        if not gejala_fields:
            gejala_fields = list(Gejala.objects.only('id','nama', 'alias', 'jenis'))
            cache.set('gejala_fields', gejala_fields, timeout=60*15)

        instance = self.instance
        instance.data_gejala = []
        instance.data_khusus = []
        instance.data_luar = []
        instance.data_dalam = []

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_value = cleaned_data.get(field_name, None)
            if gejala_field.jenis == 'data_gejala':
                instance.data_gejala.append(int(field_value) if field_value else 0)
            elif gejala_field.jenis == 'data_khusus':
                instance.data_khusus.append(int(field_value) if field_value else 0)
            elif gejala_field.jenis == 'data_luar':
                instance.data_luar.append(float(field_value) if field_value else 0.0)
            else:
                instance.data_dalam.append(float(field_value) if field_value else 0.0)

    def save(self, commit=True):
        instance = super().save(commit=False)
        for field in ['data_gejala', 'data_khusus', 'data_luar', 'data_dalam']:
            setattr(instance, field, ','.join(map(str, getattr(instance, field))))
        if commit:
            instance.save()
        return instance
class FormRegistrasi(forms.ModelForm):
    suspek=DataSuspek.objects.only('id', 'nik')
    tanggal = Pengumuman.objects.filter(jenis=1).filter()
    tanggal = tanggal.aggregate(Min('tanggal'))['tanggal__min']
    #nik = forms.ModelChoiceField(label='NIK',queryset=suspek,required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control select-bs4'}))
    nik = forms.CharField(label='NIK',required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    nama= forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    umur= forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    alamat= forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tanggal = forms.CharField(label='Tgl. Pemeriksaan',required=False, initial=tanggal if tanggal else None, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender=forms.ModelChoiceField(label='Jenis Kelamin',queryset=Gender.objects.all(),required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    data_gejala=forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    data_khusus=forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    data_luar=forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    data_dalam=forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DataSuspek
        exclude = ['diagnosa','penanganan','petugas','deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-12'
        self.helper.layout = Layout(
            Row(
                Column('tanggal', css_class='form-group col-lg-12'),       
                Column(
                    Field('nik', css_class='form-control col-lg-12'),
                 
            
                    HTML("""
                    <div class="input-group-append col-lg-3">
                        <button class="btn btn-primary" type="button" id="search-nik">Search</button>
                    </div>
                    """),
                    
                ),
                css_class='form-row'
            ),
            Row(
                Column('nama', css_class='form-group col-lg-12'),
                Column('umur', css_class='form-group col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('alamat', css_class='form-group col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('gender', css_class='form-group col-lg-12'),
                css_class='form-row'
            ),
                        Row(
                Column('data_gejala', css_class='form-group col-lg-6'),
                Column('data_khusus', css_class='form-group col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('data_luar', css_class='form-group col-lg-6'),
                Column('data_dalam', css_class='form-group col-lg-6'),
                css_class='form-row'
            ),
        )

        self.helper.layout.append(
            HTML("""
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Simpan</button>
            </div>
            """)
        )
class FormPelacakanGejala(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = []  # Kosongkan fields karena akan diisi secara dinamis


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = False

        data = Gejala.objects.filter(jenis__in=['data_gejala','data_khusus']).only('id','nama', 'alias', 'jenis')
        for gejala_field in data:
            field_name = gejala_field.alias
            field_label = gejala_field.pernyataan
            widget_attrs = {'class': 'form-control'}
                # self.fields[field_name] = forms.ModelChoiceField(required=False,label=f'{field_label} ?', queryset=Validasi.objects.all(), widget=forms.Select(attrs=widget_attrs),to_field_name='id')
            self.fields[field_name] = forms.ChoiceField(required=False,label=f'{field_label} ?',  choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs))
    def clean(self):
        cleaned_data = super().clean()

        gejala_fields = Gejala.objects.filter(jenis__in=['data_gejala','data_khusus']).only('id','nama', 'alias', 'jenis')
        instance = self.instance
        instance.data_gejala = []
        instance.data_khusus = []

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
           
            if gejala_field.jenis in ['data_gejala']:
                instance.data_gejala.append(int(cleaned_data.get(field_name, 0)))
            else:
                instance.data_khusus.append(int(cleaned_data.get(field_name, 0)))
        instance.data_gejala = [value for value in instance.data_gejala]
        instance.data_khusus = [value for value in instance.data_khusus]
        # Hapus nilai-nilai yang kosong
        instance.data_gejala = list(filter(None, instance.data_gejala))
        instance.data_khusus = list(filter(None, instance.data_khusus))


    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            for field in ['data_gejala','data_khusus']:
                setattr(instance, field, ','.join(map(str, getattr(instance, field))))
                
            instance.save()
    
class FormPengecekanLuar(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = [] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        # Ambil bidang-bidang dari Gejala yang memiliki jenis 'data_luar'
        gejala_fields = Gejala.objects.filter(jenis='data_luar').only('id','nama', 'alias', 'jenis')
        # Tambahkan bidang-bidang dinamis ke formulir
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias  # Gantilah dengan nama atribut yang sesuai
            field_label = gejala_field.nama # Gantilah dengan label yang sesuai
            self.fields[field_name] = forms.CharField(label=field_label,widget=forms.TextInput(attrs={'class': 'form-control'})) # type: ignore
    def clean(self):
        cleaned_data = super().clean()
        gejala_fields = Gejala.objects.filter(jenis='data_luar').only('id','nama', 'alias', 'jenis')
        instance = self.instance
        instance.data_luar = []

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            instance.data_luar.append(str(cleaned_data.get(field_name, 0)))
        # Hapus spasi kosong di awal dan akhir setiap nilai
        instance.data_luar = [value.strip() for value in instance.data_luar]
        # Hapus nilai-nilai yang kosong
        instance.data_luar = list(filter(None, instance.data_luar))
        # Ubah format data
        instance.data_luar = ','.join(instance.data_luar)
        return cleaned_data
class FormPengecekanDalam(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = [] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        # Ambil bidang-bidang dari Gejala yang memiliki jenis 'data_dalam'
        gejala_fields = Gejala.objects.filter(jenis='data_dalam').only('id','nama', 'alias', 'jenis')
        # Tambahkan bidang-bidang dinamis ke formulir
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias  # Gantilah dengan nama atribut yang sesuai
            field_label = gejala_field.nama # Gantilah dengan label yang sesuai
            self.fields[field_name] = forms.CharField(label=field_label,widget=forms.TextInput(attrs={'class': 'form-control'})) # type: ignore
    def clean(self):
        cleaned_data = super().clean()
        gejala_fields = Gejala.objects.filter(jenis='data_dalam').only('id','nama', 'alias', 'jenis')
        instance = self.instance
        instance.data_dalam = []

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            instance.data_dalam.append(str(cleaned_data.get(field_name,0)))
        # Hapus spasi kosong di awal dan akhir setiap nilai
        instance.data_dalam = [value.strip() for value in instance.data_dalam]
        # Hapus nilai-nilai yang kosong
        instance.data_dalam = list(filter(None, instance.data_dalam))
        # Ubah format data
        instance.data_dalam = ','.join(instance.data_dalam)
        return cleaned_data
class FormPenanganan(forms.ModelForm):
    nik= forms.CharField(required=False,label='NIK', widget=forms.TextInput(attrs={'class': 'form-control','readonly': '', 'disabled': 'true'}))
    nama= forms.CharField(required=False,label='Nama', widget=forms.TextInput(attrs={'class': 'form-control','readonly': '', 'disabled': 'true'}))
    petugas= forms.ModelChoiceField(required=False,queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control','readonly': '', 'disabled': 'true'}))
    class Meta:
        model = DataSuspek
        exclude=['umur','alamat','gender','diagnosa','penanganan','tanggal','data_gejala', 'data_khusus', 'data_luar', 'data_dalam', 'deleted_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields= False
        gejala_fields = Gejala.objects.only('id', 'nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                )
            ).order_by('jenis_order')
        
        # Tambahkan bidang-bidang dinamis ke formulir
     
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias  # Gantilah dengan nama atribut yang sesuai
            field_label = gejala_field.nama or gejala_field.pernyataan # Gantilah dengan label yang sesuai
            widget_attrs = {'class': 'form-control', 'readonly': '', 'disabled': 'true'}
            if gejala_field.jenis in ['data_gejala','data_khusus']:
                self.fields[field_name] = forms.ChoiceField(required=False,label=f'{field_label}',  choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs)) # type: ignore
            else:    
                self.fields[field_name] = forms.CharField(required=False,label=field_label,widget=forms.TextInput(attrs=widget_attrs)) # type: ignore

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Tetapkan nilai-nilai yang tidak diubah dari field readonly atau disabled
        instance.nik = self.initial.get('nik', instance.nik)
        instance.nama = self.initial.get('nama', instance.nama)
        instance.petugas_id = self.initial.get('petugas_id', instance.petugas_id)
        if commit:
            instance.save()
        return instance
   