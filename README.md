# 🤖 Abiyasta Bot – Telegram Asisten Harian

**Abiyasta Bot** adalah bot Telegram yang dirancang untuk membantu **manajemen jadwal harian, pengingat waktu makan (RUKAN), dan motivasi** di lingkungan **asrama, sekolah, maupun komunitas**.
Bot ini dapat digunakan di grup Telegram untuk memudahkan **koordinasi dan meningkatkan kedisiplinan anggota**.

---

## ✨ Fitur Utama

### 📅 Jadwal Kegiatan Otomatis

* Simpan jadwal harian dengan perintah:

  ```
  /setinfo
  ```
* Jadwal terstruktur disimpan di **jadwal.json**, sedangkan teks asli disimpan di **info.txt**.

### 🔔 Pengingat Otomatis

* **Reminder RUKAN (waktu makan):**

  * 20 menit sebelum,
  * 5 menit sebelum,
  * dan tepat saat waktu makan.
* **Reminder kegiatan:** 15 menit sebelum setiap giat.

### 📖 Informasi Jadwal

* `/inforengiat` → Menampilkan info jadwal harian (isi dari **info.txt**).
* `/infogiat` → Menampilkan kegiatan **yang sedang berlangsung saat ini**.
* `/inforukan` → Menampilkan info **waktu makan berikutnya** dan **hitung mundur wajib hadir**.

### 💡 Motivasi

* `/katakata` → Dapatkan kata-kata motivasi acak untuk membangkitkan semangat.

---

## ⚙️ Cara Instalasi & Menjalankan

1. Clone repository dan install dependensi.

   ```bash
   git clone <repo-url>
   cd abiyasta-bot
   pip install -r requirements.txt
   ```

2. Buat file `.env` di folder proyek:

   ```
   TOKEN=your_telegram_bot_api_key
   ```

3. Pastikan file `.env` masuk ke `.gitignore` (jangan pernah di-push ke GitHub).

4. Jalankan bot:

   ```bash
   python bot.py
   ```

---

## 📋 Format Jadwal

Gunakan perintah `/setinfo` dengan format seperti berikut:

* Format waktu: `HH.MM` atau `HH.MM - HH.MM`.
* Boleh multiline dan menambahkan catatan tambahan.

**Contoh input:**

```
04.00              BANGUN PAGI
04.30 - 05.30      SHOLAT
06.00              MAKAN PAGI
07.00              APEL
07.30 - 11.40      PERKULIAHAN
...
NOTE:
- Hindari pelanggaran
- Sholat 5 waktu di Masjid
```

---

## 🖼️ Contoh Output Bot

* `/inforengiat`
  → Tampilkan tabel rapi dari jadwal harian.

* `/infogiat` (misal jam **08:00**)
  → "Sekarang: Perkuliahan (07.30 – 11.40)"

* `/inforukan` (misal jam **05:45**)
  → "RUKAN berikutnya pukul 06:00, wajib hadir dalam 15 menit lagi."

* Reminder otomatis (15 menit sebelum giat, misal jam **07:15**)
  → "⚠️ 15 menit lagi menuju kegiatan: APEL (07.30)."

* `/katakata`
  → "💡 *Disiplin adalah kunci kesuksesan!*"

---

## 📂 Struktur File

* **bot.py** → Source code utama bot.
* **jadwal.json** → Jadwal terstruktur.
* **info.txt** → Teks asli jadwal.
* **.env** → Menyimpan API key (TOKEN) secara aman.

---

## 🔒 Tips Keamanan

* Jangan upload file `.env` ke GitHub.
* Simpan API key hanya di `.env`.
* Pastikan `.env` ada di `.gitignore`.

---

## 🤝 Kontribusi

Silakan **fork, pull request, atau laporkan issue** untuk pengembangan fitur baru!
Bot ini cocok untuk pengelolaan jadwal harian di **sekolah, asrama, atau komunitas**.
Membantu **disiplin, koordinasi, dan motivasi anggota** setiap hari!
