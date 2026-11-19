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

    conn.commit()
    conn.close()