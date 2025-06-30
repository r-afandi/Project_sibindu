# machine_learning.py
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from ..expert.models.m_kepakaran import Pakar
import pandas as pd
import joblib

def load_data():
    """Membaca data pelatihan dari database Django dan mengonversinya ke format numerik."""
    data_pelatihan = Pakar.objects.values('data_gejala', 'data_khusus', 'diagnosa')
    data = pd.DataFrame(data_pelatihan)
    
    # Konversi kolom 'data_gejala' dan 'data_khusus' dari string ke list float
    data['data_gejala'] = data['data_gejala'].apply(lambda x: list(map(float, x.split(','))))
    data['data_khusus'] = data['data_khusus'].apply(lambda x: list(map(float, x.split(','))))
    
    # Gabungkan kolom 'data_gejala' dan 'data_khusus' menjadi satu list untuk setiap baris
    data['features'] = data.apply(lambda row: row['data_gejala'] + row['data_khusus'], axis=1)
    
    return data[['features', 'diagnosa']]

def split_data(data):
    """Membagi data menjadi data pelatihan dan data validasi."""
    X = pd.DataFrame(data['features'].tolist())
    y = data['diagnosa']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    """Melatih model Gaussian Naive Bayes."""
    model = GaussianNB()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_val, y_val):
    """Menguji model dengan data validasi."""
    accuracy = model.score(X_val, y_val)
    return accuracy

def save_model(model):
    """Menyimpan model ke dalam file."""
    joblib.dump(model, 'naive_bayes_model.joblib')

def load_model():
    """Memuat model dari file."""
    return joblib.load('naive_bayes_model.joblib')

def predict_diagnosis(features):
    """Memperkirakan diagnosa dan menampilkan probabilitas untuk setiap kelas."""
    model = load_model()
    probs = model.predict_proba([features])
    classes = model.classes_
    
    result = {}
    for class_idx, class_label in enumerate(classes):
        result[class_label] = probs[0][class_idx]
    
    return result

# Contoh penggunaan
if __name__ == "__main__":
    data = load_data()
    X_train, X_val, y_train, y_val = split_data(data)
    model = train_model(X_train, y_train)
    save_model(model)
    
    accuracy = evaluate_model(model, X_val, y_val)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Contoh fitur untuk prediksi
    example_features = X_val.iloc[0].tolist()
    prediction = predict_diagnosis(example_features)
    print("Prediction probabilities per diagnosis:", prediction)
