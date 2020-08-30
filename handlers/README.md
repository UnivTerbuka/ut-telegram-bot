# Handlers

Folder ini tempat handler yang menghandle Update dari telegram dengan menggunakan telegram.ext

## Callbacks

Tempat semua callback_query direspon, callback_query dijalankan ketika pengguna menekan tombol InlineKeyboardButton yang mengandung callback_data, dimana callback data tersebut dapat difilter dengan menggunakan Regex.

## Commands

Tempat semua kode yang berhubungan dengan command (perintah) dalam chat telegram, semua command di sini bersifat private / difilter.

## Conversations

Tempat semua percakapan yang sebagian besar dengan entry point _command handler_ dan fallback perintah cancel

## Inlines

Tempat kode yang menghandle inline (inline mode) telegram
