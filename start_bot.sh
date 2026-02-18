#!/bin/bash

# Nama fail log
LOG_FILE="bot.log"

echo "------------------------------------------"
echo " Memulakan Sistem Rekod Petugas Masjid V2 "
echo "------------------------------------------"

# Memastikan library sudah dipasang
pip install -r requirements.txt --quiet

# Menjalankan bot di latar belakang
# nohup memastikan proses tidak mati apabila terminal ditutup
nohup python3 bot_petugas.py > $LOG_FILE 2>&1 &

echo "✅ Bot sedang berjalan di latar belakang!"
echo "📂 Log aktiviti disimpan di: $LOG_FILE"
echo "🚀 Anda boleh menutup terminal ini sekarang."
echo "------------------------------------------"
