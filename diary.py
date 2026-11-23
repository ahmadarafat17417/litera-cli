from datetime import datetime

from database import get_connection


def _input_tanggal():
    while True:
        tanggal_baca = input("Tanggal baca (YYYY-MM-DD): ").strip()
        try:
            tanggal = datetime.strptime(tanggal_baca, "%Y-%m-%d").date()
        except ValueError:
            print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
            continue
        if tanggal.isoformat() != tanggal_baca:
            print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
            continue
        return tanggal_baca


def _input_status(status_lama=None):
    while True:
        if status_lama:
            pilihan = input(
                f"Status baca [1. First Time / 2. Re-read] "
                f"(Enter untuk tetap {status_lama}): "
            ).strip()
            if not pilihan:
                return status_lama
        else:
            pilihan = input(
                "Status baca [1. First Time / 2. Re-read]: "
            ).strip()

        if pilihan == "1":
            return "First Time"
        if pilihan == "2":
            return "Re-read"
        print("Pilihan tidak valid. Masukkan 1 atau 2.")


def _input_rating(rating_lama=None):
    while True:
        if rating_lama is None:
            prompt = "Rating (1-5, Enter untuk melewati): "
        else:
            prompt = (
                f"Rating baru (1-5, Enter untuk tetap {rating_lama}, "
                "0 untuk menghapus): "
            )
        nilai = input(prompt).strip()

        if not nilai:
            return rating_lama
        if rating_lama is not None and nilai == "0":
            return None
        if nilai in {"1", "2", "3", "4", "5"}:
            return int(nilai)
        print("Rating harus berupa angka 1 sampai 5.")


def tambah_diary(user_id, id_buku):
    """Mencatat riwayat membaca buku beserta rating dan ulasan."""
    conn = get_connection()
    try:
        buku = conn.execute(
            "SELECT id FROM books WHERE id = ?", (id_buku,)
        ).fetchone()
        if buku is None:
            print("\nBuku tidak ditemukan. Diary tidak disimpan.")
            return

        tanggal_baca = _input_tanggal()
        status_read = _input_status()
        rating = _input_rating()
        isi_ulasan = input(
            "Ulasan (tekan Enter jika tidak ingin mengulas): "
        ).strip() or None

        conn.execute(
            """INSERT INTO diaries
               (id_user, id_buku, tanggal_baca, status_read, rating, isi_ulasan)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, id_buku, tanggal_baca, status_read, rating, isi_ulasan)
        )
        conn.commit()
        print("\nCatatan diary berhasil disimpan.")
    finally:
        conn.close()


def _tampilkan_diary(user_id):
    conn = get_connection()
    try:
        diaries = conn.execute(
            """SELECT diaries.id, books.judul, diaries.tanggal_baca,
                      diaries.status_read, diaries.rating, diaries.isi_ulasan
               FROM diaries
               JOIN books ON diaries.id_buku = books.id
               WHERE diaries.id_user = ?
               ORDER BY diaries.tanggal_baca DESC, diaries.id DESC""",
            (user_id,)
        ).fetchall()
    finally:
        conn.close()

    print("\n{:<5} {:<25} {:<12} {:<12} {:<8} {}".format(
        "ID", "Judul Buku", "Tanggal", "Status", "Rating", "Ulasan"
    ))
    print("-" * 100)
    if not diaries:
        print("Belum ada riwayat bacaan.")
    for catatan in diaries:
        print("{:<5} {:<25} {:<12} {:<12} {:<8} {}".format(
            catatan["id"], catatan["judul"], catatan["tanggal_baca"],
            catatan["status_read"],
            catatan["rating"] if catatan["rating"] is not None else "-",
            catatan["isi_ulasan"] or "-"
        ))


def _ambil_id_diary(prompt):
    id_diary = input(prompt).strip()
    if not id_diary.isdigit():
        print("\nID Diary harus berupa angka.")
        return None
    return int(id_diary)


def _edit_diary(user_id):
    id_diary = _ambil_id_diary("Masukkan ID Diary yang akan diedit: ")
    if id_diary is None:
        return

    conn = get_connection()
    try:
        catatan = conn.execute(
            "SELECT * FROM diaries WHERE id = ? AND id_user = ?",
            (id_diary, user_id)
        ).fetchone()
        if catatan is None:
            print("\nDiary tidak ditemukan.")
            return

        status_read = _input_status(catatan["status_read"])
        rating = _input_rating(catatan["rating"])
        ulasan_lama = catatan["isi_ulasan"] or ""
        ulasan_baru = input(
            f"Ulasan baru (Enter untuk tetap '{ulasan_lama}', "
            "- untuk menghapus): "
        ).strip()
        isi_ulasan = (
            None if ulasan_baru == "-"
            else ulasan_baru if ulasan_baru
            else catatan["isi_ulasan"]
        )

        conn.execute(
            """UPDATE diaries
               SET status_read = ?, rating = ?, isi_ulasan = ?
               WHERE id = ? AND id_user = ?""",
            (status_read, rating, isi_ulasan, id_diary, user_id)
        )
        conn.commit()
        print("\nCatatan diary berhasil diperbarui.")
    finally:
        conn.close()


def _hapus_diary(user_id):
    id_diary = _ambil_id_diary("Masukkan ID Diary yang akan dihapus: ")
    if id_diary is None:
        return

    conn = get_connection()
    try:
        catatan = conn.execute(
            "SELECT id FROM diaries WHERE id = ? AND id_user = ?",
            (id_diary, user_id)
        ).fetchone()
        if catatan is None:
            print("\nDiary tidak ditemukan.")
            return

        konfirmasi = input("Yakin ingin menghapus diary ini? (y/n): ").strip().lower()
        if konfirmasi == "y":
            conn.execute(
                "DELETE FROM diaries WHERE id = ? AND id_user = ?",
                (id_diary, user_id)
            )
            conn.commit()
            print("\nCatatan diary berhasil dihapus.")
        elif konfirmasi == "n":
            print("\nPenghapusan dibatalkan.")
        else:
            print("\nKonfirmasi tidak valid. Penghapusan dibatalkan.")
    finally:
        conn.close()


def lihat_diary(user_id):
    """Menampilkan serta mengelola riwayat diary milik pengguna."""
    while True:
        _tampilkan_diary(user_id)
        print("\n--- MENU RIWAYAT DIARY ---")
        print("1. Edit Catatan / Ulasan Diary")
        print("2. Hapus Catatan Diary")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih menu (1-3): ").strip()

        if pilihan == "1":
            _edit_diary(user_id)
        elif pilihan == "2":
            _hapus_diary(user_id)
        elif pilihan == "3":
            return
        else:
            print("\nPilihan tidak valid!")
