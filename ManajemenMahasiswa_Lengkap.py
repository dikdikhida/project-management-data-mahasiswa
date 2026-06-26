import streamlit as st
import pandas as pd
import re
import os

DATA_FILE = "data_mahasiswa.csv"

st.set_page_config(
    page_title="Manajemen Data Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

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
        if ipk >= 3.75:
            return "🥇 Cumlaude"
        elif ipk >= 3.50:
            return "🟢 Sangat Memuaskan"
        elif ipk >= 3.00:
            return "🟡 Memuaskan"
        elif ipk >= 2.00:
            return "🟠 Cukup"
        else:
            return "🔴 Kurang"
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


def bubble_sort(df, kolom):
    data = df.to_dict("records")
    n = len(data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if str(data[j][kolom]) > str(data[j + 1][kolom]):
                data[j], data[j + 1] = data[j + 1], data[j]

    return pd.DataFrame(data)


def merge_sort_list(data, kolom):
    if len(data) <= 1:
        return data

    tengah = len(data) // 2
    kiri = merge_sort_list(data[:tengah], kolom)
    kanan = merge_sort_list(data[tengah:], kolom)

    hasil = []
    i = 0
    j = 0

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


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #ffffff;
    }

    .block-container {
        max-width: 100% !important;
        padding-top: 1.2rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.6rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Layout utama: kolom menu kiri diberi batas biru */
/* PANEL MENU */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child{
    background:#0F4C81;
    border-right:4px solid #2F80ED;
    min-height:100vh;
    padding:20px 15px !important;
    border-radius:0 15px 15px 0;
    box-shadow:5px 0 20px rgba(0,0,0,.12);
}

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        padding-left: 28px !important;
    }

    .brand-box {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 8px 2px 18px 2px;
        margin-bottom: 14px;
        border-bottom: 1px solid #e5e7eb;
    }

    .brand-icon {
        font-size: 36px;
        color: #0d6efd;
        line-height: 1;
    }

    .brand-text .top {
        color: #6CB4FF;
        font-weight: 800;
        font-size: 15px;
        line-height: 1.25;
    }

    .brand-text .bottom {
        color: white;
        font-weight: 800;
        font-size: 15px;
        line-height: 1.45;
    }

    .menu-title {
        color: #A7D3FF;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: .4px;
        margin: 6px 0 8px 0;
    }

    /* Tombol menu: font kecil dan jarak rapat */
    div[data-testid="stButton"]>button{
    width:100%;
    height:42px;
    background:transparent!important;
    color:white!important;
    border:none!important;
    border-radius:10px;
    justify-content:flex-start!important;
    padding-left:16px!important;
    font-size:14px!important;
    font-weight:500;
    transition:.25s;
}

div[data-testid="stButton"]>button:hover{
    background:#2F80ED!important;
    color:white!important;
}

div[data-testid="stButton"]>button[kind="primary"]{
    background:#2F80ED!important;
    color:white!important;
    font-weight:700;
    box-shadow:0 8px 18px rgba(47,128,237,.35);
}

    .page-title {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 28px;
        margin-bottom: 4px;
    }

    .page-title .icon {
        font-size: 38px;
    }

    .page-title h1 {
        margin: 0;
        color: #111827;
        font-size: 36px;
        font-weight: 800;
        line-height: 1.1;
    }

    .page-desc {
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 28px;
    }

    .cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 22px;
        margin-bottom: 32px;
    }

    .card {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 30px 32px;
        display: flex;
        align-items: center;
        gap: 28px;
        min-height: 120px;
        box-shadow: 0 2px 8px rgba(15,23,42,.06);
        background: white;
    }

    .card-icon {
        width: 76px;
        height: 76px;
        border-radius: 11px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 36px;
    }

    .blue-bg { background: #e8f1ff; color: #0d6efd; }
    .green-bg { background: #dff8e8; color: #16a34a; }
    .purple-bg { background: #f0e3ff; color: #7e22ce; }

    .card-label {
        color: #374151;
        font-size: 15px;
        margin-bottom: 8px;
    }

    .card-value {
        color: #0d6efd;
        font-size: 32px;
        font-weight: 800;
        line-height: 1;
    }

    .card-small {
        color: #6b7280;
        font-size: 14px;
        margin-top: 10px;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
        margin-bottom: 2px;
    }

    .section-title span {
        font-size: 30px;
        color: #0d6efd;
    }

    .section-title h2 {
        margin: 0;
        font-size: 24px;
        color: #111827;
        font-weight: 800;
    }

    .section-desc {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Dataframe agar lebih rapi */
    div[data-testid="stDataFrame"] {
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid #dbe4f0 !important;
    }

    h1, h2, h3 {
        color: #111827;
        font-weight: 800 !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 9px !important;
    }

    @media (max-width: 900px) {
        .cards { grid-template-columns: 1fr; }
        .page-title h1 { font-size: 28px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


df = load_data()

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


def menu_button(label, target):
    tipe = "primary" if st.session_state.menu == target else "secondary"
    if st.button(label, use_container_width=True, type=tipe):
        st.session_state.menu = target
        st.rerun()


def show_title(icon, title, desc):
    st.markdown(
        f"""
        <div class="page-title">
            <div class="icon">{icon}</div>
            <h1>{title}</h1>
        </div>
        <div class="page-desc">{desc}</div>
        """,
        unsafe_allow_html=True
    )


col_menu, col_isi = st.columns([1.05, 4.2], gap="large")


with col_menu:
    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-icon">🎓</div>
            <div class="brand-text">
                <div class="top">Aplikasi</div>
                <div class="bottom">Manajemen Data<br>Mahasiswa</div>
            </div>
        </div>
        <div class="menu-title">MENU</div>
        """,
        unsafe_allow_html=True
    )

    menu_button("🏠   Dashboard", "Dashboard")
    menu_button("➕   Tambah Data", "Tambah Data")
    menu_button("▣   Data Mahasiswa", "Tampilkan Data")
    menu_button("✎   Edit Data", "Edit Data")
    menu_button("🗑   Hapus Data", "Hapus Data")
    menu_button("🔍   Pencarian", "Pencarian")
    menu_button("↕   Pengurutan", "Pengurutan")
    menu_button("ⓘ   Tentang Aplikasi", "Tentang Program")

menu = st.session_state.menu


with col_isi:

    if menu == "Dashboard":
        show_title("📊", "Dashboard", "Ringkasan data mahasiswa secara keseluruhan")

        rata_ipk = round(pd.to_numeric(df["IPK"], errors="coerce").mean(), 2) if not df.empty else 0
        total_jurusan = df["Jurusan"].nunique() if not df.empty else 0

        st.markdown(
            f"""
            <div class="cards">
                <div class="card">
                    <div class="card-icon blue-bg">👥</div>
                    <div>
                        <div class="card-label">Total Mahasiswa</div>
                        <div class="card-value">{len(df)}</div>
                        <div class="card-small">Mahasiswa terdaftar</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-icon green-bg">🏢</div>
                    <div>
                        <div class="card-label">Jumlah Jurusan</div>
                        <div class="card-value" style="color:#16a34a;">{total_jurusan}</div>
                        <div class="card-small">Jurusan tersedia</div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-icon purple-bg">☆</div>
                    <div>
                        <div class="card-label">Rata-rata IPK</div>
                        <div class="card-value" style="color:#7e22ce;">{rata_ipk}</div>
                        <div class="card-small">Rata-rata IPK keseluruhan</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="section-title"><span>▤</span><h2>Data Terbaru</h2></div>
            <div class="section-desc">5 data mahasiswa terbaru</div>
            """,
            unsafe_allow_html=True
        )

        if not df.empty:
            df_tampil = df.copy().tail(5).reset_index(drop=True)
            df_tampil.index = df_tampil.index + 1
            df_tampil["Predikat IPK"] = df_tampil["IPK"].apply(predikat_ipk)
            st.dataframe(df_tampil, use_container_width=True, height=245)

            st.markdown(
                """
                <div class="section-title" style="margin-top:36px;"><span>▦</span><h2>Grafik Jumlah Mahasiswa per Jurusan</h2></div>
                <div class="section-desc">Visualisasi jumlah mahasiswa berdasarkan jurusan</div>
                """,
                unsafe_allow_html=True
            )
            st.bar_chart(df["Jurusan"].value_counts())
        else:
            st.info("Belum ada data mahasiswa.")

    elif menu == "Tambah Data":
        show_title("➕", "Tambah Data Mahasiswa", "Masukkan data mahasiswa baru dengan validasi otomatis")

        with st.form("form_tambah"):
            nim = st.text_input("NIM")
            nama = st.text_input("Nama")
            email = st.text_input("Email")
            jurusan = st.selectbox("Jurusan", ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"])
            semester = st.selectbox("Semester", ["1", "2", "3", "4", "5", "6", "7", "8"])
            ipk = st.number_input("IPK", min_value=0.00, max_value=4.00, step=0.01, format="%.2f")
            tipe = st.radio("Status", ["Mahasiswa Aktif", "Mahasiswa Beasiswa"])
            submit = st.form_submit_button("Simpan Data")

        if submit:
            try:
                if not valid_nim(nim):
                    st.error("NIM harus angka minimal 5 digit.")
                elif not valid_nama(nama):
                    st.error("Nama hanya boleh huruf dan spasi.")
                elif not valid_email(email):
                    st.error("Format email tidak valid.")
                elif nim in df["NIM"].values:
                    st.error("NIM sudah terdaftar.")
                else:
                    if tipe == "Mahasiswa Beasiswa":
                        mhs = MahasiswaBeasiswa(nim, nama, email, jurusan, semester, ipk)
                    else:
                        mhs = Mahasiswa(nim, nama, email, jurusan, semester, ipk)

                    data_baru = mhs.to_dict()
                    data_baru["Status"] = mhs.status()

                    df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
                    save_data(df)

                    st.success("Data mahasiswa berhasil ditambahkan.")
                    st.info(f"Predikat IPK: {predikat_ipk(ipk)}")
                    st.balloons()
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

    elif menu == "Tampilkan Data":
        show_title("▣", "Data Mahasiswa", "Daftar lengkap data mahasiswa yang tersimpan")

        if df.empty:
            st.warning("Data masih kosong.")
        else:
            df_tampil = df.copy().reset_index(drop=True)
            df_tampil.index = df_tampil.index + 1
            df_tampil["Predikat IPK"] = df_tampil["IPK"].apply(predikat_ipk)
            st.dataframe(df_tampil, use_container_width=True)

    elif menu == "Edit Data":
        show_title("✎", "Edit Data Mahasiswa", "Perbarui data mahasiswa berdasarkan NIM")

        if df.empty:
            st.warning("Data masih kosong.")
        else:
            pilih_nim = st.selectbox("Pilih NIM", df["NIM"].tolist())
            data_lama = df[df["NIM"] == pilih_nim].iloc[0]

            with st.form("form_edit"):
                nama = st.text_input("Nama", data_lama["Nama"])
                email = st.text_input("Email", data_lama["Email"])
                jurusan = st.selectbox(
                    "Jurusan",
                    ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"],
                    index=["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"].index(data_lama["Jurusan"]) if data_lama["Jurusan"] in ["Teknik Informatika", "Sistem Informasi", "Manajemen Informatika"] else 0
                )
                semester = st.selectbox(
                    "Semester",
                    ["1", "2", "3", "4", "5", "6", "7", "8"],
                    index=["1", "2", "3", "4", "5", "6", "7", "8"].index(str(data_lama["Semester"])) if str(data_lama["Semester"]) in ["1", "2", "3", "4", "5", "6", "7", "8"] else 0
                )

                try:
                    ipk_lama = float(data_lama["IPK"])
                except Exception:
                    ipk_lama = 0.00

                ipk = st.number_input("IPK", min_value=0.00, max_value=4.00, value=ipk_lama, step=0.01, format="%.2f")
                submit = st.form_submit_button("Update Data")

            if submit:
                if not valid_nama(nama):
                    st.error("Nama tidak valid.")
                elif not valid_email(email):
                    st.error("Email tidak valid.")
                else:
                    df.loc[df["NIM"] == pilih_nim, ["Nama", "Email", "Jurusan", "Semester", "IPK"]] = [nama, email, jurusan, semester, ipk]
                    save_data(df)
                    st.success("Data berhasil diperbarui.")
                    st.info(f"Predikat IPK terbaru: {predikat_ipk(ipk)}")

    elif menu == "Hapus Data":
        show_title("🗑", "Hapus Data Mahasiswa", "Hapus data mahasiswa yang sudah tidak diperlukan")

        if df.empty:
            st.warning("Data masih kosong.")
        else:
            pilih_nim = st.selectbox("Pilih NIM yang akan dihapus", df["NIM"].tolist())

            if st.button("Hapus Data", type="primary"):
                df = df[df["NIM"] != pilih_nim]
                save_data(df)
                st.success("Data berhasil dihapus.")

    elif menu == "Pencarian":
        show_title("🔍", "Pencarian Data", "Cari mahasiswa menggunakan Linear Search atau Binary Search")

        metode = st.selectbox("Pilih Metode", ["Linear Search", "Binary Search"])
        keyword = st.text_input("Masukkan Nama atau NIM")

        if st.button("Cari", type="primary"):
            if keyword.strip() == "":
                st.warning("Masukkan keyword terlebih dahulu.")
            else:
                if metode == "Linear Search":
                    hasil = linear_search(df, keyword)
                else:
                    hasil = binary_search(df, keyword)

                if hasil.empty:
                    st.warning("Data tidak ditemukan.")
                else:
                    hasil = hasil.copy()
                    hasil["Predikat IPK"] = hasil["IPK"].apply(predikat_ipk)
                    st.dataframe(hasil, use_container_width=True)

    elif menu == "Pengurutan":
        show_title("↕", "Pengurutan Data", "Urutkan data mahasiswa menggunakan algoritma sorting")

        kolom = st.selectbox("Urutkan berdasarkan", ["NIM", "Nama", "Jurusan", "Semester", "IPK"])

        if st.button("Urutkan Data", type="primary"):
            if df.empty:
                st.warning("Data masih kosong.")
            else:
                hasil = merge_sort(df, kolom)

                hasil["Predikat IPK"] = hasil["IPK"].apply(predikat_ipk)
                st.dataframe(hasil, use_container_width=True)

    elif menu == "Tentang Program":
        show_title("ⓘ", "Tentang Aplikasi", "Informasi fitur dan konsep pemrograman yang digunakan")

        st.write("""
        Aplikasi ini dibuat untuk memenuhi tugas UAS Manajemen Data Mahasiswa berbasis web.

        Fitur yang digunakan:
        - Input, edit, hapus, dan tampilkan data mahasiswa
        - Penyimpanan data menggunakan File I/O CSV
        - OOP: class, object, encapsulation, inheritance, polymorphism
        - Searching: Linear Search dan Binary Search
        - Sorting: Bubble Sort dan Merge Sort
        - Regex validation
        - Error handling menggunakan try-except
        - Time Complexity
        - IPK menggunakan skala 0.00 sampai 4.00 seperti dunia perkuliahan
        """)

        st.subheader("Predikat IPK")
        st.table({
            "Rentang IPK": ["3.75 - 4.00", "3.50 - 3.74", "3.00 - 3.49", "2.00 - 2.99", "0.00 - 1.99"],
            "Predikat": ["Cumlaude", "Sangat Memuaskan", "Memuaskan", "Cukup", "Kurang"]
        })

        st.subheader("Estimasi Time Complexity")
        st.table({
            "Fitur": ["Linear Search", "Binary Search", "Bubble Sort", "Merge Sort"],
            "Complexity": ["O(n)", "O(log n)", "O(n²)", "O(n log n)"]
        })
