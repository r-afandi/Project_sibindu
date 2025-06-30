from django import forms
from .expert.models.m_kepakaran import Diagnosa, Gejala,Kepakaran
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML, ButtonHolder, Submit

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        error_messages={'required': 'Harap isi field ini.'}
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'password-field'}),
        error_messages={'required': 'Harap isi field ini.'}
    )
    remember = forms.BooleanField(
        label='Ingat Saya',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id': 'remember',
            'class': 'form-check-input'
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = '{% url "sibindu:login" %}'
        
        self.helper.layout = Layout(
            HTML("""
                    <div class="mb-3">
                        <label for="id_username" class="form-label">Username</label>
                        <div class="input-group">
                            <input type="text" id="id_username" name="username" class="form-control" placeholder="Username" required>
                            <span class="input-group-text"><i class="fas fa-user"></i></span>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="password-field" class="form-label">Password</label>
                        <div class="input-group">
                            <input type="password" id="password-field" name="password" class="form-control" placeholder="Password" required>
                            <span class="input-group-text" onclick="togglePassword()" style="cursor: pointer;">
                                <i id="password-icon" class="fas fa-eye-slash"></i>
                            </span>
                        </div>
                    </div>
                    
                    <div class="form-check mb-3">
                        <input type="checkbox" class="form-check-input" id="remember" name="remember">
                        <label class="form-check-label" for="remember">Ingat Saya</label>
                    </div>
                    
            """),
            Submit('submit', 'Login', css_class='btn btn-danger btn-block', style='background-color: #A6192E;')
        )
class DiagnosaFc(forms.Form):
    class Meta:
        model = Gejala
        exclude = ['id']  # Kosongkan fields karena akan diisi secara dinamis

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class='form-select'

        # Ambil bidang-bidang dari Gejala yang memiliki jenis 'data_gejala' atau 'data_khusus'
        gejala_fields = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by(
            # Urutkan data gejala terlebih dahulu kemudian data khusus
            '-jenis',
            'id'
        )
        # Tambahkan bidang-bidang dinamis ke formulir 
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_label = gejala_field.pernyataan
            self.fields[field_name] = forms.ChoiceField(
                label=field_label,
                choices=[(1, 'Ya'), (2, 'Tidak')],
                widget=forms.RadioSelect(attrs={'class': 'form-select'}),
               
            )

class FeedbackForm(forms.Form):
    umur=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength':3}), required=True)
    diagnosa_suspek=forms.ModelChoiceField(queryset=Diagnosa.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    alasan=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    diagnosa_sistem=forms.ModelChoiceField(queryset=Diagnosa.objects.all(), required=True, widget=forms.HiddenInput(attrs={'class': 'form-control'} ))

    class Meta:
        model = Kepakaran
        exclude = ['id']  # Kosongkan fields karena akan diisi secara dinamis

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.field_class='form-select'

        # Ambil bidang-bidang dari Gejala yang memiliki jenis 'data_gejala' atau 'data_khusus'
        gejala_fields = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).order_by(
            # Urutkan data gejala terlebih dahulu kemudian data khusus
            '-jenis',
            'id'
        )
        # Tambahkan bidang-bidang dinamis ke formulir 
        for gejala_field in gejala_fields:
            field_name = gejala_field.alias
            field_label = gejala_field.pernyataan
            self.fields[field_name] = forms.CharField(
                label=field_label,
                widget=forms.HiddenInput(attrs={'class': 'form-select'}),
               
            )