from telegram import Update
from telegram.ext import CallbackContext
from core.utils import action

MESSAGE = """
Daftar Formulir yang dapat di-download kemudian dicetak untuk diisi

<a href="https://ut.ac.id/sites/all/files/images/2020/juli/Formulir_Data_Pribadi_Mahasiswa_UT_F1-E_AM01-RK10-RII.6_09_Maret_2020_Universitas_Terbuka.pdf">Formulir Data Pribadi Mahasiswa Universitas Terbuka (F-1E AM01-RK10-RII.6)</a>
<a href="https://ut.ac.id/sites/all/files/images/2016/april/Formulir-UT-Reg-MatKul-AM01-RK12-RII1.pdf">Formulir Registrasi Mata Kuliah - AM01-RK12-RII.1</a>
<a href="https://ut.ac.id/sites/all/files/images/2017/November/Formulir_Pas_Foto_Tanda_Tangan_Mahasiswa_UT_AM01-RK04c-RII.2_3_April_2017.pdf">Formulir Isian Pas Foto, dan Tanda Tangan Mahasiswa UT (AM01_RK04c_RII.2)</a>
<a href="https://ut.ac.id/sites/all/files/images/2016/april/Formulir-UT-SP-BenarData-SahDok-AM01-RK04a-RII1.pdf">Mahasiswa Program Sarjana dan Diploma FE, FHISIP, FST, FKIP, dan Program Pascasarjana - AM01-RK04a-RII.1</a>
<a href="https://ut.ac.id/sites/all/files/images/2016/april/Formulir-UT-SP-BenarData-SahDok-AM01-RK04b-RII2.pdf">Mahasiswa Program Sarjana PGSD dan PGPAUD FKIP Masukan Sarjana - AM01-RK04b-RII.2</a>
<a href="https://ut.ac.id/sites/all/files/images/2019/agustus/Form_SIPAS_Pernyataan_2019.docx">Formulir Surat Pernyataan Mahasiswa Layanan Sipas Universitas Terbuka</a>

<a href="https://www.ut.ac.id/formulir">Sumber</a>
"""


@action.typing
def formulir(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
