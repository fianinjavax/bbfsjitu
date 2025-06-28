# Panduan Deploy ke Streamlit Community Cloud

## Langkah-Langkah Deploy

### 1. Persiapan Repository
- Pastikan semua file aplikasi sudah ada di repository GitHub
- File yang diperlukan:
  - `app.py` (file utama)
  - `bbfs_4d_6digit_system.py`
  - `optimized_bbfs_system.py` 
  - `ultra_smart_bbfs.py`
  - `streamlit_branding_remover.py`
  - `.streamlit/config.toml`

### 2. Deploy di Streamlit Community Cloud

#### A. Akses Streamlit Cloud
1. Buka https://share.streamlit.io/
2. Login dengan akun GitHub Anda

#### B. Deploy Aplikasi
1. Klik "New app"
2. Pilih repository GitHub yang berisi aplikasi
3. Set konfigurasi:
   - **Repository**: pilih repo Anda
   - **Branch**: main atau master
   - **Main file path**: `app.py`
   - **App URL**: (opsional, akan auto-generate)

#### C. Dependencies
Streamlit Cloud akan otomatis menginstall dependencies dari file berikut:
- `requirements.txt` (jika ada)
- Import statements di `app.py`

Dependencies yang dibutuhkan:
```
streamlit
requests
numpy
pandas
plotly
trafilatura
```

### 3. Konfigurasi Environment Variables (Opsional)

Jika Anda memiliki URL data source khusus:
1. Di Streamlit Cloud dashboard, masuk ke app settings
2. Tambahkan environment variable:
   - **Key**: `DATA_SOURCE_URL`
   - **Value**: URL sumber data Anda

### 4. Verifikasi Deploy

Setelah deploy:
1. Aplikasi akan tersedia di URL yang diberikan Streamlit Cloud
2. Biasanya format: `https://username-appname-hash.streamlit.app/`
3. Aplikasi akan otomatis restart jika ada perubahan di repository

### 5. Tips Deploy

- **Auto-deploy**: Setiap push ke branch main akan trigger redeploy otomatis
- **Logs**: Bisa dilihat di Streamlit Cloud dashboard untuk debugging
- **Custom domain**: Tersedia untuk Streamlit for Teams
- **Resource limits**: Community Cloud memiliki batasan memory dan CPU

### 6. Troubleshooting

Jika deploy gagal:
1. Cek logs di Streamlit Cloud dashboard
2. Pastikan semua dependencies tersedia
3. Verifikasi sintaks Python tidak ada error
4. Pastikan file `app.py` ada dan bisa dijalankan

### 7. Alternative: Deploy dari Replit

Untuk deploy langsung dari Replit:
1. Gunakan tombol "Deploy" di Replit
2. Pilih "Static deployment" atau "Autoscale deployment"
3. Aplikasi akan tersedia di subdomain `.replit.app`

## Status Aplikasi Saat Ini

✅ Aplikasi sudah siap deploy
✅ Konfigurasi Streamlit lengkap
✅ Branding Streamlit sudah dihilangkan
✅ Tema dark mobile-optimized
✅ Semua fungsi prediksi berjalan normal