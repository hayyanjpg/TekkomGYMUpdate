Tekkom GYM - Aplikasi Manajemen Gym Berbasis Web
Tekkom GYM adalah aplikasi berbasis web yang dirancang untuk mempermudah pengelolaan gym dan memberikan pengalaman yang lebih baik bagi anggota, pelatih, serta pengelola gym. Aplikasi ini dikembangkan menggunakan Python dengan framework Flask dan database SQLite.

Latar Belakang
Di era digital, kebutuhan akan platform kebugaran yang mudah diakses semakin meningkat. Pengelolaan gym tradisional sering menghadapi tantangan seperti kurangnya platform digital untuk manajemen pengguna, kesulitan dalam menyampaikan informasi jadwal atau promosi, dan tidak adanya sistem yang efisien untuk pemesanan kelas atau pelatih pribadi. Website "TekkomGym" dirancang untuk menjawab tantangan tersebut dengan menawarkan solusi berbasis web yang praktis dan efisien.

Fitur Utama
Aplikasi ini memiliki dua peran utama: User (Anggota) dan Admin.

Untuk User (Anggota):
Pendaftaran dan Login: Pengguna dapat membuat akun baru dan masuk ke sistem dengan aman.

Marketplace: Anggota dapat melihat dan membeli produk-produk terkait kebugaran seperti suplemen dan peralatan gym.

Manajemen Keanggotaan: Pengguna dapat membeli dan mengelola paket keanggotaan mereka secara online.

Lihat Jadwal Kelas: Melihat informasi jadwal kelas kebugaran yang tersedia secara real-time.

Untuk Admin:
Dashboard Admin: Halaman khusus untuk mengelola seluruh aspek aplikasi.

Manajemen Produk: Admin dapat menambah, memperbarui, dan menghapus produk yang dijual di marketplace.

Manajemen Membership: Mengelola jenis, harga, dan status paket keanggotaan yang ditawarkan.

Kelola Pengguna & Admin: Admin memiliki hak akses penuh untuk mengelola data pengguna dan admin lainnya.

Teknologi yang Digunakan
Backend: Python, Flask, Flask-SQLAlchemy

Frontend: HTML, CSS, JavaScript

Database: SQLite

Deployment: PythonAnywhere

Struktur Proyek
.
├── Dokumen/              # Berisi semua file dokumentasi (SKPL, DPPL, dll.)
├── ERD/                  # Diagram relasi entitas dan desain database
├── Tekkom_gym1/
│   ├── static/           # File statis (CSS, JavaScript, gambar)
│   ├── templates/        # Template HTML untuk antarmuka pengguna
│   ├── main.py           # File utama aplikasi Flask
│   └── instance/
│       └── TekkomGym.db  # File database SQLite
├── USE CASE/             # Diagram UML (Use Case, Activity, Sequence)
├── LICENSE               # File lisensi proyek
└── README.md             # File ini

Instalasi dan Setup
Untuk menjalankan proyek ini di lingkungan lokal, ikuti langkah-langkah berikut:

Clone repositori:

git clone [https://github.com/hayyanjpg/TekkomGYMUpdate.git](https://github.com/hayyanjpg/TekkomGYMUpdate.git)
cd TekkomGYMUpdate

Buat dan aktifkan virtual environment (opsional tapi disarankan):

# Membuat virtual environment
python -m venv venv

# Mengaktifkan di Windows
venv\Scripts\activate

# Mengaktifkan di macOS/Linux
source venv/bin/activate

Install dependensi:
Aplikasi ini menggunakan Flask dan beberapa library lainnya. Install semua yang dibutuhkan dengan pip.

pip install Flask Flask-SQLAlchemy Flask-Migrate Werkzeug

Jalankan aplikasi:
Masuk ke direktori Tekkom_gym1 dan jalankan file main.py.

cd Tekkom_gym1
python main.py

Akses aplikasi:
Buka browser Anda dan kunjungi http://127.0.0.1:5000.

Login Admin Default: username: admin, password: 1

Login User Default: username: aan, password: 1

Kontributor: 
HAYYAN NASHRULLOH (2211102100)

M. ALFAREZ PAHLEVI TANJUNG (2211102069)

NIZAR QULUBI (2211102096)

HIZAM ARIPIN (2211102317)

SINGGIH PRAWIRO NEGORO (2211102341)

ASA PUTRA PRATAMA (2211102092)

Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT.
