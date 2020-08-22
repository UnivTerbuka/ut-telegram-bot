# ut-telegram-bot

[![Group Telegram](https://img.shields.io/badge/Telegram-Group-blue.svg)](https://t.me/UniversitasTerbuka)
[![Donasi DANA](https://img.shields.io/badge/Donasi-DANA-blue)](https://link.dana.id/qr/1lw2r12r)
[![LISENSI](https://img.shields.io/github/license/hexatester/ut-telegram-bot)](https://github.com/hexatester/ut-telegram-bot/blob/master/LISENSI)
[![Build](https://github.com/hexatester/ut-telegram-bot/workflows/Build/badge.svg)](https://github.com/hexatester/ut-telegram-bot/actions?query=workflow%3ABuild)

Source code dari @UniversitasTerbukaBot dibuat untuk memudahkan mahasiswa Universitas Terbuka mengakses layanan Universitas Terbuka melalui aplikasi Telegram.

## Fitur

- RBV (Ruang Baca Virtual)
- Cek tiket
- Shortlink UT
- Cari buku

## Fitur yang akan datang

- Elearning UT
- QnA & FAQ

## Migrasi

Buat migrasi

```bash
python manage.py db init
python manage.py db migrate
```

Jalankan migrasi

```bash
python manage.py db upgrade
```

## Legal / Hukum

Kode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh [Universitas Terbuka](https://ut.ac.id/) atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.
