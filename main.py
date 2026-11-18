from database import init_db
import auth
import buku
import diary

current_user = None

def menu_utama():
    """Tampilan menu awal sebelum pengguna login"""
    global current_user
    
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
            auth.register()
        elif pilihan == '2':
            user = auth.login()
            if user is not None:
                current_user = user
                menu_setelah_login()
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan Litera. Sampai jumpa!")
            break
        else:
            print("\nPilihan tidak valid! Silakan masukkan angka 1, 2, atau 3.")

def menu_setelah_login():
    """Tampilan menu setelah login (dibedakan berdasarkan Role)"""
    global current_user
    
    while current_user is not None:
        print(f"\n=================================")
        print(f" SELAMAT DATANG, {current_user['username'].upper()}!")
        print(f" Peran: {current_user['role']}")
        print("=================================")
        
        # Menu Khusus Penulis (6 Opsi)
        if current_user['role'] == 'Penulis':
            print("1. Tambah Buku Baru (Create)")
            print("2. Lihat Buku Saya (Read)")
            print("3. Edit Data Buku (Update)")
            print("4. Hapus Buku (Delete)")
            print("5. Lihat Profil Saya")
            print("6. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-6): ").strip()
            
            if pilihan == '1':
                buku.tambah_buku(current_user['id'])
            elif pilihan == '2':
                buku.lihat_buku_saya(current_user['id'])
            elif pilihan == '3':
                buku.edit_buku(current_user['id'])
            elif pilihan == '4':
                buku.hapus_buku(current_user['id'])
            elif pilihan == '5':
                auth.lihat_profil(current_user['id'])
            elif pilihan == '6':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print("\nPilihan tidak valid!")

        # Menu Khusus Pembaca (4 Opsi)
        elif current_user['role'] == 'Pembaca':
            print("1. Lihat & Cari Katalog Buku")
            print("2. Riwayat Diary Bacaan Saya")
            print("3. Lihat Profil Saya")
            print("4. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-4): ").strip()
            
            if pilihan == '1':
                buku.katalog_buku(current_user['id'])
            elif pilihan == '2':
                diary.lihat_diary(current_user['id'])
            elif pilihan == '3':
                auth.lihat_profil(current_user['id'])
            elif pilihan == '4':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print("\nPilihan tidak valid!")

if __name__ == '__main__':
    init_db()
    menu_utama()