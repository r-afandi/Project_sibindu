# SIBINDU - Sistem Informasi POSBINDU PTM

**SIBINDU** adalah sistem informasi berbasis web yang dirancang untuk mendukung kegiatan Pos Pembinaan Terpadu Penyakit Tidak Menular (POSBINDU PTM). Aplikasi ini juga dilengkapi dengan fitur **sistem pakar diagnosis dini diabetes** berbasis metode **Naive Bayes** dan **Forward Chaining**.

Website demo: **Menyusul**

Login demo:  

**admin**
- **Username:** admin
- **Password:** sibindu1

**expert**
- **Username:** expert
- **Password:** sibindu2

**validator**
- **Username:** validator
- **Password:** sibindu3

**petugas** 
- **Username:** petugas  
- **Password:** sibindu4

> ⚠️ Ini adalah proyek portofolio pribadi dan **tidak digunakan dalam instansi resmi manapun**.

---

## ✨ Fitur Utama

- Manajemen data suspek (peserta pemeriksaan POSBINDU)
- Input dan penyimpanan data gejala, faktor risiko, dan hasil pemeriksaan
- Diagnosis otomatis berdasarkan gejala dengan metode:
  - **Naive Bayes** (berbasis data training)
  - **Forward Chaining** (berbasis aturan)
- Riwayat pemeriksaan dan rekam medis sederhana
- Panel admin dan hak akses petugas
- Export laporan hasil pemeriksaan
- Autentikasi pengguna (petugas/admin)

---

## ⚙️ Teknologi yang Digunakan

- **Backend:** Python (Django)
- **Frontend:** HTML, Bootstrap, JavaScript
- **Database:** MySQL / MariaDB
- **Deployment:** Gunicorn, Nginx, VPS (Ubuntu)
- **Others:** Pandas, NumPy (untuk pengolahan data diagnosis)

---

## 📁 Struktur Direktori (Umum)
Project_sibindu/
├── apps/ # Aplikasi Django modular (pengelolaan user, data, diagnosa)
├── core/ # Konfigurasi utama project Django
├── templates/ # Template HTML untuk frontend
├── static/ # File statis (CSS, JS, ikon)
├── media/ # Media upload pengguna
├── manage.py # Entry point Django
└── requirements.txt # Daftar dependensi Python

📷 Tampilan Aplikasi
Berikut beberapa cuplikan antarmuka SIBINDU:

- Halaman login pengguna

- Input data gejala & pemeriksaan

- Hasil diagnosis otomatis

- Dashboard & histori pasien


📌 Catatan
- Password dan akun yang disediakan hanya untuk keperluan demo.

📬 Kontak
Rizki Afandi
Email: nama.rizki.afandi@gmail.com
LinkedIn: https://www.linkedin.com/in/rizki-afandi-6b88a1233/

