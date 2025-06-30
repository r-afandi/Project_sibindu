import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import joblib
from apps.base.expert.models.m_kepakaran import Pakar

class NB_Trainer:
    @classmethod
    def train_model_and_evaluate(cls):
        # Ambil data dari database
        data_pakar = Pakar.objects.all()

        # Ubah data menjadi dataframe
        df = pd.DataFrame(list(data_pakar.values()))
        print(df)

        # Preprocessing data
        # Konversi string ke list
        df['data_luar'] = df['data_luar'].apply(lambda x: list(map(float, x.split(','))))
        df['data_dalam'] = df['data_dalam'].apply(lambda x: list(map(float, x.split(','))))
        df['diagnosa_id'] = df['diagnosa_id'].apply(lambda y: [int(y)] if isinstance(y, int) else list(map(int, y.split(','))))

        # Gabungkan fitur data_luar dan data_dalam
        df['combined_data'] = df.apply(lambda row: row['data_luar'] + row['data_dalam'], axis=1)
        # Ambil fitur dan target
      
        X = np.array(df['combined_data'].tolist())
        y = np.array(df['diagnosa_id'].tolist())

        # Bagi data menjadi data latih dan data uji
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Inisialisasi model
        model = GaussianNB()

        # Latih model
        model.fit(X_train, y_train)

        # Prediksi menggunakan data uji
        y_pred = model.predict(X_test)

        # Evaluasi model
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        # Simpan model
        joblib.dump(model, 'naive_bayes_model.joblib')
