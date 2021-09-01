import time
import sys
import argparse
import os
from datetime import datetime

import edit_inventory
import transaksi
import alat
#LOKASI FILE
try:
    parser = argparse.ArgumentParser()    #Membuat parser
    parser.add_argument('Path', type=str, help='Path ke folder')    #Menambahkan argumen yang akan dibaca
    args = parser.parse_args()  #Assign parser

    lokasi = args.Path      #Menyimpan path di variabel lokasi
except:
    print("Tidak ada nama folder yang diberikan!")
    print("Usage : python mainCode.py <nama_folder>")
    sys.exit()

def hashing(password):                                     #Hashing dengan menggabungkan karakter pertama dan terakhir. jika panjang password>3 maka
    hashed = ''                                            #yang digabungkan adalah karakter pertama,terakhir, dan kedua terakhir
    if len(password) == 1:                                 #agar tidak muncul simbol yang aneh maka dibatasi nilai ascii hanya akan berada
        password += "AB"                                   #di nilai 48 hingga 122
    N = len(password)                                     
    if N > 3:                                              
        for i in range(N-2):
            if i == 0:
                var_antara = ((ord(password[i]) + 2*i) % 3) + 10*i + ord(password[N-1]) + ord(password[N-2])
            else:
                var_antara = ((ord(password[i]) + 2*i) % 3) + 10*i
            while var_antara>122:
                var_antara = var_antara//2
            while var_antara<48:
                var_antara += 15  
            hashed = hashed + chr(var_antara)
    else:
        for i in range(N-1):
            if i == 0:
                var_antara = ((ord(password[i]) + 2*i) % 3) + 10*i + ord(password[N-1])
            else:
                var_antara = ((ord(password[i]) + 2*i) % 3) + 10*i
            while var_antara>122:
                var_antara = var_antara//2
            while var_antara<48:
                var_antara += 15  
            hashed = hashed + chr(var_antara)
    return hashed


def appund(elemen_utama,elemen_tambahan):                       #.Append
    return (elemen_utama + [elemen_tambahan])
    
def seplit(calon_array,pembatas = ';'):                         #.split
    array_baru = []
    isi = ''
    for huruf in calon_array:
        if (huruf!=pembatas):
            isi += huruf
        else:
            array_baru = appund(array_baru,isi)
            isi = ''
    if (isi != ''):
        array_baru = appund(array_baru,isi)
    return array_baru

def proses_data_awal(array,array_data):                         #split dan strip masukan ke dalam array
    for line in array:
        linet = seplit(line)
        linet = [isi.strip() for isi in linet]
        array_data = appund(array_data,linet)
    return array_data

def proses_data_num_gadget(array_data):                                #Mengganti string menjadi angka untuk value kolom tertentu
    for i in array_data:
        i[3] = int(i[3])
        i[5] = int(i[5])
    return array_data

def proses_data_num_cons(array_data):                                #Mengganti string menjadi angka untuk value kolom tertentu
    for i in array_data:
        i[3] = int(i[3])
    return array_data

def proses_data_num_cons_histo(array_data):                                #Mengganti string menjadi angka untuk value kolom tertentu
    for i in array_data:
        i[4] = int(i[4])
    return array_data

def proses_data_num_borrow(array_data):                                #Mengganti string menjadi angka untuk value kolom tertentu
    for i in array_data:
        i[4] = int(i[4])
        i[5] = True if (i[5] == 'True') else False
    return array_data

def proses_data_string_gadget(array_data):                             #Mengubah kembali value yang sudah diubah jenisnya kembali menjadi string
    for i in array_data:
        i[3] = str(i[3])
        i[5] = str(i[5])
    return array_data

def proses_data_string_cons(array_data):                             #Mengubah kembali value yang sudah diubah jenisnya kembali menjadi string
    for i in array_data:
        i[3] = str(i[3])
    return array_data

def proses_data_string_cons_histo(array_data):                             #Mengubah kembali value yang sudah diubah jenisnya kembali menjadi string
    for i in array_data:
        i[4] = str(i[4])
    return array_data

def proses_data_string_borrow(array_data):                             #Mengubah kembali value yang sudah diubah jenisnya kembali menjadi string
    for i in array_data:
        i[4] = str(i[4])
        i[5] = str(i[5])
    return array_data


def proses_kembali_csv(array_data,header):                      #Mengubah format agar siap di rewrite ke csv
    array_teks = []
    teks = ''
    array_data = [[header]] + array_data
    for i in array_data:
        array_teks = appund(array_teks,";".join(i))

    ind = 0

    for k in array_teks:
        array_teks[ind] += "\n"
        teks += array_teks[ind]
        ind += 1
    return teks

def tambah_data_login(array_data):                              #Fungsi untuk register data login
    Nama = input("Masukkan nama: ")
    Username = input("Masukkan username: ")
    Id = "#" + ("%03d" % (len(array_data)+1))
    Password = ''
    while len(Password)<2:
        Password = input("Masukkan password: ")
        if len(Password)<2:
            print("Password anda terlalu lemah(minimal 2 karakter)")
    Alamat = input("Masukkan alamat: ")
    Nama = Nama.lower()
    Nama = seplit(Nama," ")
    nama_sementara = ''
    for i in Nama:
        nama_sementara += i.capitalize()
        nama_sementara += " "
    nama_sementara = nama_sementara.strip()
    Nama = nama_sementara
    Role = "User"
    bool_konfirmasi_register = True
    for a in array_data:
        if (a[1] == Username):
            bool_konfirmasi_register = False
            print("Username anda sudah diambil... :( silahkan coba lagi dengan username lain.")
            return array_data,bool_konfirmasi_register,Password
    array_data += [[Id,Username,Nama,Alamat,hashing(Password),Role]]
    return array_data,bool_konfirmasi_register,Password

def buka_data(file):                                          #Fungsi untuk membaca data csv login
    line = open((lokasi + "/" + file + ".csv"),"r")
    lines = line.readlines()
    lines = [line.replace("\n",'') for line in lines]
    line.close()
    return lines

def pembatas():                                                 #Pembatas hiasan menggunakan "="
    for i in range(60):
        print("=",end='')
    print()

def rewrite_data(data_text,file,lokasi_save):                              #Fungsi untuk rewrite file CSV
    f = open((lokasi_save + "/" + file + ".csv"),"w")
    f.write(data_text)
    f.close()

def mengeluarkan_data_gadget_rarity(array_data_gadget,rarity):         #Fungsi yang dapat menampilkan data gadget tergantung rarity yang dimasukkan
    tidak_ada = True
    for i in array_data_gadget:
        if i[4] == rarity:
            tidak_ada = False
            print("Nama             :",i[1])
            print("Deskripsi        :",i[2])
            print("Jumlah           :",i[3])
            print("Rarity           :",i[4])
            print("Tahun Ditemukan  :",i[5])
            print()
    if tidak_ada:
        print("Admin belum menambahkan item dengan rarity ini :( hubungi admin pemalasmu sekarang!")
        print()

def show_gadget(array_data_gadget_mini):
    print("Nama             :",array_data_gadget_mini[1])
    print("Deskripsi        :",array_data_gadget_mini[2])
    print("Jumlah           :",array_data_gadget_mini[3])
    print("Rarity           :",array_data_gadget_mini[4])
    print("Tahun Ditemukan  :",array_data_gadget_mini[5])
    print()

def mengeluarkan_data_gadget_tahun(array_data_gadget,tahun,kategori):         #Fungsi yang dapat menampilkan data gadget tergantung rarity yang dimasukkan
    tidak_ada = True
    for i in array_data_gadget:
        if kategori == "=":
            if i[5] == tahun:
                tidak_ada = False
                show_gadget(i)
        elif kategori == "<":
            if i[5] < tahun:
                tidak_ada = False
                show_gadget(i)
        elif kategori == ">":
            if i[5] > tahun:
                tidak_ada = False
                show_gadget(i)
        elif kategori == "<=":
            if i[5] <= tahun:
                tidak_ada = False
                show_gadget(i)
        elif kategori == ">=":
            if i[5] >= tahun:
                tidak_ada = False
                show_gadget(i)

    if tidak_ada:
        print("Admin belum menambahkan item yang ditemukan pada range tahun ini :( hubungi admin pemalasmu sekarang!")
        print()

def save_data(folder_save,folder_ada,array_data_user,file,header,direk = ''):                    
    for folder in os.listdir():
        if folder == folder_save:                               #Mengecek apakah folder sudah ada atau belum
            folder_ada = True
    if folder_ada:
        array_data_user_rewrite = proses_kembali_csv(array_data_user,header)  #Menjadikan array_data agar siap di rewrite
        rewrite_data(array_data_user_rewrite,file,folder_save)
        
    else:       
        os.mkdir(folder_save)#direk+"/"+folder_save)                #Membuat folder
        array_data_user_rewrite = proses_kembali_csv(array_data_user,header)
        rewrite_data(array_data_user_rewrite,file,folder_save)
        
def helpmenu():
    if role == "Belum Login": #Jika belum login
        print("99. Login - melakukan login ke dalam sistem")
        print("13. Help - memberikan panduan penggunaan sistem")
        print("14. Exit - keluar dari aplikasi")
    elif role == "Admin": #Jika admin
        print("0. Register - mendaftarkan pengguna baru")
        print("99. Login - melakukan login ke dalam sistem")
        print("1. Carirarity - mencari gadget berdasarkan rarity tertentu")
        print("2. Caritahun - mencari gadget berdasarkan tahun tertentu")
        print("3. Tambahitem - menambahkan item ke dalam inventori")
        print("4. Hapusitem - menghapus suatu item yang ada dalam database")
        print("5. Ubahjumlah - mengubah jumlah gadget dan consumable yang terdapat di dalam sistem")
        print("9. Riwayatpinjam - melihat riwayat peminjaman gadget (admin)")
        print("10. Riwayatkembali - melihat riwayat pengembalian gadget")
        print("11. Riwayatambil - melihat riwayat pengambilan consumable")
        print("12. Save - melakukan penyimpanan data setelah dilakukan perubahan (admin, user)")
        print("13. Help - memberikan panduan penggunaan sistem")
        print("14. Exit - keluar dari aplikasi")

    elif role == "User": #Jika user
        print("99. Login - melakukan login ke dalam sistem")
        print("1. Carirarity - mencari gadget berdasarkan rarity tertentu")
        print("2. Caritahun - mencari gadget berdasarkan tahun tertentu")
        print("6. Pinjam - melakukan peminjaman gadget")
        print("7. Kembalikan - mengembalikan gadget secara seutuhnya")
        print("8. Minta - meminta consumable yang tersedia")
        print("12. Save - melakukan penyimpanan data setelah dilakukan perubahan")
        print("13. Help - memberikan panduan penggunaan sistem")
        print("14. Exit - keluar dari aplikasi")    



#LOOP UTAMA PROGRAM
#KAMUS
bool_loop_utama = True
logged = False
bool_menu_setelah_login = True
bool_menu_search_rarity = False
bool_menu_search_tahun = False
bool_menu_tambah_item = False
bool_menu_hapus_gadget_cons = False
bool_menu_ubah_jumlah = False
bool_menu_pinjam_gadget = False
bool_menu_kembalikan_gadget = False
bool_menu_meminta_cons = False
bool_menu_riwayat_pinjam_gadget = False
bool_menu_riwayat_kembali_gadget = False
bool_menu_riwayat_ambil_cons = False
bool_menu_load_data = False
bool_menu_save_data = False
bool_menu_exit = False
konfirmasi_exit_akhir = False
bool_register = False
bool_login = False
bool_menu_help = False
role = "Belum Login"

#Buka data user
lines = buka_data("user")
header_user = lines.pop(0)
array_data_user = proses_data_awal(lines,[])

#Pembukaan data gadget
array_data_gadget_awal = buka_data("gadget")
header_gadget = array_data_gadget_awal.pop(0)
array_data_gadget = proses_data_awal(array_data_gadget_awal,[])
array_data_gadget = proses_data_num_gadget(array_data_gadget)

array_data_cons_awal = buka_data("consumable")
header_cons = array_data_cons_awal.pop(0)
array_data_cons = proses_data_awal(array_data_cons_awal,[])
array_data_cons = proses_data_num_cons(array_data_cons)

array_data_cons_histo_awal = buka_data("consumable_history")
header_cons_histo = array_data_cons_histo_awal.pop(0)
array_data_cons_histo = proses_data_awal(array_data_cons_histo_awal,[])
try:
    array_data_cons_histo = proses_data_num_cons_histo(array_data_cons_histo)
except:
    array_data_cons_histo = []

array_data_borrow_awal = buka_data("gadget_borrow_history")
header_borrow = array_data_borrow_awal.pop(0)
array_data_borrow = proses_data_awal(array_data_borrow_awal,[])
try:
    array_data_borrow = proses_data_num_borrow(array_data_borrow)
except:
    array_data_borrow = []

array_data_return_awal = buka_data("gadget_return_history")
header_return = array_data_return_awal.pop(0)
try:
    array_data_return = proses_data_awal(array_data_return_awal,[])
except:
    array_data_borrow = []

array_data_gadget_terhapus_awal = buka_data("gadget_terhapus")
header_gadget_terhapus = array_data_gadget_terhapus_awal.pop(0)
array_data_gadget_terhapus = proses_data_awal(array_data_gadget_terhapus_awal,[])
try:
    array_data_gadget_terhapus = proses_data_num_gadget(array_data_gadget_terhapus)
except:
    array_data_gadget_terhapus = []

while bool_loop_utama:
    #Menu Setelah login

    #ALGORITMA
    while bool_menu_setelah_login:                                          #MENAMPILKAN TAMPILAN MENU UTAMA SETELAH 
        pembatas()
        print("SELAMAT DATANG! SAYA ADALAH DIGIEMON.")
        print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣶⣶⣶⣶⣶⠶⣶⣤⣤⣀⠀⠀⠀⠀⠀⠀ ")
        time.sleep(0.05)
        print("⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⠁⠀⢀⠈⢿⢀⣀⠀⠹⣿⣿⣿⣦⣄⠀⠀⠀ ")
        time.sleep(0.05)
        print("⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⠿⠀⠀⣟⡇⢘⣾⣽⠀⠀⡏⠉⠙⢛⣿⣷⡖⠀ ")
        time.sleep(0.05)
        print("⠀⠀⠀⠀⠀⣾⣿⣿⡿⠿⠷⠶⠤⠙⠒⠀⠒⢻⣿⣿⡷⠋⠀⠴⠞⠋⠁⢙⣿⣄ ")
        time.sleep(0.05)
        print("⠀⠀⠀⠀⢸⣿⣿⣯⣤⣤⣤⣤⣤⡄⠀⠀⠀⠀⠉⢹⡄⠀⠀⠀⠛⠛⠋⠉⠹⡇ ")
        time.sleep(0.05)
        print("⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣼⣇⣀⣀⣀⣛⣛⣒⣲⢾⡷ ")
        time.sleep(0.05)
        print("⢀⠤⠒⠒⢼⣿⣿⠶⠞⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⣼⠃ ")
        time.sleep(0.05)
        print("⢮⠀⠀⠀⠀⣿⣿⣆⠀⠀⠻⣿⡿⠛⠉⠉⠁⠀⠉⠉⠛⠿⣿⣿⠟⠁⠀⣼⠃⠀ ")
        time.sleep(0.05)
        print("⠈⠓⠶⣶⣾⣿⣿⣿⣧⡀⠀⠈⠒⢤⣀⣀⡀⠀⠀⣀⣀⡠⠚⠁⠀⢀⡼⠃⠀")
        time.sleep(0.05)
        print("⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⣭⣭⣭⣭⣭⣥⣤⣤⣤⣴⣟⠁")
        time.sleep(1)
        print("APA YANG BISA SAYA BANTU HARI INI?")
        print("0. Register                                                  99. Login")
        pembatas()
        print("PILIHAN MENU:")
        print("1. Mencari gadget berdasarkan rarity                         8. Meminta consumable")
        print("2. Mencari gadget berdasarkan tahun ditemukan                9. Melihat riwayat peminjaman gadget")
        print("3. Menambah item                                             10. Melihat riwayat pengembalian gadget")
        print("4. Menghapus gadget atau consumable                          11. Melihat riwayat pengambilan consumable")
        print("5. Mengubah jumlah gadget atau consumable pada inventory     12. save data")
        print("6. Meminjam gadget                                           13. Help")
        print("7. Mengembalikan gadget                                      ")
        print("                                     14. Exit")
        
        print()
        try:
            pilihan_menu = int(input("Menu mana yang ingin anda pilih?(jawab menggunakan angka!): "))   #Pilihan 
            print()
            if (pilihan_menu == 13):
                bool_menu_help = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 0) and role == "Admin":
                bool_register = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 0):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1)
            elif (pilihan_menu == 99) and logged:
                print("Anda sudah login.")
                time.sleep(1)
            elif (pilihan_menu == 99):
                bool_login = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 14):
                bool_menu_exit = True
                bool_menu_setelah_login = False
            elif not logged and (pilihan_menu>=0 and pilihan_menu<=14 or pilihan_menu==99) :
                print("Anda harus login terlebih dahulu sebelum mengakses menu ini.")
                time.sleep(1) 
            elif (pilihan_menu == 1):
                bool_menu_search_rarity = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 2):
                bool_menu_search_tahun = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 3) and role == "Admin":
                bool_menu_tambah_item = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 3):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 4) and role == "Admin":
                bool_menu_hapus_gadget_cons = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 4):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 5) and role == "Admin":
                bool_menu_ubah_jumlah = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 5):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 6):
                bool_menu_pinjam_gadget = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 7):
                bool_menu_kembalikan_gadget = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 8):
                bool_menu_meminta_cons = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 9 and role == "Admin"):
                bool_menu_riwayat_pinjam_gadget = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 9):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 10 and role == "Admin"):
                bool_menu_riwayat_kembali_gadget = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 10):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 11 and role == "Admin"):
                bool_menu_riwayat_ambil_cons = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 11):
                print("Maaf x-x menu ini hanya dapat di akses oleh admin.")
                time.sleep(1.5)
            elif (pilihan_menu == 12):
                bool_menu_save_data = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 0):
                bool_register = True
                bool_menu_setelah_login = False
            elif (pilihan_menu == 99):
                bool_login = True
                bool_menu_setelah_login = False
            else:
                print("Menu yang anda pilih tidak ditemukan :(. Silahkan masukan kode menu yang tepat.")
                time.sleep(1)
        except ValueError:
            print("Masukan anda salah")
            time.sleep(1)

    #F01 (REGISTER)

    #ALGORITMA
    while bool_register:
        bool_konfirmasi_register = True
        pembatas()
        print("Silahkan masukan data anda.")
        array_data_user,bool_konfirmasi_register,Password = tambah_data_login(array_data_user)

        while bool_konfirmasi_register:
            pembatas()
            print("Nama anda:",array_data_user[len(array_data_user)-1][2])
            print("Username anda:",array_data_user[len(array_data_user)-1][1])
            print("Password anda:",Password)
            print("Alamat anda:",array_data_user[len(array_data_user)-1][3])
            konfirmasi_register = input("Apakah anda yakin akan mendaftar dengan data di atas?(y/n): ")
            konfirmasi_register = konfirmasi_register.lower()
            if (konfirmasi_register == "y"):
                bool_register = False
                bool_konfirmasi_register = False
                bool_menu_setelah_login = True
            elif (konfirmasi_register=="n"):
                bool_konfirmasi_register = False
                array_data_user.remove(array_data_user[len(array_data_user)-1])
                print("Silahkan masukkan kembali dengan data yang sudah dibenarkan!")
                time.sleep(1)
            else:
                print("Masukkan anda salah! Silahkan ulangi masukkan!")
                time.sleep(1)
    #F02 (LOGIN)
    #ALGORITMA
    while bool_login:
        pembatas()    
        username = input("Masukkan username anda: ")
        password = input("Masukkan password anda: ")
        for i in array_data_user:
            if i[1] == username and i[4] == hashing(password):
                role = i[5]
                id_user = i[0]
                bool_login = False
                bool_menu_setelah_login = True
                logged = True
                break
        if bool_login:
            print("Username/password salah! Silahkan Masukkan kembali username/password anda!")
            time.sleep(1)


    #F03 Pencarian gadget berdasarkan rarity
    while bool_menu_search_rarity:
        konfirmasi_search = True               #Bool untuk loop input konfirmasi ingin search kembali
        pembatas()
        rarity = input("Masukkan rarity barang yang ingin anda cari!: ")
        rarity = rarity.capitalize()
        mengeluarkan_data_gadget_rarity(array_data_gadget,rarity)      #Mengeluarkan data search rarity
        while konfirmasi_search:
            konfirmasi_menu_search_rarity = input("Apakah anda masih ingin mencari barang?(y/n): ")
            konfirmasi_menu_search_rarity = konfirmasi_menu_search_rarity.lower()
            if konfirmasi_menu_search_rarity == "y":
                konfirmasi_search = False
            elif konfirmasi_menu_search_rarity == "n":
                konfirmasi_search = False
                bool_menu_search_rarity = False
                bool_menu_setelah_login = True
            else:
                print("Masukkan anda salah!")

    #F04 Pencarian gadget berdasarkan tahun ditemukan
    while bool_menu_search_tahun:
        konfirmasi_search = True               #Bool untuk loop input konfirmasi ingin search kembali
        pembatas()
        tahun = int(input("Masukkan tahun ditemukan barang yang ingin anda cari!: "))
        kategori = input("Masukkan kategori pencarian tahun (=,<,>,>=,<=): ")
        mengeluarkan_data_gadget_tahun(array_data_gadget,tahun,kategori)      #Mengeluarkan data search tahun
        while konfirmasi_search:
            konfirmasi_menu_search_tahun = input("Apakah anda masih ingin mencari barang?(y/n): ")
            konfirmasi_menu_search_tahun = konfirmasi_menu_search_tahun.lower()
            if konfirmasi_menu_search_tahun == "y":
                konfirmasi_search = False
            elif konfirmasi_menu_search_tahun == "n":
                konfirmasi_search = False
                bool_menu_search_tahun = False
                bool_menu_setelah_login = True
            else:
                print("Masukkan anda salah!")
    
    #F05 Menambah item
    #ALGORITMA
    while bool_menu_tambah_item:
        pembatas()
        print('MENAMBAHKAN ITEM')
        edit_inventory.tambah_item(array_data_gadget, array_data_cons, array_data_gadget_terhapus)

        konfirmasi_keluar_tambah = True
        while konfirmasi_keluar_tambah:
            konfirmasi_tambah_item = input("Apakah anda masih ingin menambahkan barang barang?(y/n): ")
            konfirmasi_tambah_item = konfirmasi_tambah_item.lower()
            if konfirmasi_tambah_item == "y":
                konfirmasi_keluar_tambah = False
            elif konfirmasi_tambah_item == "n":
                konfirmasi_keluar_tambah = False
                bool_menu_tambah_item = False
                bool_menu_setelah_login = True
            else:
                print("Masukkan anda salah!")

    # F06 Menghapus Gadget atau Consumable
    # ALGORITMA
    while bool_menu_hapus_gadget_cons:
      pembatas()
      print('MENGHAPUS ITEM')
      isSukses = edit_inventory.hapus_item(array_data_gadget, array_data_cons, array_data_gadget_terhapus)
      if isSukses:
        konfirmasi_keluar_hapus = True
        while konfirmasi_keluar_hapus:
          konfirmasi = input("Apakah anda masih ingin menghapus item?(y/n): ")
          konfirmasi = konfirmasi.lower()
          if konfirmasi == "y":
            konfirmasi_keluar_hapus = False
          elif konfirmasi == "n":
            konfirmasi_keluar_hapus = False
            bool_menu_hapus_gadget_cons = False
            bool_menu_setelah_login = True
          else:
            print("Masukkan anda salah!")
      else:
        bool_menu_hapus_gadget_cons = False
        bool_menu_setelah_login = True

    # F07 Mengubah Jumlah Gadget atau Consumable pada Inventory
    # Algoritma
    while bool_menu_ubah_jumlah:
      pembatas()
      print('MENGUBAH JUMLAH ITEM')
      isSukses = edit_inventory.ubah_jumlah(array_data_gadget, array_data_cons)
      if isSukses:
        konfirmasi_keluar = True
        while konfirmasi_keluar:
          konfirmasi = input("Apakah anda masih ingin mengubah item?(y/n): ")
          konfirmasi = konfirmasi.lower()
          if konfirmasi == "y":
            konfirmasi_keluar = False
          elif konfirmasi == "n":
            konfirmasi_keluar = False
            bool_menu_ubah_jumlah = False
            bool_menu_setelah_login = True
          else:
            print("Masukkan anda salah!")
      else:
        bool_menu_ubah_jumlah = False
        bool_menu_setelah_login = True

    # F08 Meminjam Gadget
    # Algoritma
    while bool_menu_pinjam_gadget:
      pembatas()
      print('MEMINJAM GADGET')
      isSukses = transaksi.pinjam_gadget(array_data_gadget, array_data_borrow, id_user)

      if isSukses:
        konfirmasi_keluar = True
        while konfirmasi_keluar:
          konfirmasi = input("Apakah Anda masih ingin meminjam gadget?(y/n): ")
          konfirmasi = konfirmasi.lower()
          if konfirmasi == "y":
            konfirmasi_keluar = False
          elif konfirmasi == "n":
            konfirmasi_keluar = False
            bool_menu_pinjam_gadget = False
            bool_menu_setelah_login = True
          else:
            print("Masukkan anda salah!")
      else:
        bool_menu_pinjam_gadget = False
        bool_menu_setelah_login = True

    # F09 Mengembalikan Gadget
    # Algoritma
    while bool_menu_kembalikan_gadget:
      pembatas()
      print('MENGEMBALIKAN GADGET')
      isSukses = transaksi.kembali_gadget(array_data_gadget, array_data_return, array_data_borrow, id_user, array_data_gadget_terhapus)

      if isSukses:
        konfirmasi_keluar = True
        while konfirmasi_keluar:
          konfirmasi = input("Apakah Anda masih ingin mengembalikan gadget?(y/n): ")
          konfirmasi = konfirmasi.lower()
          if konfirmasi == "y":
            konfirmasi_keluar = False
          elif konfirmasi == "n":
            konfirmasi_keluar = False
            bool_menu_kembalikan_gadget = False
            bool_menu_setelah_login = True
      else:
        bool_menu_kembalikan_gadget = False
        bool_menu_setelah_login = True

    # F10 Meminta Consumable
    while bool_menu_meminta_cons:
      pembatas()
      print('MENGAMBIL CONSUMABLE')
      isSukses = transaksi.minta_consum(array_data_cons, array_data_cons_histo, id_user)

      if isSukses:
        konfirmasi_keluar = True
        while konfirmasi_keluar:
          konfirmasi = input("Apakah Anda masih ingin mengambil consumable?(y/n): ")
          konfirmasi = konfirmasi.lower()
          if konfirmasi == "y":
            konfirmasi_keluar = False
          elif konfirmasi == "n":
            konfirmasi_keluar = False
            bool_menu_meminta_cons = False
            bool_menu_setelah_login = True
      else:
        bool_menu_meminta_cons = False
        bool_menu_setelah_login = True

    #F11 riwayatpinjam
    if bool_menu_riwayat_pinjam_gadget:                         
      
        array_data_borrow = sorted(array_data_borrow, key = lambda row: datetime.strptime(row[3], "%d/%m/%Y"),reverse=True)  #Mengurutkan sesuai tanggal
        datas_length_f11 = len(array_data_borrow)
        tampilkan_lagi = True
        indeks = 0
        while tampilkan_lagi:
            if datas_length_f11 == 0:                                 #Memeriksa data kosong
                pass

            elif datas_length_f11 <= 5:                                  #Menampilkan data berjumlah <= 5
                for i in range(datas_length_f11):
                    print("ID Peminjaman        : ", array_data_borrow[i][0])
                    for k in array_data_user:
                        if k[0] == array_data_borrow[i][1]:
                            print("Nama Pengambil       : ", k[2])
                    for l in array_data_gadget:
                        if l[0] == array_data_borrow[i][2]:
                            print("Nama Gadget          : ", l[1])
                    print("Tanggal Peminjaman   : ", array_data_borrow[i][3])
                    print("Jumlah               : ", array_data_borrow[i][4])
                    print("\n")
                datas_length_f11 = 0
            
            elif datas_length_f11 > 5:
                                                    #Menampilkan data berjumlah > 5
                    for i in range(5):
                        print("ID Peminjaman        : ", array_data_borrow[indeks][0])
                        for k in array_data_user:
                            
                            if k[0] == array_data_borrow[indeks][1]:
                                print("Nama Pengambil       : ", k[2])
                        for l in array_data_gadget:
                            
                            if l[0] == array_data_borrow[indeks][2]:
                                print("Nama Gadget          : ", l[1])
                        print("Tanggal Peminjaman   : ", array_data_borrow[indeks][3])
                        print("Jumlah               : ", array_data_borrow[indeks][4])
                        print("\n")
                        indeks += 1
                    datas_length_f11 -= 5
            tampilkan_lagi = False
            konfirmasi_tampilkan_lagi = ''
            if datas_length_f11 > 0:
                konfirmasi_tampilkan_lagi = input("Apakah anda masih ingin menampilkan history?(y/n): ")
                konfirmasi_tampilkan_lagi = konfirmasi_tampilkan_lagi.lower()
            if konfirmasi_tampilkan_lagi == "n":
                tampilkan_lagi = False
            elif konfirmasi_tampilkan_lagi == "y":
                tampilkan_lagi = True


        bool_menu_riwayat_pinjam_gadget = False
        bool_menu_setelah_login = True
    #F12 riwayatkembali
    if bool_menu_riwayat_kembali_gadget:                         
      
        array_data_return = sorted(array_data_return, key = lambda row: datetime.strptime(row[2], "%d/%m/%Y"),reverse=True)  #Mengurutkan sesuai tanggal
        datas_length_f12 = len(array_data_return)
        tampilkan_lagi = True
        indeks = 0
        while tampilkan_lagi:
            if datas_length_f12 == 0:                                 #Memeriksa data kosong
                pass

            elif datas_length_f12 <= 5:                                  #Menampilkan data berjumlah <= 5
                for i in range(datas_length_f12):
                    print("ID Pengembalian        : ", array_data_return[i][0])
                    for k in array_data_borrow:
                        if k[0] == array_data_return[i][1]:
                            for j in array_data_user:
                                if j[0] == k[1]:
                                    print("Nama Pengambil         : ", j[2])
                    for m in array_data_borrow:
                        if m[0] == array_data_return[i][1]:
                            for l in array_data_gadget:
                                if l[0] == m[2]:
                                    print("Nama Gadget            : ", l[1])
                    print("Tanggal Pengembalian   : ", array_data_return[i][2])
                    print("\n")
                datas_length_f12 = 0
            
            elif datas_length_f12 > 5:
                                                    #Menampilkan data berjumlah > 5
                for i in range(5):
                    print("ID Pengembalian        : ", array_data_return[indeks][0])
                    for k in array_data_borrow:
                        if k[0] == array_data_return[indeks][1]:
                            for j in array_data_user:
                                if j[0] == k[1]:
                                    print("Nama Pengambil         : ", j[2])
                    for m in array_data_borrow:
                        if m[0] == array_data_return[indeks][1]:
                            for l in array_data_gadget:
                                if l[0] == m[2]:
                                    print("Nama Gadget            : ", l[1])
                    print("Tanggal Pengembalian   : ", array_data_return[indeks][2])
                    print("\n")
                    indeks += 1
                datas_length_f12 -= 5
            tampilkan_lagi = False
            konfirmasi_tampilkan_lagi = ''
            if datas_length_f12 > 0:
                konfirmasi_tampilkan_lagi = input("Apakah anda masih ingin menampilkan history?(y/n): ")
                konfirmasi_tampilkan_lagi = konfirmasi_tampilkan_lagi.lower()
            if konfirmasi_tampilkan_lagi == "n":
                tampilkan_lagi = False
            elif konfirmasi_tampilkan_lagi == "y":
                tampilkan_lagi = True


        bool_menu_riwayat_kembali_gadget = False
        bool_menu_setelah_login = True
      

    #F13 riwayatambil (consumable)
    if bool_menu_riwayat_ambil_cons:                          

        array_data_cons_histo = sorted(array_data_cons_histo, key = lambda row: datetime.strptime(row[3], "%d/%m/%Y"),reverse=True)  #Mengurutkan sesuai tanggal
        datas_length_f13 = len(array_data_cons_histo)
        tampilkan_lagi = True
        indeks = 0
        while tampilkan_lagi:
            if datas_length_f13 == 0:                                 #Memeriksa data kosong
                pass

            elif datas_length_f13 <= 5:                                  #Menampilkan data berjumlah < 5
                for i in range(datas_length_f13):
                    print("ID Pengambilan       : ", array_data_cons_histo[i][0])
                    for k in array_data_user:
                        if k[0] == array_data_cons_histo[i][1]:
                            print("Nama Pengambil       : ", k[2])
                    for l in array_data_cons:
                        if l[0] == array_data_cons_histo[i][2]:
                            print("Nama Consumable      : ", l[1])
                    print("Tanggal Pengambilan  : ", array_data_cons_histo[i][3])
                    print("Jumlah               : ", array_data_cons_histo[i][4])
                    print("\n")
                datas_length_f13 = 0
            
            elif datas_length_f13 > 5:
                                                    #Menampilkan data berjumlah >= 5
                    for i in range(5):
                        print("ID Pengambilan       : ", array_data_cons_histo[indeks][0])
                        for k in array_data_user:
                            
                            if k[0] == array_data_cons_histo[indeks][1]:
                                print("Nama Pengambil       : ", k[2])
                        for l in array_data_cons:
                            
                            if l[0] == array_data_cons_histo[indeks][2]:
                                print("Nama Consumable      : ", l[1])
                        print("Tanggal Pengambilan  : ", array_data_cons_histo[indeks][3])
                        print("Jumlah               : ", array_data_cons_histo[indeks][4])
                        print("\n")
                        indeks += 1
                    datas_length_f13 -= 5
            tampilkan_lagi = False
            konfirmasi_tampilkan_lagi = ''
            if datas_length_f13 > 0:
                konfirmasi_tampilkan_lagi = input("Apakah anda masih ingin menampilkan history?(y/n): ")
                konfirmasi_tampilkan_lagi = konfirmasi_tampilkan_lagi.lower()
            if konfirmasi_tampilkan_lagi == "n":
                tampilkan_lagi = False
            elif konfirmasi_tampilkan_lagi == "y":
                tampilkan_lagi = True


        bool_menu_riwayat_ambil_cons = False
        bool_menu_setelah_login = True
    
    #F15 Save Data
    #KAMUS
    direk = os.path.dirname(lokasi)

    #ALGORITMA
    if bool_menu_save_data:
        pembatas()
        folder_ada = False
        bool_menu_save_data = False
        bool_menu_setelah_login = True
        folder_save = input("Masukkan nama folder penyimpanan: ")

        array_data_gadget_save = proses_data_string_gadget(alat.deepcopy(array_data_gadget))
        array_data_cons_save = proses_data_string_cons(alat.deepcopy(array_data_cons))
        try:
            array_data_gadget_terhapus_save = proses_data_string_gadget(alat.deepcopy(array_data_gadget_terhapus))
        except:
            pass
        array_data_borrow_save = proses_data_string_borrow(alat.deepcopy(array_data_borrow))
        array_data_cons_histo_save = proses_data_string_cons_histo(alat.deepcopy(array_data_cons_histo))
        
        save_data(folder_save,folder_ada,array_data_user,"user",header_user,direk)
        save_data(folder_save,folder_ada,array_data_gadget_save,"gadget",header_gadget,direk)
        save_data(folder_save,folder_ada,array_data_cons_save,"consumable",header_cons,direk)
        try:
            save_data(folder_save,folder_ada,array_data_gadget_terhapus_save,"gadget_terhapus",header_gadget_terhapus,direk)
        except:
            array_data_gadget_terhapus_save = []
            save_data(folder_save,folder_ada,array_data_gadget_terhapus_save,"gadget_terhapus",header_gadget_terhapus,direk)
        save_data(folder_save,folder_ada,array_data_cons_histo_save,"consumable_history",header_cons_histo,direk)
        save_data(folder_save,folder_ada,array_data_borrow_save,"gadget_borrow_history",header_borrow,direk)
        save_data(folder_save,folder_ada,array_data_return,"gadget_return_history",header_return,direk)
    
        print("Saving...")
        print("Data telah disimpan pada folder " + folder_save)
        time.sleep(1)
        
        if konfirmasi_exit_akhir:
            sys.exit()

    #F16 Help
    if bool_menu_help == True: #Mengaktifkan menu help (13)
        print("Berikut adalah menu yang dapat Anda akses")
        helpmenu()
        pembatas()
        bool_menu_help = False
        bool_menu_setelah_login = True


    #F17 Exit
    while bool_menu_exit:
        pembatas()
        konfirmasi_menu_exit = input("Apakah anda yakin ingin keluar dari program?(y/n)(Anda akan diarahkan untuk save jika sudah login): ")
        konfirmasi_menu_exit = konfirmasi_menu_exit.lower()
        if logged and konfirmasi_menu_exit == "y":
            bool_menu_save_data = True
            bool_menu_exit = False
            konfirmasi_exit_akhir = True
        elif konfirmasi_menu_exit == "y":
            sys.exit()
        elif konfirmasi_menu_exit == "n":
            bool_menu_setelah_login = True
            bool_menu_exit = False
        else:
            print("Masukkan y atau n!")
