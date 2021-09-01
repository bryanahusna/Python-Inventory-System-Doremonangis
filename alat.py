'Modul alat untuk mempermudah karena sering digunakan'
# Dibuat dan diimplementasikan sendiri


def deepcopy(array_data):
    # Return salinan array
    # Menghindari pengubahan di dalam beberapa fungsi tertentu tiba-tiba mengubah array original di pemanggil
    # Seperti ketika memproses array untuk disimpan di database csv yang melibatkan pengubahan int ke string
    # Terinspirasi dari https://www.programiz.com/python-programming/shallow-deep-copy , dibuat dan diimplementasikan sendiri
    copied_array = []
    for i in array_data:
        copied_array.append(i.copy())
    return copied_array


def dapatkan_indeks(id, daftar_item):
    # Return indeks data dengan id tertentu di daftar_item, -1 jika tidak ada
    # Fungsi yang berfungsi mencari indeks dari id di daftar_item
    # Karena sering dipakai, bagus untuk dibuat fungsi
    for i in range(len(daftar_item)):
        if daftar_item[i][0] == id:
            return i
    return -1  # Jika tidak ditemukan id tersebut, return -1


def dapatkan_indeks_col(nilai, daftar_item, col):
    # Return indeks data dengan nilai tertentu pada column tertentu di daftar_item
    # Fungsi yang berfungsi mencari indeks data dengan nilai tertentu dari kolom tertentu (seperti deskripsi, nama, dll.) di daftar_item
    for i in range(len(daftar_item)):
        if daftar_item[i][col] == nilai:
            return i
    return -1

# Daftar jumlah hari di tahun biasa dan kabisat, untuk menentukan apakah tanggal valid
# Terinspirasi dari The C Programming Language, 2nd Edition (Brian W. Kernighan, 1998)
hari_bulan_biasa = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
hari_bulan_kabisat = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isKabisat(tahun):
    # Return True jika tahun kabisat, False jika tidak
    if (tahun % 400) == 0:
        return True
    elif (tahun % 100) != 0 and (tahun % 4) == 0:
        return True
    else:
        return False


def cek_tanggal(tanggal):
    # Return True jika tanggal valid dan sesuai format, False jika tidak
    # Mengecek apakah tanggal, bulan, dan tahun valid dan sesuai format
    # Yang tidak valid seperti 32/01/2001, 15/15/2001, atau 29/02/2019
    tanggal = tanggal.strip()
    if tanggal[0:2].isdigit() and tanggal[3:5].isdigit():
        if tanggal[6] == '-' and tanggal[7:11].isdigit() and len(
                tanggal) == 11:
            tahun = -1 * int(tanggal[7:11])
        elif tanggal[6:10].isdigit() and len(tanggal) == 10:
            tahun = int(tanggal[6:10])
        else:
            return False

        hari = int(tanggal[0:2])
        bulan = int(tanggal[3:5])
        if hari == 0 or (bulan == 0 or bulan > 12):
            return False

        if isKabisat(tahun):
            if hari > hari_bulan_kabisat[bulan]:
                return False
        else:
            if hari > hari_bulan_biasa[bulan]:
                return False
        return True

    else:
        return False
