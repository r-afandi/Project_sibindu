from apps.base import required
from ...models.m_kepakaran import Diagnosa, Gejala,TipePenyakit,StatusPenyakit
from ....posbindu.models.laporan.m_laporan_sdp import Validasi
from crispy_forms.helper import FormHelper
from django import forms
from django.db.models import Case, When, IntegerField
from django.db.models import Max,Min
class FormDiagnosa(forms.ModelForm):
    kode=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    tipe=forms.ModelChoiceField(required=False,queryset=TipePenyakit.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    status=forms.ModelChoiceField(required=False,queryset=StatusPenyakit.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    diagnosa=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    penanganan=forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = Diagnosa
        exclude=['data_gejala','data_luar', 'data_dalam','data_khusus','kode','created_at','updated_at']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = False

        gejala_fields = Gejala.objects.only('id','nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_label = gejala_field.nama
            widget_attrs = {'class': 'form-control'}
            if gejala_field.jenis in ['data_gejala','data_khusus']:
                #self.fields[field_name] = forms.ModelChoiceField(required=False, queryset=Validasi.objects.all(), widget=forms.Select(attrs={'class': 'form-control select'}))
                self.fields[field_name] = forms.ChoiceField(label=field_label,required=False, choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs))
            else:
                self.fields[field_name] = forms.CharField(required=False, label=field_label, widget=forms.TextInput(attrs=widget_attrs))

    def clean(self):
        cleaned_data = super().clean()

        gejala_fields = Gejala.objects.only('id','nama', 'alias').annotate(
                jenis_order=Case(
                    When(jenis='data_gejala', then=0),
                    When(jenis='data_khusus', then=1),
                    When(jenis='data_luar', then=2),
                    When(jenis='data_dalam', then=3),
                    output_field=IntegerField(),
                )
            ).order_by('jenis_order')
        instance = self.instance
        instance.data_gejala = []
        instance.data_khusus = []
        instance.data_luar = []
        instance.data_dalam = []

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias

            if gejala_field.jenis in ['data_gejala']:
                instance.data_gejala.append(int(cleaned_data.get(field_name, 0)))
            elif gejala_field.jenis in ['data_khusus']:
                instance.data_khusus.append(int(cleaned_data.get(field_name, 0)))
            elif gejala_field.jenis in ['data_luar']:
                instance.data_luar.append(float(cleaned_data.get(field_name, 0)))
            else:
                instance.data_dalam.append(float(cleaned_data.get(field_name, 0)))

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            for field in ['data_gejala','data_khusus','data_luar', 'data_dalam']:
                setattr(instance, field, ','.join(map(str, getattr(instance, field))))

            instance.save()

class FormGejala(forms.ModelForm):
    
    class Meta:
        model =Gejala
        exclude=['id'] 
        widgets = {   
            'nama': forms.TextInput(attrs={'class': 'form-control'}),  
            'alias': forms.TextInput(attrs={'class': 'form-control'}),        
            'jenis': forms.Select(attrs={'class': 'form-control'}, choices=[("", "Pilih"),("data_gejala", "Data Gejala"),("data_luar", "Data Luar"), ("data_dalam", "Data Dalam"),("data_khusus", "Data Khusus")]),
            
            
    }  


# template.html

