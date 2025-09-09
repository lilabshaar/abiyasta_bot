from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatType
import os
import json
import re
import asyncio
from datetime import datetime, time, timedelta
import random

TOKEN = "7700385066:AAGTD1cZdDpj1RIUXSrK3BFzy2oNP0JLpUQ"
JADWAL_FILE = "jadwal.json"

RUKAN_TIMES = ["06.00", "12.30", "18.30"]

KATA_KATA_LIST = [
    "Kerja keras mengalahkan bakat saat bakat tidak bekerja keras.",
    "Jangan menyerah, keajaiban terjadi saat kamu tidak menyerah.",
    "Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.",
    "Setiap hari adalah kesempatan baru untuk menjadi lebih baik.",
    "Percaya pada proses, hasil akan mengikuti.",
    "Kegagalan adalah awal dari kesuksesan.",
    "Jangan takut bermimpi besar, mulailah dari langkah kecil.",
    "Keberanian adalah kunci membuka pintu peluang.",
    "Belajar dari kemarin, hidup untuk hari ini, berharap untuk besok.",
    "Usaha tidak akan mengkhianati hasil."
]

def parse_jadwal(text):
    jadwal = []
    lines = text.strip().splitlines()
    for line in lines:
        line = line.strip()
        # Match format: HH.MM - HH.MM Kegiatan
        match = re.match(r"^(\d{2}\.\d{2})\s*-\s*(\d{2}\.\d{2})\s+(.*)$", line)
        if match:
            start, end, kegiatan = match.groups()
            jadwal.append({
                "start": start,
                "end": end,
                "kegiatan": kegiatan.strip()
            })
            continue
        # Match format: HH.MM Kegiatan
        match = re.match(r"^(\d{2}\.\d{2})\s+(.*)$", line)
        if match:
            start, kegiatan = match.groups()
            jadwal.append({
                "start": start,
                "end": start,
                "kegiatan": kegiatan.strip()
            })
    return jadwal

def save_jadwal(jadwal):
    with open(JADWAL_FILE, "w", encoding="utf-8") as f:
        json.dump({"jadwal": jadwal}, f, ensure_ascii=False, indent=2)

async def setinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    full_text = update.message.text
    info = full_text[len('/setinfo '):] if full_text.startswith('/setinfo ') else full_text
    info = info.strip()
    if not info:
        await update.message.reply_text("Format: /setinfo [jadwal] (boleh multiline).")
        return
    jadwal = parse_jadwal(info)
    save_jadwal(jadwal)
    # Simpan info asli ke info.txt
    with open("info.txt", "w", encoding="utf-8") as f:
        f.write(info)
    await update.message.reply_text("Jadwal berhasil disimpan ke jadwal.json dan info.txt!")

def load_jadwal():
    if not os.path.exists(JADWAL_FILE):
        return [], ""
    with open(JADWAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("jadwal", []), ""

def format_table(jadwal):
    if not jadwal:
        return "Belum ada jadwal."
    header = f"{'Mulai':<8} {'Selesai':<8} {'Kegiatan'}"
    rows = [header, "-"*35]
    for item in jadwal:
        rows.append(f"{item['start']:<8} {item['end']:<8} {item['kegiatan']}")
    return "\n".join(rows)

def parse_time_str(tstr):
    return datetime.strptime(tstr, "%H.%M").time()

def get_next_rukan(now=None):
    if not now:
        now = datetime.now()
    now_time = now.time()
    today = now.date()
    rukan_times = [parse_time_str(t) for t in RUKAN_TIMES]
    for t in rukan_times:
        if now_time < t:
            return datetime.combine(today, t)
    # Jika sudah lewat semua, ambil RUKAN pertama besok
    return datetime.combine(today + timedelta(days=1), rukan_times[0])

def is_rukan_now(now=None):
    if not now:
        now = datetime.now()
    now_time = now.time()
    for t in RUKAN_TIMES:
        rukan_time = parse_time_str(t)
        # Anggap jam RUKAN berlangsung 30 menit
        end_time = (datetime.combine(datetime.today(), rukan_time) + timedelta(minutes=30)).time()
        if rukan_time <= now_time < end_time:
            return True
    return False

def get_current_activity(jadwal):
    now = datetime.now()  # Ambil waktu lokal tanpa penambahan jam
    now_time = now.time()
    for item in jadwal:
        start = datetime.strptime(item['start'], "%H.%M").time()
        end = datetime.strptime(item['end'], "%H.%M").time()
        # Handle overnight activities (end < start)
        if end < start:
            if start <= now_time or now_time <= end:
                return item, now
        else:
            if start <= now_time <= end:
                return item, now
    return None, now

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya siap membantu di grup ini 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
         "📌 Daftar Perintah Bot Abiyasta:\n\n"
    "🤝 /help - Dapatkan bantuan dan cara penggunaan bot\n"
    "📅 /inforengiat - Lihat tabel lengkap jadwal kegiatan harian\n"
    "⏰ /infogiat - Cek kegiatan yang sedang berlangsung saat ini\n"
    "🍽️ /inforukan - Info lengkap ruang makan (RUKAN) berikutnya, plus hitung mundur hadir\n"
    "💡 /katakata - Dapatkan kata-kata motivasi untuk membakar semangat\n"
    )
    await update.message.reply_text(help_text)

async def inforengiat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists("info.txt"):
        await update.message.reply_text("Belum ada info jadwal.")
        return
    with open("info.txt", "r", encoding="utf-8") as f:
        info = f.read().strip()
    if not info:
        await update.message.reply_text("Belum ada info jadwal.")
        return
    await update.message.reply_text(f"Informasi Rengiat:\n{info}")

async def infogiat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jadwal, _ = load_jadwal()
    if not jadwal:
        await update.message.reply_text("Belum ada jadwal.")
        return
    item, now = get_current_activity(jadwal)
    now_str = now.strftime("%H:%M WIB")
    if item:
        await update.message.reply_text(
            f"⏰ Sekarang: {now_str}\n📌 Giat: {item['kegiatan']} ({item['start']} - {item['end']})"
        )
    else:
        await update.message.reply_text(f"⏰ Sekarang: {now_str}\nTidak ada kegiatan yang sedang berlangsung.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Kamu bilang: {update.message.text}")

async def inforukan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    now_str = now.strftime("%H:%M WIB")
    if is_rukan_now(now):
        await update.message.reply_text(f"⏰ Sekarang: {now_str}\nSedang jam RUKAN, silakan makan sekarang.")
    else:
        next_rukan = get_next_rukan(now)
        delta = next_rukan - now
        menit_lagi = int(delta.total_seconds() // 60)
        wajib_hadir = max(menit_lagi - 15, 0)
        await update.message.reply_text(
            f"⏰ Sekarang: {now_str}\nBelum jam RUKAN.\n"
            f"RUKAN berikutnya: {next_rukan.strftime('%H:%M WIB')}\n"
            f"Wajib hadir dalam {wajib_hadir} menit."
        )

async def katakata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kata = random.choice(KATA_KATA_LIST)
    await update.message.reply_text(f"🌟 Kata-kata hari ini:\n\n{kata}")

chat_ids = set()

async def track_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    # Hanya simpan chat_id grup
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        chat_ids.add(chat.id)

async def rukan_reminder(app: Application):
    while True:
        now = datetime.now()
        today = now.date()
        for tstr in RUKAN_TIMES:
            rukan_dt = datetime.combine(today, parse_time_str(tstr))
            # Reminder 20 menit sebelum
            remind_20 = rukan_dt - timedelta(minutes=20)
            # Reminder 5 menit sebelum
            remind_5 = rukan_dt - timedelta(minutes=5)
            # Reminder saat RUKAN
            remind_0 = rukan_dt

            for remind_time, msg in [
                (remind_20, "20 menit lagi menuju RUKAN, wajib hadir 15 menit sebelumnya."),
                (remind_5, "Segera menuju RUKAN."),
                (remind_0, "Lonceng berbunyi, mulai makan sekarang."),
            ]:
                wait_sec = (remind_time - datetime.now()).total_seconds()
                if wait_sec > 0:
                    await asyncio.sleep(wait_sec)
                    # Kirim ke semua grup yang pernah ada interaksi
                    for chat_id in chat_ids:
                        await app.bot.send_message(chat_id, msg)
        # Tunggu sampai hari berikutnya
        tomorrow = datetime.combine(today + timedelta(days=1), time(0, 0))
        wait_sec = (tomorrow - datetime.now()).total_seconds()
        if wait_sec > 0:
            await asyncio.sleep(wait_sec)

async def giat_reminder(app: Application):
    while True:
        jadwal, _ = load_jadwal()
        now = datetime.now()
        today = now.date()
        for item in jadwal:
            start_time = datetime.strptime(item['start'], "%H.%M").time()
            giat_dt = datetime.combine(today, start_time)
            remind_dt = giat_dt - timedelta(minutes=15)
            wait_sec = (remind_dt - datetime.now()).total_seconds()
            if wait_sec > 0:
                await asyncio.sleep(wait_sec)
                msg = f"⏰ 15 menit lagi menuju giat: {item['kegiatan']} ({item['start']} - {item['end']})"
                for chat_id in chat_ids:
                    await app.bot.send_message(chat_id, msg)
        # Tunggu sampai hari berikutnya
        tomorrow = datetime.combine(today + timedelta(days=1), time(0, 0))
        wait_sec = (tomorrow - datetime.now()).total_seconds()
        if wait_sec > 0:
            await asyncio.sleep(wait_sec)

async def post_init(app: Application):
    app.create_task(rukan_reminder(app))
    app.create_task(giat_reminder(app))  # Tambahkan ini

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("setinfo", setinfo))
    app.add_handler(CommandHandler("inforengiat", inforengiat))
    app.add_handler(CommandHandler("infogiat", infogiat))
    app.add_handler(CommandHandler("inforukan", inforukan))
    app.add_handler(CommandHandler("katakata", katakata))  # Tambahkan handler baru
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.ALL, track_chat_id))  # Track chat_id grup

    print("Bot berjalan...")

    app.run_polling()

if __name__ == "__main__":
    main()