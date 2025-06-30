
from ..posbindu.models.data_suspek.m_data_suspek import DataSuspek
from django import forms

  
class FormRegistrasi(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = "__all__" 
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
        }
class FormGejalaLuar(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = "__all__" 
        widgets = {
            'gejala_luar': forms.TextInput(attrs={'class': 'form-control'}),
        }
class FormGejalaDalam(forms.ModelForm):
    class Meta:
        model = DataSuspek
        fields = "__all__" 
        widgets = {
            'gejala_dalam': forms.TextInput(attrs={'class': 'form-control'}),
        }