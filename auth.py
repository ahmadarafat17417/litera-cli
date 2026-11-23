import sqlite3
from database import get_connection

def register():
    """Mendaftarkan akun pengguna baru (Pembaca atau Penulis)"""
    print("\n--- REGISTER AKUN BARU ---")
    username = input("Masukkan Username: ").strip()
    password = input("Masukkan Password: ").strip()

    if not username or not password:
        print("Error: Username dan password tidak boleh kosong!")
        return

    print("Pilih Peran (Role):")
    print("1. Pembaca")
    print("2. Penulis")
    pilihan_role = input("Pilih (1/2): ").strip()

    if pilihan_role == '1':
        role = 'Pembaca'
    elif pilihan_role == '2':
        role = 'Penulis'
    else:
        print("Error: Pilihan peran tidak valid! Registrasi dibatalkan.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        print(f"\nBerhasil! Akun '{username}' sebagai {role} telah terdaftar. Silakan login.")
    except sqlite3.IntegrityError:
        # Muncul otomatis jika username sudah ada karena kolom username bertipe UNIQUE
        print(f"\nError: Username '{username}' sudah digunakan! Silakan pilih username lain.")
    finally:
        conn.close()


def login():
    """Memverifikasi kredensial pengguna saat masuk aplikasi"""
    print("\n--- LOGIN LITERA ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\nLogin berhasil! Halo, {user['username']}.")
        # Mengubah sqlite3.Row menjadi dictionary biasa agar mudah dipakai di main.py
        return dict(user)
    else:
        print("\nLogin gagal! Username atau password salah.")
        return None


def lihat_profil(user_id):
    """Menampilkan profil pengguna, statistik (jika Pembaca), dan opsi edit profil"""
    while True:
        conn = get_connection()
        cursor = conn.cursor()

        # Ambil data terbaru user
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            print("\nError: Data pengguna tidak ditemukan.")
            conn.close()
            return

        print("\n=================================")
        print("          PROFIL PENGGUNA        ")
        print("=================================")
        print(f"Username : {user['username']}")
        print(f"Role     : {user['role']}")

        # Tampilkan statistik ala Letterboxd jika role adalah Pembaca
        if user['role'] == 'Pembaca':
            # 1. Total semua buku yang dicatat di diary
            cursor.execute("SELECT COUNT(*) FROM diaries WHERE id_user = ?", (user_id,))
            total_baca = cursor.fetchone()[0]

            # 2. Total buku dibaca tahun ini (2026)
            cursor.execute(
                "SELECT COUNT(*) FROM diaries WHERE id_user = ? AND tanggal_baca LIKE '2026%'",
                (user_id,)
            )
            baca_tahun_ini = cursor.fetchone()[0]

            # 3. Rata-rata rating yang diberikan
            cursor.execute(
                "SELECT AVG(rating) FROM diaries WHERE id_user = ? AND rating IS NOT NULL",
                (user_id,)
            )
            avg_rating = cursor.fetchone()[0]
            rating_tampil = f"{avg_rating:.1f} / 5.0" if avg_rating is not None else "Belum ada rating"

            print("---------------------------------")
            print("       STATISTIK BACAAN          ")
            print("---------------------------------")
            print(f"Total Buku Dibaca     : {total_baca} buku")
            print(f"Dibaca Tahun Ini      : {baca_tahun_ini} buku")
            print(f"Rata-rata Rating      : {rating_tampil}")

        # Tampilkan statistik karya jika role adalah Penulis
        elif user['role'] == 'Penulis':
            cursor.execute("SELECT COUNT(*) FROM books WHERE id_penulis = ?", (user_id,))
            total_karya = cursor.fetchone()[0]
            print("---------------------------------")
            print(f"Total Karya Diterbitkan : {total_karya} buku")

        conn.close()

        print("=================================")
        print("1. Edit Username / Password")
        print("2. Kembali ke Menu Utama")
        print("=================================")

        pilihan = input("Pilih menu (1-2): ").strip()

        if pilihan == '1':
            edit_profil(user_id, user['username'], user['password'])
        elif pilihan == '2':
            break
        else:
            print("\nPilihan tidak valid!")


def edit_profil(user_id, username_lama, password_lama):
    """Fungsi pembantu untuk mengubah username atau password pengguna"""
    print("\n--- EDIT PROFIL ---")
    print("(Tekan Enter langsung jika tidak ingin mengubah data tersebut)")
    
    username_baru = input(f"Username baru [{username_lama}]: ").strip()
    password_baru = input("Password baru [****]: ").strip()

    # Jika kosong (user menekan Enter), tetap gunakan data yang lama
    if not username_baru:
        username_baru = username_lama
    if not password_baru:
        password_baru = password_lama

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE users SET username = ?, password = ? WHERE id = ?",
            (username_baru, password_baru, user_id)
        )
        conn.commit()
        print("\nProfil berhasil diperbarui!")
    except sqlite3.IntegrityError:
        print(f"\nError: Username '{username_baru}' sudah dipakai akun lain!")
    finally:
        conn.close()