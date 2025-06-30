
from ..models.m_about import About
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
  
class FormAbout(forms.ModelForm):
    nama = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    alamat = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    maps= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tentang = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    tentang_footer = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = About
        exclude=['id']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'