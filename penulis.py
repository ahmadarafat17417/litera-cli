from database import get_connection


# ---------- fungsi bantu ----------

def _ambil_buku_penulis(cursor, user_id):
    # ambil semua buku punya penulis ini, sekalian nama kategori + rata2 rating
    cursor.execute('''
        SELECT b.id, b.judul, b.sinopsis, b.id_kategori,
               c.nama_kategori,
               AVG(d.rating) AS rata_rating,
               COUNT(d.id)   AS jumlah_diary
        FROM books b
        JOIN categories c ON b.id_kategori = c.id
        LEFT JOIN diaries d ON d.id_buku = b.id
        WHERE b.id_penulis = ?
        GROUP BY b.id
        ORDER BY b.id
    ''', (user_id,))
    return cursor.fetchall()

def _tampilkan_daftar_ringkas(daftar_buku):
    # list singkat buat menu edit sama hapus
    for b in daftar_buku:
        print(f"  [{b['id']}] {b['judul']}  ({b['nama_kategori']})")

