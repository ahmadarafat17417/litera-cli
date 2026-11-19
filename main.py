from database import init_db
import auth
import admin
import penulis
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
    """Tampilan menu setelah login (Admin, Penulis, Pembaca)"""
    global current_user
    
    while current_user is not None:
        print(f"\n=================================")
        print(f" SELAMAT DATANG, {current_user['username'].upper()}!")
        print(f" Peran: {current_user['role']}")
        print("=================================")
        
        # 1. MENU KHUSUS ADMIN
        if current_user['role'] == 'Admin':
            print("1. Manajemen User")
            print("2. Manajemen Buku")
            print("3. Manajemen Kategori")
            print("4. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-4): ").strip()
            
            if pilihan == '1':
                admin.manajemen_user()
            elif pilihan == '2':
                admin.manajemen_buku()
            elif pilihan == '3':
                admin.manajemen_kategori()
            elif pilihan == '4':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print("\nPilihan tidak valid!")

        # 2. MENU KHUSUS PENULIS
        elif current_user['role'] == 'Penulis':
            print("1. Tambah Buku Baru")
            print("2. Lihat Buku Saya")
            print("3. Edit Data Buku")
            print("4. Hapus Buku")
            print("5. Lihat Profil Saya")
            print("6. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-6): ").strip()
            
            if pilihan == '1':
                penulis.tambah_buku(current_user['id'])
            elif pilihan == '2':
                penulis.lihat_buku_saya(current_user['id'])
            elif pilihan == '3':
                penulis.edit_buku(current_user['id'])
            elif pilihan == '4':
                penulis.hapus_buku(current_user['id'])
            elif pilihan == '5':
                auth.lihat_profil(current_user['id'])
            elif pilihan == '6':
                current_user = None
                print("\nBerhasil logout!")
                break
            else:
                print("\nPilihan tidak valid!")

        # 3. MENU KHUSUS PEMBACA
        elif current_user['role'] == 'Pembaca':
            print("1. Discover & Cari Buku")
            print("2. Riwayat Diary & Ulasan Saya")
            print("3. Lihat Profil Saya")
            print("4. Logout")
            print("=================================")
            
            pilihan = input("Pilih menu (1-4): ").strip()
            
            if pilihan == '1':
                buku.discover_buku(current_user['id'])
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