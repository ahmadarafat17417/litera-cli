import sqlite3

def get_connection():
    """Membuat koneksi ke database SQLite"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Membuat tabel-tabel utama jika belum ada"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabel Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL  -- 'Pembaca' atau 'Penulis'
        )
    ''')

    # 2. Tabel Books
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

    # 3. Tabel Diaries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            tanggal_baca TEXT NOT NULL,
            status_read TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users (id),
            FOREIGN KEY (id_buku) REFERENCES books (id)
        )
    ''')

    # 4. Tabel Reviews
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_buku INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            isi_ulasan TEXT,
            tanggal_ulasan TEXT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES users (id),
            FOREIGN KEY (id_buku) REFERENCES books (id)
        )
    ''')

    conn.commit()
    conn.close()