import sqlite3

def get_connection():
    """Membuat koneksi ke database SQLite"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Membuat tabel-tabel utama & akun admin default jika belum ada"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabel Users (Pembaca, Penulis, Admin)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL  -- 'Pembaca', 'Penulis', atau 'Admin'
        )
    ''')

    # 2. Tabel Categories (Master Data Kategori/Genre oleh Admin)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_kategori TEXT UNIQUE NOT NULL
        )
    ''')

    # 3. Tabel Books (Terhubung ke id_kategori dan id_penulis)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            id_kategori INTEGER NOT NULL,
            sinopsis TEXT,
            id_penulis INTEGER NOT NULL,
            FOREIGN KEY (id_kategori) REFERENCES categories (id),
            FOREIGN KEY (id_penulis) REFERENCES users (id)
        )
    ''')

    # 4. Tabel Diaries (Gabungan Reading Tracker + Rating & Ulasan)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            tanggal_baca TEXT NOT NULL,
            status_read TEXT NOT NULL, -- 'First Time' atau 'Re-read'
            rating INTEGER,            -- Nilai 1-5 (opsional)
            isi_ulasan TEXT,           -- Teks ulasan (opsional)
            FOREIGN KEY (id_user) REFERENCES users (id),
            FOREIGN KEY (id_buku) REFERENCES books (id)
        )
    ''')

    # Seed akun Admin bawaan agar langsung bisa login sebagai Admin
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ('admin', 'admin123', 'Admin')
        )

    # Seed beberapa kategori awal agar tabel categories tidak kosong
    kategori_awal = ['Fiksi', 'Non-Fiksi', 'Teknologi', 'Sastra', 'Misteri']
    for kat in kategori_awal:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (nama_kategori) VALUES (?)",
            (kat,)
        )
        
    seed_dummy(cursor)

    conn.commit()
    conn.close()
    
def seed_dummy(cursor):
    """Mengisi data dummy awal jika database masih kosong"""
    # Cek apakah sudah ada data buku (sebagai penanda dummy sudah pernah diisi)
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] > 0:
        return  # Keluar jika data sudah ada agar tidak dobel saat program dijalankan ulang

    # 1. Tambah Akun Dummy (Selain 'admin' yang sudah dibuat di init_db)
    users_dummy = [
        ('tere_liye', '123', 'Penulis'),      # ID = 2
        ('andrea_hirata', '123', 'Penulis'),  # ID = 3
        ('username', 'password', 'Pembaca'),     # ID = 4
        ('ahmad', '123', 'Pembaca')     # ID = 5
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        users_dummy
    )

    # 2. Tambah Buku Dummy (id_kategori: 1=Fiksi, 2=Non-Fiksi, 3=Teknologi, 4=Sastra, 5=Misteri)
    books_dummy = [
        ('Bumi', 1, 'Petualangan Raib, Seli, dan Ali di dunia paralel.', 2),
        ('Pulang', 1, 'Kisah perjalanan Bujang menjadi tukang pukul keluarga Tong.', 2),
        ('Laskar Pelangi', 4, 'Perjuangan sepuluh anak Belitung menempuh pendidikan.', 3),
        ('Algoritma Python Dasar', 3, 'Panduan logika pemrograman untuk mahasiswa semester 1.', 3)
    ]
    cursor.executemany(
        "INSERT INTO books (judul, id_kategori, sinopsis, id_penulis) VALUES (?, ?, ?, ?)",
        books_dummy
    )

    # 3. Tambah Diary & Ulasan Dummy
    diaries_dummy = [
        (4, 1, '2026-10-15', 'First Time', 5, 'Seru banget! Dunia paralelnya imajinatif.'),
        (4, 3, '2026-11-02', 'Re-read', 5, 'Dibaca ulang tetap menyentuh dan menginspirasi.'),
        (5, 1, '2026-11-10', 'First Time', 4, 'Alurnya cepat dan bikin penasaran lanjut ke seri berikutnya.'),
        (5, 4, '2026-11-18', 'First Time', 5, 'Sangat membantu buat persiapan UAS Dasar Pemrograman!')
    ]
    cursor.executemany(
        """INSERT INTO diaries 
           (id_user, id_buku, tanggal_baca, status_read, rating, isi_ulasan) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        diaries_dummy
    )