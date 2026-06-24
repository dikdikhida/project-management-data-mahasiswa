import os
import re
import streamlit as st


class Person:
    """Kelas Induk (Abstract Base Class Concept)"""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name


class Student(Person):
    """Kelas Turunan (Pewarisan dari Person)"""
    def __init__(self, name: str, nim: str, email: str, gpa: float):
        super().__init__(name)
        self._nim = nim
        self._email = email
        self._gpa = float(gpa)

    @property
    def nim(self) -> str:
        return self._nim

    @nim.setter
    def nim(self, nim: str):
        self._nim = nim

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def gpa(self) -> float:
        return self._gpa

    @gpa.setter
    def gpa(self, gpa: float):
        self._gpa = float(gpa)


def validate_nim(nim: str) -> bool:
    return bool(re.match(r"^\d{10}$", nim))

def validate_email(email: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def validate_gpa(gpa: float) -> bool:
    return 0.0 <= gpa <= 4.0

def save_to_file(students: list, filename: str):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for student in students:
                f.write(f"{student.name},{student.nim},{student.email},{float(student.gpa)}\n")
    except IOError as e:
        st.error(f"Gagal menulis data ke file: {e}")

def load_from_file(filename: str) -> list:
    students = []
    if not os.path.exists(filename):
        return students
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 4:
                    try:
                        name, nim, email, gpa_str = parts
                        students.append(Student(name, nim, email, float(gpa_str)))
                    except ValueError:
                        continue
    except IOError as e:
        st.warning(f"Gagal membaca file: {e}")
    return students


def bubble_sort_by_gpa(arr: list):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j].gpa < arr[j + 1].gpa:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def insertion_sort_by_nim(arr: list):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].nim > key.nim:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def sequential_search_by_name(arr: list, target_name: str) -> int:
    for i in range(len(arr)):
        if arr[i].name.lower() == target_name.lower():
            return i
    return -1

def binary_search_by_nim(arr: list, target_nim: str) -> int:
    insertion_sort_by_nim(arr)
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid].nim == target_nim:
            return mid
        elif arr[mid].nim < target_nim:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def main():
    st.set_page_config(page_title="My Dashboard", layout="wide")
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600;700&display=swap');
            html, body, [data-testid="stSidebar"] {
                font-family: 'Inter', sans-serif;
            }
            
            .main-title {
                background: linear-gradient(135deg, #6366F1 0%, #3B82F6 50%, #06B6D4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                font-size: 2.6rem;
                line-height: 1.3;
                margin-top: 0.5rem;
                margin-bottom: 0.2rem;
            }
            
            button[data-baseweb="tab"] {
                font-weight: 600 !important;
                color: #4B5563 !important;
            }
            button[data-baseweb="tab"][aria-selected="true"] {
                color: #3B82F6 !important;
                border-bottom-color: #3B82F6 !important;
                background-color: #EFF6FF !important;
                border-radius: 8px 8px 0px 0px;
            }
            
            .custom-card {
                background: #ffffff;
                border-radius: 16px;
                padding: 1.5rem;
                transition: all 0.3s ease;
            }
            .card-blue { border-left: 5px solid #3B82F6; border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB; }
            .card-emerald { border-left: 5px solid #10B981; border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB; }
            .card-purple { border-left: 5px solid #8B5CF6; border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB; }
            
            .custom-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            }
            
            .card-label {
                color: #6B7280;
                font-size: 0.85rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .card-value {
                color: #1F2937;
                font-size: 2.1rem;
                font-weight: 700;
                margin-top: 0.25rem;
            }
            
            /* Trik CSS untuk membuat tombol khusus di Tab Hapus berwarna merah bahaya */
            div.stButton > button:first-child[dir="ltr"] {
                border-color: #EF4444 !important;
                color: #EF4444 !important;
            }
            div.stButton > button:first-child[dir="ltr"]:hover {
                background-color: #FEF2F2 !important;
                color: #DC2626 !important;
            }
            
            .block-container {
                padding-top: 3.5rem !important;
                padding-bottom: 2rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    filename = "mahasiswa.txt"

    if 'students' not in st.session_state:
        st.session_state.students = load_from_file(filename)

    def get_dataframe_data(student_list):
        return [
            {"NIM": s.nim, "Nama": s.name, "Email": s.email, "GPA": float(s.gpa)} 
            for s in student_list
        ]

    st.markdown('<p class="main-title">Manajemen Data Mahasiswa Unpam</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280; margin-top:-5px; font-size:1.1rem;">"Sistem Manajemen Mahasiswa kelas 03TPLE003"</p>', unsafe_allow_html=True)

    total_mhs = len(st.session_state.students)
    avg_gpa = sum(float(s.gpa) for s in st.session_state.students) / total_mhs if total_mhs > 0 else 0.0
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""
            <div class="custom-card card-blue">
                <div class="card-label" style="color: #3B82F6;"> Total Mahasiswa</div>
                <div class="card-value">{total_mhs} <span style="font-size:1rem; font-weight:400; color:#9CA3AF;">Aktif</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
            <div class="custom-card card-emerald">
                <div class="card-label" style="color: #10B981;"> Rata-Rata IPK (GPA)</div>
                <div class="card-value" style="color: #059669;">{avg_gpa:.2f} <span style="font-size:1rem; font-weight:400; color:#A7F3D0;">/ 4.00</span></div>
            </div>
        """, unsafe_allow_html=True)
    with col_s3:
        status_color = "#8B5CF6" if os.path.exists(filename) else "#EF4444"
        status_text = "Tersinkronisasi" if os.path.exists(filename) else "Lokal"
        st.markdown(f"""
            <div class="custom-card card-purple">
                <div class="card-label" style="color: #8B5CF6;"> Basis Data (TXT)</div>
                <div class="card-value" style="color: {status_color};">{status_text}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")


    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        " Data Center", 
        " Tambah Akun", 
        " Edit", 
        " Hapus", 
        " Pencarian Cepat", 
        " Penyaringan Urutan"
    ])

    with tab1:
        st.markdown("<h3 style='color:#1E3A8A; margin-bottom:1rem;'> Database Mahasiswa Terdaftar</h3>", unsafe_allow_html=True)
        if not st.session_state.students:
            st.info("Belum ada entri data terdeteksi. Silakan tambah data baru terlebih dahulu.")
        else:
            st.dataframe(
                get_dataframe_data(st.session_state.students), 
                use_container_width=True,
                column_config={
                    "NIM": st.column_config.TextColumn("Nomor Induk Mahasiswa"),
                    "Nama": st.column_config.TextColumn("Nama Lengkap"),
                    "Email": st.column_config.LinkColumn("Surat Elektronik (Email)"),
                    "GPA": st.column_config.ProgressColumn(
                        "GPA / IPK", 
                        min_value=0.0, 
                        max_value=4.0, 
                        format="%.2f",
                        color="blue"
                    )
                }
            )

    with tab2:
        st.markdown("<h3 style='color:#1E3A8A;'> Tambah Akuntabilitas Mahasiswa</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            with st.form("form_tambah_modern", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Nama Lengkap", placeholder="Masukkan nama tanpa gelar").strip()
                    nim = st.text_input("NIM (10 digit)", placeholder="Contoh: 1234567890").strip()
                with c2:
                    email = st.text_input("Alamat Email", placeholder="contoh@domain.com").strip()
                    gpa = st.number_input("IPK Terakhir", min_value=0.0, max_value=4.0, step=0.01, format="%.2f")
                
                st.write("")
                submitted = st.form_submit_button(" Daftarkan Mahasiswa", use_container_width=True, type="primary")
                
                if submitted:
                    if not name: st.error("Kolom nama wajib diisi!")
                    elif not validate_nim(nim): st.error("NIM ditolak! Harus berupa kombinasi 10 digit angka asli.")
                    elif any(s.nim == nim for s in st.session_state.students): st.error("NIM duplikat terdeteksi!")
                    elif not validate_email(email): st.error("Format domain email salah.")
                    else:
                        new_student = Student(name, nim, email, float(gpa))
                        st.session_state.students.append(new_student)
                        save_to_file(st.session_state.students, filename)
                        st.success(f"Data mahasiswa {name} berhasil diamankan!")
                        st.toast(f"Sukses mendaftarkan {name}!")
                        st.rerun()

    with tab3:
        st.markdown("<h3 style='color:#1E3A8A;'> Perbarui Data Terpilih</h3>", unsafe_allow_html=True)
        target_nim = st.text_input("Masukkan NIM Akun Sasaran Modifikasi:", key="edit_nim_key").strip()
        
        idx = next((i for i, s in enumerate(st.session_state.students) if s.nim == target_nim), -1)
        
        if target_nim and idx == -1:
            st.error("NIM Tidak ditemukan.")
        elif idx != -1:
            mhs = st.session_state.students[idx]
            st.info(f"Data Ditemukan! Mengedit profil untuk: **{mhs.name}**")
            
            with st.form("form_edit_modern"):
                cx, cy = st.columns(2)
                with cx:
                    new_name = st.text_input("Edit Nama Lengkap", value=mhs.name).strip()
                    new_email = st.text_input("Edit Email Hubungan", value=mhs.email).strip()
                with cy:
                    new_gpa = st.number_input("Sesuaikan Nilai GPA", min_value=0.0, max_value=4.0, value=float(mhs.gpa), step=0.01, format="%.2f")
                
                st.write("")
                saved = st.form_submit_button(" Terapkan Perubahan", use_container_width=True, type="primary")
                if saved:
                    if not validate_email(new_email):
                        st.error("Email modifikasi tidak valid!")
                    else:
                        st.session_state.students[idx].name = new_name
                        st.session_state.students[idx].email = new_email
                        st.session_state.students[idx].gpa = float(new_gpa)
                        save_to_file(st.session_state.students, filename)
                        st.success("Sinkronisasi data modifikasi berhasil diselesaikan.")
                        st.rerun()

    with tab4:
        st.markdown("<h3 style='color:#DC2626;'> Hapus Entri Data</h3>", unsafe_allow_html=True)
        del_nim = st.text_input("Ketikkan NIM yang ingin dieliminasi secara permanen:", key="del_nim_key").strip()
        
        idx = next((i for i, s in enumerate(st.session_state.students) if s.nim == del_nim), -1)
        
        if del_nim and idx == -1:
            st.error("NIM Mahasiswa salah atau tidak ada.")
        elif idx != -1:
            mhs = st.session_state.students[idx]
            st.write("")
            st.warning(f"Tindakan Berbahaya: Anda akan menghapus data atas nama **{mhs.name}** secara permanen dari server.")
            st.write("")
            
            # FUNGSI CALLBACK: Dipanggil saat tombol ditekan untuk menghapus data & mereset state kolom NIM dengan aman
            def proses_hapus_data():
                st.session_state.students.pop(idx)
                save_to_file(st.session_state.students, filename)
                st.session_state["del_nim_key"] = ""  # Mengosongkan kolom input
                st.toast("Data Dihapus",)
            
            st.button(
                "Konfirmasi Pembuangan Data", 
                type="primary", 
                use_container_width=True, 
                on_click=proses_hapus_data
            )

    with tab5:
        st.markdown("<h3 style='color:#1E3A8A;'> Mesin Pencari Data</h3>", unsafe_allow_html=True)
        method = st.pills("Metode Engine:", ["Sequential Search (Nama)", "Binary Search (NIM)"], default="Sequential Search (Nama)")
        
        if "Nama" in method:
            s_name = st.text_input("Cari Berdasarkan Karakter Nama:", placeholder="Ketik nama di sini...")
            if s_name:
                res = sequential_search_by_name(st.session_state.students, s_name)
                if res != -1:
                    st.success(f"Ditemukan pada indeks array ke-{res}")
                    st.dataframe(get_dataframe_data([st.session_state.students[res]]), use_container_width=True)
                else:
                    st.error("Nama tidak cocok dengan database kami.")
                    
        elif "NIM" in method:
            s_nim = st.text_input("Cari Berdasarkan Angka NIM Pas:", placeholder="Ketik 10 digit angka...")
            if s_nim:
                res = binary_search_by_nim(st.session_state.students, s_nim)
                if res != -1:
                    st.success("Target berhasil diisolasi melalui Binary Search!")
                    st.dataframe(get_dataframe_data([st.session_state.students[res]]), use_container_width=True)
                else:
                    st.error("NIM tidak ditemukan dalam struktur pohon pencarian.")

    with tab6:
        st.markdown("<h3 style='color:#1E3A8A;'> Strukturisasi & Pengurutan Algoritma</h3>", unsafe_allow_html=True)
        rule = st.radio("Aturan Algoritma Pengurutan:", [
            "Urutkan GPA Tertinggi ke Terendah (Bubble Sort - Descending)", 
            "Urutkan NIM Terkecil ke Terbesar (Insertion Sort - Ascending)"
        ], horizontal=True)
        
        if st.button("Eksekusi Penyusunan Ulang", type="primary", use_container_width=True):
            with st.spinner("Memetakan ulang struktur memori..."):
                if "GPA" in rule:
                    bubble_sort_by_gpa(st.session_state.students)
                    st.toast("Bubble Sort Selesai!")
                else:
                    insertion_sort_by_nim(st.session_state.students)
                    st.toast("Insertion Sort Selesai!")
                
                save_to_file(st.session_state.students, filename)
                st.dataframe(get_dataframe_data(st.session_state.students), use_container_width=True)

if __name__ == "__main__":
    main()
