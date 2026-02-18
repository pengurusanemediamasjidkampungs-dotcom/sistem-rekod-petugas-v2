import logging
import json
import csv
import datetime
import asyncio
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# ==========================================
# KONFIGURASI BOT & GROUP
# ==========================================
CONFIG = {
    "IMAM": {
        "token": "8556037283:AAGVZAE_8rCKN5YFaZRRHK-mkAf3xZHOofY", 
        "chat_id": "-1003763076324",
        "csv": "rekod_imam.csv",
        "kategori": "imam"
    },
    "MUAZZIN": {
        "token": "8514736580:AAFG0mNtKxvz6EPHgWOzvweoSpINIdFWuIA", 
        "chat_id": "-1003750856502",
        "csv": "rekod_muazzin.csv",
        "kategori": "bilal"
    }
}

# Pastikan fail CSV wujud dengan header jika baru
for cfg in CONFIG.values():
    if not os.path.exists(cfg['csv']):
        with open(cfg['csv'], mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "tarikh", "Hari", "Nama petugas", "Jawatan", "Waktu Solat", "Status", "Catatan"])

# Muat data JSON petugas
try:
    with open('petugas.json', 'r') as f:
        DATA_JSON = json.load(f)
except FileNotFoundError:
    print("RALAT: Fail petugas.json tidak dijumpai!")
    exit()

# ==========================================
# FUNGSI PEMBANTU
# ==========================================
def rekod_ke_csv(file_csv, nama, jawatan, waktu, status, catatan="-"):
    now = datetime.datetime.now()
    hari_map = {
        "Monday": "Isnin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Khamis", "Friday": "Jumaat", "Saturday": "Sabtu", "Sunday": "Ahad"
    }
    hari = hari_map[now.strftime("%A")]
    
    with open(file_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            now.strftime("%Y-%m-%d %H:%M:%S"), 
            now.strftime("%d/%m/%Y"), 
            hari, nama, jawatan, waktu, status, catatan
        ])

# ==========================================
# HANDLERS (LOGIK BOT)
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Subuh", callback_data='w_Subuh'), InlineKeyboardButton("Zohor", callback_data='w_Zohor')],
        [InlineKeyboardButton("Asar", callback_data='w_Asar'), InlineKeyboardButton("Maghrib", callback_data='w_Maghrib')],
        [InlineKeyboardButton("Isyak", callback_data='w_Isyak'), InlineKeyboardButton("Jumaat", callback_data='w_Jumaat')]
    ]
    await update.message.reply_text('🌙 Sila pilih Waktu Solat:', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, config_key: str):
    query = update.callback_query
    await query.answer()
    data = query.data
    cfg = CONFIG[config_key]

    # 1. Pilih Waktu
    if data.startswith('w_'):
        context.user_data['waktu'] = data.split('_')[1]
        petugas_list = DATA_JSON.get(cfg['kategori'], [])
        
        keyboard = [[InlineKeyboardButton(p['nama'], callback_data=f"p_{p['id']}")] for p in petugas_list]
        await query.edit_message_text(
            text=f"📌 Waktu: {context.user_data['waktu']}\n\nSila pilih Nama Petugas:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 2. Pilih Nama & Tanya Status
    elif data.startswith('p_'):
        pid = data.split('_')[1]
        petugas_list = DATA_JSON.get(cfg['kategori'], [])
        petugas = next((p for p in petugas_list if p['id'] == pid), None)
        
        if petugas:
            context.user_data['petugas'] = petugas
            keyboard = [
                [InlineKeyboardButton("✅ Hadir Sendiri", callback_data='s_Hadir')],
                [InlineKeyboardButton("🔄 Ganti (Orang Lain)", callback_data='s_Ganti')]
            ]
            await query.edit_message_text(
                text=f"Petugas: {petugas['nama']}\nJawatan: {petugas['jawatan']}\n\nSahkan kehadiran:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    # 3. Simpan Rekod
    elif data.startswith('s_'):
        status_type = data.split('_')[1]
        p = context.user_data.get('petugas')
        w = context.user_data.get('waktu')

        if status_type == 'Hadir':
            rekod_ke_csv(cfg['csv'], p['nama'], p['jawatan'], w, "Hadir", "Petugas Asal")
            msg = f"✅ REKOD DISIMPAN\n\nPetugas: {p['nama']}\nWaktu: {w}\nStatus: Hadir"
            await query.edit_message_text(text=msg)
            await context.bot.send_message(chat_id=cfg['chat_id'], text=msg)
        else:
            context.user_data['waiting_for_ganti'] = True
            await query.edit_message_text(text=f"Sila taip NAMA PENGGANTI untuk menggantikan {p['nama']}:")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE, config_key: str):
    if context.user_data.get('waiting_for_ganti'):
        cfg = CONFIG[config_key]
        nama_ganti = update.message.text.upper()
        p = context.user_data.get('petugas')
        w = context.user_data.get('waktu')

        rekod_ke_csv(cfg['csv'], nama_ganti, p['jawatan'], w, "Hadir (Ganti)", f"Ganti {p['nama']}")
        
        res = f"✅ REKOD GANTI DISIMPAN\n\nNama: {nama_ganti}\nGanti: {p['nama']}\nWaktu: {w}"
        await update.message.reply_text(res)
        await context.bot.send_message(chat_id=cfg['chat_id'], text=res)
        
        context.user_data['waiting_for_ganti'] = False

# ==========================================
# RUNNER
# ==========================================
async def setup_bot(config_key):
    cfg = CONFIG[config_key]
    app = Application.builder().token(cfg['token']).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lambda u, c: handle_callback(u, c, config_key)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_text(u, c, config_key)))
    
    await app.initialize()
    await app.start_polling()
    print(f"Bot {config_key} sedang berjalan...")

async def main():
    # Menjalankan kedua-dua bot serentak
    await asyncio.gather(setup_bot("IMAM"), setup_bot("MUAZZIN"))
    # Menjaga skrip supaya tidak mati
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot telah dihentikan.")
