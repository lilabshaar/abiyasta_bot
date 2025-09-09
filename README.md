Bot Telegram Abiyasta
Bot Telegram ini dirancang untuk membantu manajemen jadwal harian, pengingat waktu makan (RUKAN), dan memberikan motivasi di lingkungan asrama, sekolah, atau komunitas. Bot ini dapat digunakan di grup Telegram untuk memudahkan koordinasi dan meningkatkan kedisiplinan anggota.

Fitur Utama
Jadwal Kegiatan Otomatis

Simpan jadwal harian dengan perintah /setinfo.
Jadwal terstruktur disimpan di jadwal.json, teks asli di info.txt.
Pengingat Otomatis

Reminder RUKAN (waktu makan) 20 menit, 5 menit sebelum, dan saat waktu makan.
Reminder giat (kegiatan) 15 menit sebelum setiap kegiatan.
Informasi Jadwal

/inforengiat : Menampilkan info jadwal harian (isi dari info.txt).
/infogiat : Menampilkan kegiatan yang sedang berlangsung saat ini.
/inforukan : Menampilkan info waktu makan berikutnya dan hitung mundur wajib hadir.
Motivasi

/katakata : Mendapatkan kata-kata motivasi acak.
Cara Instalasi & Menjalankan
Clone repository dan install dependensi:

Buat file .env di folder proyek:

Pastikan file .env masuk ke .gitignore:

Jalankan bot:

Format Jadwal
Gunakan perintah /setinfo dengan format seperti berikut:

Format waktu: HH.MM atau HH.MM - HH.MM
Boleh multiline dan ada catatan tambahan.

Contoh Output Bot
/inforengiat
/infogiat (misal jam 08:00)
/inforukan (misal jam 05:45)
Reminder otomatis (15 menit sebelum giat, misal jam 07:15)
/katakata
File Terkait
bot.py : Source code utama bot
jadwal.json : Jadwal terstruktur
info.txt : Teks asli jadwal
.env : Menyimpan API key (TOKEN) secara aman
Tips Keamanan
Jangan upload file .env ke GitHub.
Simpan API key hanya di .env dan pastikan .env ada di .gitignore.
Kontribusi
Silakan fork, pull request, atau laporkan issue untuk pengembangan fitur baru!

Bot ini cocok untuk pengelolaan jadwal harian di lingkungan sekolah, asrama, atau komunitas.
Membantu disiplin, koordinasi, dan motivasi anggota setiap hari!
