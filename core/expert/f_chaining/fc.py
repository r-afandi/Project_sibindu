from apps.base.expert.models.m_kepakaran import Diagnosa  # Mengimpor model Diagnosa dari aplikasi expert
from apps.base.expert.naive_bayes import load_model  # Mengimpor fungsi load_model untuk Naive Bayes
import numpy as np  # Mengimpor numpy untuk manipulasi array
from joblib import load  # Mengimpor fungsi load untuk memuat model machine learning

class Diagnosis:
    def __init__(self, id, kode,status, diagnosa, data_gejala, data_khusus, data_luar, data_dalam, penanganan):
        # Konstruktor untuk inisialisasi objek Diagnosis
        self.id = id
        self.kode = kode
        self.status = status
        self.diagnosa = diagnosa
        self.data_gejala = data_gejala  # Daftar gejala dalam bentuk list integer
        self.data_khusus = data_khusus  # Daftar faktor khusus dalam bentuk list integer
        self.data_luar = data_luar  # Data luar seperti antropometri (list float)
        self.data_dalam = data_dalam  # Data dalam seperti biomarker (list float)
        self.penanganan = penanganan  # Penanganan yang direkomendasikan

    @staticmethod
    def load_diagnoses():
        # Memuat semua data diagnosis dari basis data
        diagnoses = []  # Daftar diagnosis
        for d in Diagnosa.objects.all():
            # Iterasi setiap diagnosis di basis data
            diagnoses.append(Diagnosis(
                id=d.id,
                kode=d.kode,
                status=d.status,
                diagnosa=d.diagnosa,
                data_gejala=[int(x) for x in d.data_gejala.split(',') if x],  # Konversi string ke list integer
                data_khusus=[int(x) for x in d.data_khusus.split(',') if x],  # Konversi string ke list integer
                data_luar=[float(x) for x in d.data_luar.split(',') if x],  # Konversi string ke list float
                data_dalam=[float(x) for x in d.data_dalam.split(',') if x],  # Konversi string ke list float
                penanganan=d.penanganan
            ))
        return diagnoses  # Mengembalikan daftar diagnosis

    @staticmethod
    def priority_sort_key(diagnosis):
        # Membuat kunci pengurutan berdasarkan prioritas kode diagnosis
        all_diagnoses = Diagnosis.load_diagnoses()  # Memuat semua diagnosis
        prefixes = sorted(set(d.kode[:2] for d in all_diagnoses))  # Ambil awalan unik dari kode diagnosis
        prefix_priority = {prefix: i for i, prefix in enumerate(prefixes)}  # Tentukan urutan prioritas
        return (prefix_priority.get(diagnosis.kode[:2], 99), diagnosis.kode)  # Kembalikan tuple prioritas dan kode

    @staticmethod
    def is_match(data_luar, data_dalam, diagnosis):
        # Mengecek apakah data input cocok dengan kondisi diagnosis
        for i in range(len(data_dalam)):
            if data_dalam[i] < diagnosis.data_dalam[i]:  # Bandingkan data_dalam pengguna dengan diagnosis
                return False  # Jika ada data tidak cocok, kembalikan False
        return True  # Jika semua cocok, kembalikan True


    @staticmethod
    def diagnose_forward_chaining(data_luar, data_dalam):
        # Melakukan diagnosis menggunakan forward chaining
        diagnoses = Diagnosis.load_diagnoses()  # Memuat semua diagnosis
        diagnoses_sorted = sorted(diagnoses, key=Diagnosis.priority_sort_key)  # Urutkan diagnosis berdasarkan prioritas
        results = []  # Hasil diagnosis
        found_prefixes = set()  # Set untuk menyimpan awalan kode yang sudah ditemukan

        for diagnosis in diagnoses_sorted:
            prefix = diagnosis.kode[:2]  # Ambil awalan kode diagnosis
            if prefix not in found_prefixes and Diagnosis.is_match(data_luar, data_dalam, diagnosis):
                # Jika awalan belum ditemukan dan data cocok, tambahkan ke hasil
                results.append((diagnosis.id,diagnosis.penanganan))
                found_prefixes.add(prefix)  # Tandai awalan sudah ditemukan

        return results  # Kembalikan hasil diagnosis
    # NB
    @staticmethod
    def load_model():
        # Memuat model Naive Bayes dari file joblib
        model = load('naive_bayes_model.joblib')  # Muat model
        return model  # Kembalikan model

    @staticmethod
    def diagnose_naive_bayes(data_gejala, data_khusus):
        # Melakukan prediksi menggunakan Naive Bayes
        model = load_model()  # Memuat model Naive Bayes
        prediction = model.predict(np.array(data_gejala + data_khusus).reshape(1, -1))  # Prediksi dengan input gabungan
        return prediction[0]  # Kembalikan hasil prediksi pertama

    @staticmethod
    def diagnose(data_gejala, data_khusus, data_luar, data_dalam):
        # Menggabungkan hasil Naive Bayes dan Forward Chaining
        naive_bayes_result = Diagnosis.diagnose_naive_bayes(data_gejala, data_khusus)  # Prediksi dengan Naive Bayes

        # Cari diagnosis yang sesuai dengan hasil Naive Bayes
        naive_bayes_diagnosis = next((d for d in Diagnosis.load_diagnoses() if d.id == naive_bayes_result), None)

        # Gunakan Forward Chaining untuk verifikasi hasil
        forward_chaining_results = Diagnosis.diagnose_forward_chaining(data_luar, data_dalam)

        combined_results = []  # Gabungan hasil diagnosis

        # Tambahkan hasil Naive Bayes ke gabungan hasil
        if naive_bayes_diagnosis:
            combined_results.append({
                'id': naive_bayes_diagnosis.id,
                'status': naive_bayes_diagnosis.status.id,  # Sertakan status
                'diagnosa': naive_bayes_diagnosis.diagnosa,
                'penanganan': naive_bayes_diagnosis.penanganan,
                'nama': 'Gejala Tubuh dan Pola Hidup',
                'metode': 'Naive Bayes'
            })

        # Tambahkan hasil Forward Chaining ke gabungan hasil
        for result in forward_chaining_results:
            diagnosis = next((d for d in Diagnosis.load_diagnoses() if d.id == result[0]), None)
            if diagnosis:
                combined_results.append({
                    'id': diagnosis.id,
                    'status': diagnosis.status.id,  # Sertakan status
                    'diagnosa': diagnosis.diagnosa,
                    'penanganan': diagnosis.penanganan,
                    'nama': 'Hasil Antropometri dan Biomarker',
                    'metode': 'Forward Chaining'
                })

        return combined_results  # Kembalikan hasil gabungan diagnosis