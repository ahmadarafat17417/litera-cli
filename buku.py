import diary
from database import get_connection


def _tampilkan_daftar_buku(buku):
    print("\n{:<5} {:<30} {:<20} {}".format(
        "ID", "Judul", "Kategori", "Penulis"
    ))
    print("-" * 85)
    if not buku:
        print("Buku tidak ditemukan.")
        return

    for item in buku:
        print("{:<5} {:<30} {:<20} {}".format(
            item["id"], item["judul"], item["nama_kategori"],
            item["nama_penulis"]
        ))


def _ambil_buku(kata_kunci=None):
    conn = get_connection()
    try:
        query = """SELECT books.id, books.judul,
                          categories.nama_kategori,
                          users.username AS nama_penulis
                   FROM books
                   JOIN categories ON books.id_kategori = categories.id
                   JOIN users ON books.id_penulis = users.id"""
        parameter = ()
        if kata_kunci is not None:
            query += """ WHERE books.judul LIKE ?
                         OR categories.nama_kategori LIKE ?"""
            pola = f"%{kata_kunci}%"
            parameter = (pola, pola)
        query += " ORDER BY books.id"
        return conn.execute(query, parameter).fetchall()
    finally:
        conn.close()


def discover_buku(user_id):
    """Menampilkan katalog buku dan menyediakan pencarian serta detail."""
    while True:
        _tampilkan_daftar_buku(_ambil_buku())
        print("\n--- MENU KATALOG ---")
        print("1. Cari Buku")
        print("2. Lihat Detail Buku")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu (1-3): ").strip()

        if pilihan == "1":
            kata_kunci = input(
                "Masukkan kata kunci judul atau kategori: "
            ).strip()
            _tampilkan_daftar_buku(_ambil_buku(kata_kunci))
        elif pilihan == "2":
            id_buku = input("Masukkan ID buku: ").strip()
            if not id_buku.isdigit():
                print("\nID buku harus berupa angka.")
                continue
            detail_buku(int(id_buku), user_id)
        elif pilihan == "3":
            return
        else:
            print("\nPilihan tidak valid!")


def detail_buku(id_buku, user_id):
    """Menampilkan detail buku, rating, dan ulasan pembaca."""
    conn = get_connection()
    try:
        buku = conn.execute(
            """SELECT books.id, books.judul, books.sinopsis,
                      categories.nama_kategori,
                      users.username AS nama_penulis,
                      (SELECT AVG(diaries.rating)
                       FROM diaries
                       WHERE diaries.id_buku = books.id) AS rata_rating
               FROM books
               JOIN categories ON books.id_kategori = categories.id
               JOIN users ON books.id_penulis = users.id
               WHERE books.id = ?""",
            (id_buku,)
        ).fetchone()
        if buku is None:
            print("\nBuku tidak ditemukan.")
            return

        ulasan = conn.execute(
            """SELECT users.username AS nama_pembaca, diaries.isi_ulasan
               FROM diaries
               JOIN users ON diaries.id_user = users.id
               WHERE diaries.id_buku = ?
                 AND diaries.isi_ulasan IS NOT NULL
                 AND TRIM(diaries.isi_ulasan) != ''
               ORDER BY diaries.tanggal_baca DESC, diaries.id DESC""",
            (id_buku,)
        ).fetchall()
    finally:
        conn.close()

    print("\n--- DETAIL BUKU ---")
    print(f"Judul       : {buku['judul']}")
    print(f"Penulis     : {buku['nama_penulis']}")
    print(f"Kategori    : {buku['nama_kategori']}")
    print(f"Sinopsis    : {buku['sinopsis'] or '-'}")
    if buku["rata_rating"] is None:
        print("Rata-rata Rating: Belum ada rating.")
    else:
        print(f"Rata-rata Rating: {buku['rata_rating']:.2f} / 5")

    print("\nUlasan Pembaca:")
    if not ulasan:
        print("Belum ada ulasan.")
    else:
        for item in ulasan:
            print(f"- {item['nama_pembaca']}: {item['isi_ulasan']}")

    while True:
        print("\n1. Catat ke Diary & Beri Ulasan")
        print("2. Kembali ke Katalog")
        pilihan = input("Pilih menu (1-2): ").strip()

        if pilihan == "1":
            diary.tambah_diary(user_id, id_buku)
            return
        if pilihan == "2":
            return
        print("\nPilihan tidak valid!")
