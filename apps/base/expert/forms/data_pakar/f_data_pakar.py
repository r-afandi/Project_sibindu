from django import forms
from crispy_forms.helper import FormHelper
from django.db.models import Case, When, IntegerField
from ...models.m_kepakaran import Kepakaran,Diagnosa,Gejala

class FormPakar(forms.ModelForm):
    umur=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Kepakaran
        exclude=['id','data_gejala', 'data_luar', 'data_dalam','data_khusus','diagnosa_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = False

        gejala_fields = Gejala.objects.only('id', 'nama', 'alias','jenis').annotate(
            jenis_order=Case(
                When(jenis='data_gejala', then=0),
                When(jenis='data_khusus', then=1),
                default=2,  # Menambahkan default untuk nilai lain
                output_field=IntegerField(),
            )
        ).filter(jenis_order__lt=2).order_by('jenis_order')

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_label = gejala_field.alias
            widget_attrs = {'class': 'form-control'}       
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs))

    def clean(self):
        cleaned_data = super().clean()
        gejala_fields = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).only('id','nama', 'alias', 'jenis')
        instance = self.instance

        # Hapus data gejala sebelumnya
        instance.data_gejala = ''
        instance.data_khusus = ''

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias

            gejala_data = cleaned_data.get(field_name)

            # Periksa apakah data gejala kosong
            if not gejala_data:
                # Jika kosong, lewati dan lanjut ke iterasi berikutnya
                continue

            # Tambahkan data gejala ke string
            if gejala_field.jenis == 'data_gejala':
                instance.data_gejala += str(int(gejala_data)) + ','
            else:
                instance.data_khusus += str(int(gejala_data)) + ','

        # Hapus koma terakhir
        instance.data_gejala = instance.data_gejala[:-1]
        instance.data_khusus = instance.data_khusus[:-1]

        return cleaned_data

    
class FormKepakaran(forms.ModelForm):
    umur=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    alasan=forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta:
        model = Kepakaran
        exclude=['id','data_gejala', 'data_luar', 'data_dalam','data_khusus','diagnosa_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = False

        gejala_fields = Gejala.objects.only('id', 'nama', 'alias','jenis').annotate(
            jenis_order=Case(
                When(jenis='data_gejala', then=0),
                When(jenis='data_khusus', then=1),
                default=2,  # Menambahkan default untuk nilai lain
                output_field=IntegerField(),
            )
        ).filter(jenis_order__lt=2).order_by('jenis_order')
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_label = gejala_field.nama
            widget_attrs = {'class': 'form-control'}       
            self.fields[field_name] = forms.ChoiceField(label=field_label, choices=[(1, 'Ya'), (2, 'Tidak')], widget=forms.Select(attrs=widget_attrs))

    def clean(self):
        cleaned_data = super().clean()
        gejala_fields = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).only('id','nama', 'alias', 'jenis')
        instance = self.instance

        # Hapus data gejala sebelumnya
        instance.data_gejala = ''
        instance.data_khusus = ''

        for gejala_field in gejala_fields:
            field_name = gejala_field.alias

            gejala_data = cleaned_data.get(field_name)

            # Periksa apakah data gejala kosong
            if not gejala_data:
                # Jika kosong, lewati dan lanjut ke iterasi berikutnya
                continue

            # Tambahkan data gejala ke string
            if gejala_field.jenis == 'data_gejala':
                instance.data_gejala += str(int(gejala_data)) + ','
            else:
                instance.data_khusus += str(int(gejala_data)) + ','

        # Hapus koma terakhir
        instance.data_gejala = instance.data_gejala[:-1]
        instance.data_khusus = instance.data_khusus[:-1]

        return cleaned_data

    