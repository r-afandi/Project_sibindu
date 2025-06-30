from .....expert.models.m_kepakaran import Gejala,Pakar,Diagnosa
class DiagnosisEngine:
    def __init__(self, data_khusus, data_luar, data_dalam):
        self.data_khusus = data_khusus
        self.data_luar = data_luar
        self.data_dalam = data_dalam
        self.diagnosis = None
        self.penanganan = None

    def apply_rules(self):
        # Ambil semua diagnosis dari database
        all_diagnosis = Diagnosa.objects.all()

        for diagnosa in all_diagnosis:
            # Ubah data dari string ke list
            db_data_khusus = list(map(int, diagnosa.data_khusus.split(',')))
            db_data_dalam = list(map(float, diagnosa.data_dalam.split(',')))
            db_data_luar = list(map(float, diagnosa.data_luar.split(',')))

            # Periksa kecocokan data khusus
            if self.data_khusus == db_data_khusus:
                # Periksa kecocokan data dalam
                match_data_dalam = all(
                    d <= p for d, p in zip(self.data_dalam, db_data_dalam)
                )
                # Periksa kecocokan data luar
                match_data_luar = all(
                    d >= p for d, p in zip(self.data_luar, db_data_luar)
                )

                if match_data_dalam and match_data_luar:
                    self.diagnosis = diagnosa.id
                    self.penanganan = diagnosa.penanganan
                    return  # Keluar dari loop saat diagnosis ditemukan

def diagnose(data_khusus, data_luar, data_dalam):
    engine = DiagnosisEngine(data_khusus, data_luar, data_dalam)
    engine.apply_rules()
    return engine.diagnosis, engine.penanganan

# Penggunaan dalam view
diagnosis_results = diagnose(data_khusus, data_luar, data_dalam)

if diagnosis_results[0]:  # Ada diagnosis yang valid
    data.diagnosa_id = diagnosis_results[0]
    data.penanganan = diagnosis_results[1]
    valid_diagnosis = True
else:
    valid_diagnosis = False
