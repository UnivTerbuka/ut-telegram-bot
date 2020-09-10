from telegram import Update
from telegram.ext import CallbackContext

MESSAGE = 'Dengan menggunakan bot ini Anda memahami dan setuju bahwa :\n'\
    '1. Bot ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara,'\
    ' disponsori atau didukung oleh Universitas Terbuka.\n'\
    '2. Bot ini adalah perangkat lunak yang independen dan tidak resmi.'\
    ' Gunakan dengan risiko Anda sendiri!\n'\
    '3. @hexatester akan menyediakan support & update dengan terbatas,'\
    ' jadi kalau terjadi error / lambat harap dimaklumi.\n\n'\
    'Jika Anda merasa terbantu dengan adanya bot ini,'\
    ' tolong bantu @hexatester dengan mengeshare bot ini,'\
    ' khususnya kepada mahasiswa Universitas Terbuka.\n\n'\
    'Maaf dan Terimakasih,\n'\
    '@hexatester'


def eula(update: Update, context: CallbackContext):
    update.effective_message.reply_text(MESSAGE)
