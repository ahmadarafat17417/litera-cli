import sqlite3

def get_connection():
    # connect ke database sqlite
    conn = sqlite3.connect('database.db')
    # biar hasil query bisa diakses pakai nama kolom (kayak dict)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # bikin tabel kalau belum ada
    conn = get_connection()
    cursor = conn.cursor()

    # tabel user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL  -- 'Pembaca' atau 'Penulis'
        )
    ''')

    # tabel katalog buku
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            genre TEXT NOT NULL,
            sinopsis TEXT,
            id_penulis INTEGER NOT NULL,
            FOREIGN KEY (id_penulis) REFERENCES users (id)
        )
    ''')

    # tabel diary / catatan bacaan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            tanggal_baca TEXT NOT NULL,
            status_read TEXT NOT NULL, -- 'First Time' atau 'Re-read'
            FOREIGN KEY (id_user) REFERENCES users (id),
            FOREIGN KEY (id_buku) REFERENCES books (id)
        )
    ''')

    # tabel ulasan & rating
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            rating INTEGER NOT NULL,  -- 1 sampai 5
            isi_ulasan TEXT,
            tanggal_ulasan TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users (id),
            FOREIGN KEY (id_buku) REFERENCES books (id)
        )
    ''')

    conn.commit()
    conn.close()

# nyimpen data user yang lagi login
current_user = None

def menu_utama():
    # menu awal sebelum login
    while True:
        print("\n=================================")
        print("    SELAMAT DATANG DI LITERA     ")
        print("=================================")
        print("1. Register Akun Baru")
        print("2. Login")
        print("3. Keluar Aplikasi")
        print("=================================")
        
        pilihan = input("Pilih menu (1-3): ").strip()
        
        if pilihan == '1':
            print("\n[Fitur Register akan dipanggil di Langkah 3]")
        elif pilihan == '2':
            print("\n[Fitur Login akan dipanggil di Langkah 3]")
            # nanti kalau login sukses, panggil menu_setelah_login()
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan Litera. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid! Silakan masukkan angka 1, 2, atau 3.")

def menu_setelah_login():
    # menu utama setelah login, beda-beda tergantung role
    global current_user
    
    while current_user is not None:
        print(f"\n=================================")
        print(f" SELAMAT DATANG, {current_user['username'].upper()}!")
        print(f" Peran: {current_user['role']}")
        print("=================================")
        
        # menu buat penulis
        if current_user['role'] == 'Penulis':
            print("1. Tambah Buku Baru (Create)")
            print("2. Lihat Buku Saya (Read)")
            print("3. Edit Data Buku (Update)")
            print("4. Hapus Buku (Delete)")
            print("5. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-5): ").strip()
            if pilihan == '5':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print(f"\n[Fitur Penulis menu {pilihan} akan diisi di Langkah 5]")

        # menu buat pembaca
        elif current_user['role'] == 'Pembaca':
            print("1. Lihat & Cari Katalog Buku (Read)")
            print("2. Isi Catatan Diary Bacaan (Create)")
            print("3. Lihat Riwayat Diary Saya (Read)")
            print("4. Beri Ulasan & Rating Buku (Create)")
            print("5. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-5): ").strip()
            if pilihan == '5':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print(f"\n[Fitur Pembaca menu {pilihan} akan diisi di Langkah 5]")

if __name__ == '__main__':
    init_db()
    menu_utama()