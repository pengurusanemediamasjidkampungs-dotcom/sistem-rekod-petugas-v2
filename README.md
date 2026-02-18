# Sistem Rekod Petugas Masjid V2 (Offline-First)

Sistem rekod kehadiran petugas masjid (Imam & Muazzin) yang sangat ringan, direka khas untuk penggunaan CPU/RAM hampir sifar supaya tidak mengganggu perisian kritikal lain seperti OBS atau CCTV monitor.

## 🚀 Ciri-ciri Utama
- **Zero GUI Load**: Berjalan sepenuhnya di terminal/latar belakang.
- **Dual Bot System**: Bot berbeza untuk Imam dan Muazzin dengan pangkalan data CSV berasingan.
- **Offline Storage**: Data disimpan dalam fail `.csv` secara lokal.
- **Telegram Integrated**: Notifikasi kehadiran dihantar terus ke Group Telegram Masjid.

## 📂 Struktur Fail
- `bot_petugas.py`: Skrip utama Python (Asyncio).
- `petugas.json`: Senarai data petugas (Imam, Bilal, Nazir).
- `rekod_imam.csv`: Pangkalan data kehadiran Imam.
- `rekod_muazzin.csv`: Pangkalan data kehadiran Muazzin/Bilal.
- `start_bot.sh`: Skrip untuk memulakan sistem.

## 🛠️ Cara Pemasangan di Ubuntu

1. **Clone Repository:**
   ```bash
   git clone [https://github.com/pengurusanemediamasjidkampungs-dotcom/sistem-rekod-petugas-v2.git](https://github.com/pengurusanemediamasjidkampungs-dotcom/sistem-rekod-petugas-v2.git)
   cd sistem-rekod-petugas-v2

```

2. **Pasang Library:**
```bash
pip install -r requirements.txt

```


3. **Beri Kebenaran (Permission):**
```bash
chmod +x start_bot.sh

```


4. **Jalankan Bot:**
```bash
./start_bot.sh

```



## 📊 Semakan Rekod

Rekod boleh disemak terus melalui fail `.csv` atau melalui mesej yang dihantar oleh bot ke dalam Group Telegram yang telah dikonfigurasi.

---

Dikembangkan untuk: **Pengurusan E-Media Masjid Kampung**

```

---
