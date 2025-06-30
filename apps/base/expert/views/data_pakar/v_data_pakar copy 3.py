from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.core.cache import cache
from ...models.m_kepakaran import Diagnosa, Pakar,Gejala
from ....views import get_auth_key
from ...forms.data_pakar.f_data_pakar import FormPakar
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ....views import add_notify
from ....models import Notifikasi
import pandas as pd
import numpy as np
import joblib
@method_decorator([login_required, add_notify(feature='Data Pakar')], name='dispatch')

class PakarListView(View):
    def get(self, request):
        user = request.user
        data = cache.get('data_pakar')
        
        if not data:
            data = Pakar.objects.only('id', 'umur', 'data_gejala', 'data_khusus', 'diagnosa').select_related('diagnosa')
            data = list(data)  # Convert queryset to list
            cache.set('data_pakar', data, timeout=60*15)  # Cache selama 15 menit

        menu, group = get_auth_key(request)
        group_perm = group.permissions.all()
        check = [perm.codename for perm in group_perm]
        content_type = ContentType.objects.get_for_model(Pakar)
        post_permission = Permission.objects.filter(content_type=content_type)
        perm = [perm.codename for perm in post_permission]
        error_handle = f"untuk {user.first_name} {user.last_name}, Anda tidak bisa mengakses ini"
        
        if not all(p in check for p in perm):  # Periksa setiap izin secara individual
            context = {
                'menu': menu,
                'group': group,
                'error_handle': error_handle
            }
            return render(request, 'layouts/error/error.html', context)

        nama_tabel = Gejala.objects.filter(jenis__in=['data_gejala', 'data_khusus']).only('id', 'jenis')
        

        for item in data:
            item.gejala = (item.data_gejala + "," + item.data_khusus).split(",")

        notifications = Notifikasi.objects.filter(is_deleted=False).exclude(read_by=user).order_by('-created_at')
        jumlah = notifications.count()

        context = {
            'notifications': notifications,
            'jumlah': jumlah,
            'data': data,
            'menu': menu,
            'group': group,
            'nama_tabel': nama_tabel,
        }
        return render(request, 'expert/data_pakar/data_pakar.html', context)

    def post(self, request):
        # Handle form submission for POST requests
        form = FormPakar(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another appropriate view
            return redirect("data_pakar:data_pakar")
        # If the form is not valid, re-render the form page with errors
        return render(request, 'expert/data_pakar/add_pakar.html')


    def post(self, request, id):
        pakar = get_object_or_404(Pakar, id=id)
        form = FormPakar(request.POST, instance=pakar)
        if form.is_valid():
            form.save()
            return redirect("data_pakar:data_pakar")
        return render(request, 'expert/data_pakar/edit_pakar.html', {'form': form})

def generate_continuous_data(mean, std, size):
    return np.random.normal(mean, std, size)

def convert_to_binary(data, threshold):
    return (data > threshold).astype(int)

def diagnose(row, diabetes_criteria_columns, medication_criteria_columns, lifestyle_criteria_columns):
    diabetes_criteria = [row[col] for col in diabetes_criteria_columns]
    medication_criteria = [row[col] for col in medication_criteria_columns]
    lifestyle_criteria = [row[col] for col in lifestyle_criteria_columns]

    # Ensure Pot Belly and Obesity relationship
    if row["obesitas"] == 1:
        row["perut_buncit"] = 1
    if row["perut_buncit"] == 1:
        row["obesitas"] = 0

    # Check for Diabetes
    if sum(diabetes_criteria) == 4 or sum(diabetes_criteria) == 3 and row["pernah_diabetes"] == 1:
        if row["uwl"] == 1:
            if row["perut_buncit"] == 0 and row["obesitas"] == 0:
                return 1  # Diabetes
        else:
            return 1  # Diabetes

    # Check for Prediabetes
    if sum(diabetes_criteria) < 3 and row["pernah_diabetes"] == 1:
        if row["uwl"] == 1:
            if row["perut_buncit"] == 0 and row["obesitas"] == 0:
                return 2  # Prediabetes
        if all(x == 1 for x in medication_criteria):
            if sum(lifestyle_criteria) > 4:
                return 2  # Prediabetes

    # Check for Normal
    if all(x == 0 for x in diabetes_criteria) and all(x == 0 for x in medication_criteria):
        if sum(lifestyle_criteria) < 4:
            return 3  # Normal

class GenerateDummyDataView(View):
    filepath="naive_bayes_model.joblib"
    def load_model(self, filepath):
        return joblib.load(filepath)

    def dump_model(self, model, filepath):
        joblib.dump(model, filepath)
    def get(self, request, *args, **kwargs):

        data_gejala = Gejala.objects.filter(jenis='data_gejala').values_list('alias', flat=True)
        data_khusus = Gejala.objects.filter(jenis='data_khusus').values_list('alias', flat=True)

        diabetes_criteria_columns = ["polidipsi", "polifagi", "poliuri", "uwl"]
        medication_criteria_columns = list(data_khusus)
        lifestyle_criteria_columns = [col for col in data_gejala if col not in diabetes_criteria_columns]

        columns = diabetes_criteria_columns + medication_criteria_columns + lifestyle_criteria_columns + ["pernah_diabetes", "Diagnosa"]

        # Generate continuous data
        size = 10000  # Increase initial size to ensure enough data for each category
        continuous_features = ["polidipsi", "polifagi", "poliuri", "uwl"]
        data_continuous = {col: generate_continuous_data(0, 1, size) for col in continuous_features}

        # Convert continuous data to binary
        thresholds = {col: 0 for col in continuous_features}  # Set threshold at 0 for simplicity
        data_binary = {col: convert_to_binary(data_continuous[col], thresholds[col]) for col in continuous_features}

        # Generate binary data for the remaining features
        binary_features = [col for col in columns[:-1] if col not in continuous_features]
        data_binary.update({col: np.random.randint(0, 2, size) for col in binary_features})

        # Combine continuous and binary data into one DataFrame
        data = pd.DataFrame(data_binary)

        # Apply the diagnosis function
        data["Diagnosa"] = data.apply(diagnose, axis=1, args=(diabetes_criteria_columns, medication_criteria_columns, lifestyle_criteria_columns))

        # Print distribution of diagnoses to ensure we have enough of each category
        print(data['Diagnosa'].value_counts())

        # Balance the dataset
        df_diabetes = data[data["Diagnosa"] == 1].sample(n=333, replace=True)
        df_prediabetes = data[data["Diagnosa"] == 2].sample(n=333, replace=True)
        df_normal = data[data["Diagnosa"] == 3].sample(n=334, replace=True)

        # Combine and shuffle
        df_balanced = pd.concat([df_diabetes, df_prediabetes, df_normal]).sample(frac=1).reset_index(drop=True)
        # delete pakar
        Pakar.objects.all().delete()
        

        # Loop untuk memproses setiap baris dan menyimpan data ke dalam list
        for index, row in df_balanced.iterrows():
            data_khusus_dict = {col: row[col] for col in medication_criteria_columns}
            data_gejala_dict = {col: row[col] for col in lifestyle_criteria_columns + diabetes_criteria_columns}
            data_pakar = Pakar(
            umur=np.random.randint(20, 70),  # Anda dapat mengganti dengan data umur yang sesuai
            data_khusus=','.join(f"{value}" for i,value in data_khusus_dict.items()),
            data_gejala=','.join(f"{value}" for i,value in data_gejala_dict.items()),
            diagnosa_id=row['Diagnosa']
        )
            
            data_pakar.save()


        # Render the data to template or return a response
        return render(request, 'expert/data_pakar/data_pakar.html', {'data': df_balanced.head()})
    

@method_decorator([login_required, add_notify(feature='Data Pakar')], name='dispatch')
class DeletePakarView(View):
    def post(self, request, id):
        pakar = get_object_or_404(Pakar, id=id)
        pakar.delete()
        return redirect("data_pakar:data_pakar")