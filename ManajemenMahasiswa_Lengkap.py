import streamlit as st
import pandas as pd
import re
import os

DATA_FILE = "data_mahasiswa.csv"

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="Manajemen Data Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS untuk mempercantik UI/UX, font, dan elemen form
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #13547a 0%, #80d0c7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #6c757d;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Form & Container card styling */
    div[data-testid="stForm"] {
        border-radius: 16px !important;
        border: 1px solid rgba(128, 208, 199, 0.3) !important;
        padding: 2rem !important;
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    /* Style dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- BACKEND LOGIC (OOP, Searching, Sorting) ---
class Mahasiswa:
    def __init__(self, nim, nama, email, jurusan, semester, ipk):
        self.__nim = nim
        self.__nama = nama
        self.__email = email
        self.__jurusan = jurusan
        self.__semester = semester
        self.__ipk = ipk

    def to_dict(self):
        return {
            "NIM": self.__nim,
            "Nama": self.__nama,
            "Email": self.__email,
            "Jurusan": self.__jurusan,
            "Semester": self.__semester,
            "IPK": self.__ipk
        }

    def status(self):
        return "Mahasiswa Aktif"


class MahasiswaBeasiswa(Mahasiswa):
    def status(self):
        return "Mahasiswa Beasiswa"


def load_data():
    try:
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE, dtype=str)
            if "Nilai" in df.columns and "IPK" not in df.columns:
                df = df.rename(columns={"Nilai": "IPK"})

            kolom = ["NIM", "Nama", "Email", "Jurusan", "Semester", "IPK", "Status"]
            for k in kolom:
                if k not in df.columns:
                    df[k] = ""
            return df[kolom]
        return pd.DataFrame(columns=["NIM", "Nama", "Email", "Jurusan", "Semester", "IPK", "Status"])
    except Exception as e:
        st.error(f"Error membaca file: {e}")
        return pd.DataFrame(columns=["NIM", "Nama", "Email", "Jurusan", "Semester", "IPK", "Status"])


def save_data(df):
    try:
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        st.error(f"Error menyimpan file: {e}")


def valid_nim(nim):
    return re.match(r"^[0-9]{5,15}$", nim)


def valid_nama(nama):
    return re.match(r"^[A-Za-z\s]+$", nama)


def valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)


def predikat_ipk(ipk):
    try:
        ipk = float(ipk)
        if ipk >= 3.75: return "🥇 Cumlaude"
        elif ipk >= 3.50: return "🟢 Sangat Memuaskan"
        elif ipk >= 3.00: return "🟡 Memuaskan"
        elif ipk >= 2.00: return "🟠 Cukup"
        else: return "🔴 Kurang"
    except Exception:
        return "-"


def linear_search(df, keyword):
    hasil = []
    for _, row in df.iterrows():
        if keyword.lower() in str(row["Nama"]).lower() or keyword in str(row["NIM"]):
            hasil.append(row)
    return pd.DataFrame(hasil)


def binary_search(df, nim):
    df_sorted = df.sort_values("NIM").reset_index(drop=True)
    kiri = 0
    kanan = len(df_sorted) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if df_sorted.loc[tengah, "NIM"] == nim:
            return pd.DataFrame([df_sorted.loc[tengah]])
        elif df_sorted.loc[tengah, "NIM"] < nim:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return pd.DataFrame()


def merge_sort_list(data, kolom):
    if len(data) <= 1: return data
    tengah = len(data) // 2
    kiri = merge_sort_list(data[:tengah], kolom)
    kanan = merge_sort_list(data[tengah:], kolom)
    hasil, i, j = [], 0, 0
    while i < len(kiri) and j < len(kanan):
        if str(kiri[i][kolom]) <= str(kanan[j][kolom]):
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def merge_sort(df, kolom):
    data = df.to_dict("records")
    return pd.DataFrame(merge_sort_list(data, kolom))


# --- SIDEBAR NAVIGATION ---
df = load_data()

with st.sidebar:
    st.markdown("<h2 style='text-align: center; font-weight: 800;'>🎓 Unand Apps</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.85rem; margin-bottom: 2rem;'>Sistem Informasi Akademik</p>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi Menu",
        ["🏠 Dashboard", "➕ Tambah Data", "▣ Tampilkan Data", "✎ Edit Data", "🗑 Hapus Data", "🔍 Pencarian Data", "↕ Pengurutan Data", "ⓘ Tentang Aplikasi"],
        label_visibility="collapsed"
    )

# --- MAIN CONTENT INTERFACE ---
def render_header(icon, title, desc):
    st.markdown(f"<div class='main-title'>{icon} {title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{desc}</div>", unsafe_allow_html=True)
    st.divider()


if "Dashboard" in menu:
    render_header("📊", "Dashboard", "Ringkasan data mahasiswa secara keseluruhan")
    
    # Penghitungan metrics statistik dasar
    rata_ipk = round(pd.to_numeric(df["IPK"], errors="coerce").mean(), 2) if not df.empty else 0.0
    total_jurusan = df["Jurusan"].nunique() if not df.empty else 0
    
    # Tampilan modern menggunakan st.metric bawaan yang rapi
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Total Mahasiswa Terdaftar", value=len(df), delta="Siswa Aktif")
    with m2:
        st.metric(label="Jumlah Jurusan", value=total_jurusan)
    with m3:
        st.metric(label="Rata-rata IPK Total", value=rata_ipk)

    st.subheader("▤ 5 Mahasiswa Terbaru")
    if not df.empty:
        df_tampil = df.copy().tail(5).reset_index(drop=True)
        df_tampil.index = df_tampil.index + 1
        df_tampil["Predikat IPK"] = df_tampil["IPK"].apply(predikat_ipk)
        st.dataframe(df_tampil, use_container_width=True)

        st.subheader("▦ Visualisasi Mahasiswa per Jurusan")
        st.bar_chart(df["Jurusan"].value_counts(), color="#80d0c7")
    else:
        st.info("Belum ada data mahasiswa yang tersimpan.")

elif "Tambah Data" in menu:
    render_header("➕", "Tambah Data Mahasiswa", "Masukkan data mahasiswa baru dengan validasi otomatis sistem")
    
    with st.form("form_tambah", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nim = st.text_input("Nomor Induk Mahasiswa (NIM)", placeholder="Contoh: 2111522001")
            nama = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
            email = st.text_input("Alamat Email", placeholder="Contoh: budi@student.unand.ac.id")
        with c2:
            jurusan = st.selectbox("Jurusan / Program Studi", ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"])
            semester = st.selectbox("Semester Berjalan", [str(i) for i in range(1, 9)])
            ipk = st.number_input("Indeks Prestasi Kumulatif (IPK)", min_value=0.00, max_value=4.00, step=0.01, format="%.2f")
            tipe = st.radio("Status Pembiayaan Kuliah", ["Mahasiswa Aktif", "Mahasiswa Beasiswa"], horizontal=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("Simpan Data Mahasiswa", type="primary", use_container_width=True)

    if submit:
        if not valid_nim(nim): st.error("❌ NIM harus berupa angka antara 5 sampai 15 digit.")
        elif not valid_nama(nama): st.error("❌ Nama hanya diperbolehkan kombinasi alfabet dan spasi.")
        elif not valid_email(email): st.error("❌ Format alamat Email tidak valid.")
        elif nim in df["NIM"].values: st.error("❌ Gagal! NIM sudah terdaftar di dalam sistem.")
        else:
            mhs = MahasiswaBeasiswa(nim, nama, email, jurusan, semester, ipk) if tipe == "Mahasiswa Beasiswa" else Mahasiswa(nim, nama, email, jurusan, semester, ipk)
            data_baru = mhs.to_dict()
            data_baru["Status"] = mhs.status()

            df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
            save_data(df)

            st.success(f"🎉 Sukses! Data mahasiswa {nama} berhasil disimpan ke sistem.")
            st.toast(f"Predikat Kelulusan: {predikat_ipk(ipk)}")
            st.balloons()

elif "Tampilkan Data" in menu:
    render_header("▣", "Daftar Mahasiswa", "Berikut adalah seluruh data registrasi mahasiswa terdaftar")
    
    if df.empty:
        st.warning("⚠️ Berkas database kosong atau belum diisi.")
    else:
        df_tampil = df.copy().reset_index(drop=True)
        df_tampil.index = df_tampil.index + 1
        df_tampil["Predikat IPK"] = df_tampil["IPK"].apply(predikat_ipk)
        
        # Penambahan fitur filter interaktif cepat di luar tabel
        search_query = st.text_input("⚡ Filter instan tabel (ketik nama/jurusan):", "")
        if search_query:
            df_tampil = df_tampil[df_tampil['Nama'].str.contains(search_query, case=False) | df_tampil['Jurusan'].str.contains(search_query, case=False)]
            
        st.dataframe(df_tampil, use_container_width=True, height=450)

elif "Edit Data" in menu:
    render_header("✎", "Modifikasi Data Mahasiswa", "Perbarui entri informasi internal mahasiswa berdasarkan NIM resmi")
    
    if df.empty:
        st.warning("⚠️ Database kosong. Tidak ada data yang dapat diubah.")
    else:
        pilih_nim = st.selectbox("Pilih NIM Mahasiswa yang ingin diubah:", df["NIM"].tolist())
        data_lama = df[df["NIM"] == pilih_nim].iloc[0]

        with st.form("form_edit"):
            st.info(f"Mengedit data untuk NIM: **{pilih_nim}**")
            c1, c2 = st.columns(2)
            with c1:
                nama = st.text_input("Nama Lengkap", data_lama["Nama"])
                email = st.text_input("Email", data_lama["Email"])
            with c2:
                jurusan = st.selectbox("Jurusan", ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"], 
                                     index=["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"].index(data_lama["Jurusan"]) if data_lama["Jurusan"] in ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"] else 0)
                semester = st.selectbox("Semester", [str(i) for i in range(1, 9)], 
                                      index=[str(i) for i in range(1, 9)].index(str(data_lama["Semester"])) if str(data_lama["Semester"]) in [str(i) for i in range(1, 9)] else 0)
            
            try: ipk_lama = float(data_lama["IPK"])
            except Exception: ipk_lama = 0.00
            
            ipk = st.number_input("IPK Terkini", min_value=0.00, max_value=4.00, value=ipk_lama, step=0.01, format="%.2f")
            submit = st.form_submit_button("Simpan Perubahan Data", type="primary", use_container_width=True)

        if submit:
            if not valid_nama(nama): st.error("❌ Format nama baru tidak valid.")
            elif not valid_email(email): st.error("❌ Format email baru tidak valid.")
            else:
                df.loc[df["NIM"] == pilih_nim, ["Nama", "Email", "Jurusan", "Semester", "IPK"]] = [nama, email, jurusan, semester, ipk]
                save_data(df)
                st.success("✅ Perubahan data mahasiswa berhasil diperbarui di database.")

elif "Hapus Data" in menu:
    render_header("🗑", "Penghapusan Data", "Menghapus berkas data mahasiswa secara permanen dari sistem")
    
    if df.empty:
        st.warning("⚠️ Tidak ada data untuk dihapus.")
    else:
        pilih_nim = st.selectbox("Pilih NIM Mahasiswa yang akan dikeluarkan:", df["NIM"].tolist())
        data_target = df[df["NIM"] == pilih_nim].iloc[0]
        
        st.warning(f"Apakah Anda yakin ingin menghapus data **{data_target['Nama']}** ({pilih_nim})? Tindakan ini tidak dapat dibatalkan.")
        
        if st.button("Ya, Hapus Permanen", type="primary", use_container_width=True):
            df = df[df["NIM"] != pilih_nim]
            save_data(df)
            st.success("💥 Data mahasiswa telah berhasil dihapus dari sistem storage.")
            st.rerun()

elif "Pencarian Data" in menu:
    render_header("🔍", "Mesin Pencari Data", "Temukan data spesifik via algoritma Linear & Binary Search")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        metode = st.selectbox("Pilih Algoritma Pencarian", ["Linear Search", "Binary Search"])
    with c2:
        keyword = st.text_input("Masukkan Kata Kunci (Nama atau NIM)", placeholder="Ketik kata kunci di sini...")

    if st.button("Mulai Proses Pencarian", type="primary", use_container_width=True):
        if not keyword.strip():
            st.warning("⚠️ Kolom kata kunci pencarian tidak boleh kosong.")
        else:
            hasil = linear_search(df, keyword) if metode == "Linear Search" else binary_search(df, keyword)
            
            if hasil.empty:
                st.error("🔍 Data tidak ditemukan. Periksa kembali kecocokan keyword Anda.")
            else:
                st.success(f"🎯 Ditemukan {len(hasil)} baris data yang cocok:")
                hasil = hasil.copy()
                hasil["Predikat IPK"] = hasil["IPK"].apply(predikat_ipk)
                st.dataframe(hasil, use_container_width=True)

elif "Pengurutan Data" in menu:
    render_header("↕", "Modul Sorting Data", "Mengurutkan susunan tabel data menggunakan algoritma pilihan")
    
    c1, c2 = st.columns(2)
    with c1:
        kolom = st.selectbox("Urutkan Berdasarkan Kolom", ["NIM", "Nama", "Jurusan", "Semester", "IPK"])
    with c2:
        metode_sort = st.selectbox("Pilih Algoritma", ["Merge Sort (Rekomendasi - Cepat)", "Bubble Sort (Konvensional)"])

    if st.button("Eksekusi Pengurutan", type="primary", use_container_width=True):
        if df.empty:
            st.warning("⚠️ Data kosong, proses sorting dibatalkan.")
        else:
            with st.spinner("Sedang memproses struktur urutan data..."):
                hasil = merge_sort(df, kolom) if "Merge" in metode_sort else bubble_sort(df, kolom)
            st.success(f"✅ Data berhasil diurutkan berdasarkan kriteria **{kolom}**")
            hasil["Predikat IPK"] = hasil["IPK"].apply(predikat_ipk)
            st.dataframe(hasil, use_container_width=True)

elif "Tentang Aplikasi" in menu:
    render_header("ⓘ", "Informasi Sistem", "Detail arsitektur pemrograman dan fitur aplikasi UAS")
    
    tab1, tab2 = st.tabs(["📋 Fitur & Konsep OOP", "📈 Kompleksitas Algoritma"])
    
    with tab1:
        st.write("""
        Sistem manajemen data ini dirancang mengimplementasikan aspek fundamental arsitektur perangkat lunak modern:
        - **Penyimpanan Utama:** Menggunakan berkas File I/O CSV (`data_mahasiswa.csv`).
        - **Konsep OOP Dasar:** Terdiri dari penerapan *Class, Object, Encapsulation* (Private atribut), *Inheritance*, dan *Polymorphism* pada sub-kelas status mahasiswa.
        - **Validasi Mutu:** Integrasi mesin Regex untuk penyaringan input Nama, Email, dan batasan digit NIM.
        """)
        
        st.subheader("Ketentuan Klasterisasi Predikat IPK")
        st.table({
            "Rentang Batas Nilai IPK": ["3.75 - 4.00", "3.50 - 3.74", "3.00 - 3.49", "2.00 - 2.99", "0.00 - 1.99"],
            "Predikat Akademis": ["🥇 Cumlaude", "🟢 Sangat Memuaskan", "🟡 Memuaskan", "Cukup", "Kurang"]
        })

    with tab2:
        st.subheader("Estimasi Efisiensi & Time Complexity")
        st.markdown("Berikut performa algoritma pencarian dan pengurutan yang terpasang di sistem backend:")
        st.table({
            "Nama Algoritma / Fitur": ["Linear Search", "Binary Search", "Bubble Sort", "Merge Sort"],
            "Notasi Big O (Complexity)": ["O(n)", "O(log n)", "O(n²)", "O(n log n)"]
        })
