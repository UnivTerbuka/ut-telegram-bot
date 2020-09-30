from telegram import Update
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = """
Langkah langkah Registrasi Online Calon Mahasiswa UT
Form yang memiliki tanda * berwarna merah di kanan namanya wajib diisi!

A. Registrasi Akun Sia

1. Buka https://sia.ut.ac.id/register
2. Masukan Nama (Name), Alamat email (E-Mail Address) yang masih aktif, serta Password (Password & Konfirmasi Password disamakan)
3. Masukan kode captcha yang ada di gambar ke form di bawahnya
4. Lalu klik Register
5. Silahkan cek Kotak Masuk (Inbox) dari Alamat email yang anda masukan, pastikan ada email baru dari UNIVERSITAS TERBUKA (srs@ut.ac.id) jika tidak ulangi proses 1-4
6. Buka / klik link dalam email verivikasi tersebut (dengan teks Link Verifikasi)


B. Registrasi UPBJJ & Jenjang Pendidikan

1. Buka https://sia.ut.ac.id/login dan masuk dengan akun yang terverivikasi
2. Silahkan pilih UPBJJ-UT (sesuai dengan domisili anda), jenjang pendidikan yang ingin ditempuh, serta Fakultas dan Program Studi
3. Kemudian klik SELANJUTNYA


C. Registrasi Data Pribadi

1. Isi & lengkapi Form Pengisian Data Pribadi Sementara
2. Isi form Alamat Pengiriman (di gunakan untuk mengirim bahan ajar)
3. Isi Form Pengisian Data Pribadi Sementara (yang kedua)
4. Isi form Informasi Tambahan
5. Unggah semua Berkas Pendaftaran (dapat berupa foto)
6. Kemudian Klik Simpan
"""


@action.typing
def registrasi(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
