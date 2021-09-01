import const
import alat

# Daftar Konten Modul
# F05 - Menambah Item
# F06 - Menghapus Gadget atau Consumable
# F07 - Mengubah Jumlah Gadget atau Consumable pada Inventory


# F05 - Menambah Item
def tambah_item(list_gadget, list_consum, list_gadget_terhapus):
    print('Masukan ID yang ingin ditambahkan, atau "batal" untuk kembali ke menu')
    isIdValid = False
    while not isIdValid:
        # Pengecekan ID, ID harus diawali 'G' atau 'C', juga mengecek apakah ID sudah ada di data (dapatkan_indeks(id, data) akan return -1 jika ID belum ada)
        id = input('Masukan ID\t\t\t: ')
        if id == 'batal':
            return False
        elif id[0] == 'G':
            if alat.dapatkan_indeks(
                    id, list_gadget) == -1 and alat.dapatkan_indeks(
                        id, list_gadget_terhapus) == -1:  # Validasi
                tambah_gadget(id, list_gadget)
                isIdValid = True
            else:
                print('ID sudah ada! Coba yang lain\n')
        elif id[0] == 'C':
            if alat.dapatkan_indeks(id, list_consum) == -1:
                tambah_consum(id, list_consum)
                isIdValid = True
            else:
                print('ID sudah ada! Coba yang lain\n')
        else:
            print('ID item tidak valid! Silakan masukan lagi (Harus diawali G atau C)\n')
    return True


def tambah_gadget(id, list_gadget):
    nama = input('Masukan Nama\t\t: ')
    while nama == '':
        print('Nama tidak boleh kosong!\n')
        nama = input('Masukan Nama\t\t: ')
    deskripsi = input('Masukan Deskripsi\t: ')

    isJumlahValid = False
    while not isJumlahValid:
        jumlah = input('Masukan Jumlah\t\t: ')
        if not jumlah.isdigit() or int(jumlah) < 0:
            print('Masukan tidak valid! Harus angka nol atau positif\n')
        else:
            jumlah = int(jumlah)
            isJumlahValid = True

    rarity = input('Masukan Rarity\t\t: ')
    while rarity != 'C' and rarity != 'B' and rarity != 'A' and rarity != 'S':
        print('Input rarity tidak valid! Harus C, B, A, atau S\n')
        rarity = input('Masukan Rarity\t\t: ')

    isTahunValid = False
    while not isTahunValid:
        tahun = input('Masukan tahun ditemukan\t: ')
        tahun = tahun.strip()
        if tahun.isdigit():
            isTahunValid = True
        elif tahun[0] == '-' and tahun[1:].isdigit():
            isTahunValid = True
        else:
            print('Tahun tidak valid! Coba lagi\n')

    tahun = int(tahun)

    list_gadget.append([id, nama, deskripsi, jumlah, rarity, tahun])
    print('\nItem gadget {0} telah berhasil ditambahkan ke database.\n'.format(
        nama))


def tambah_consum(id, list_consum):
    nama = input('Masukan Nama\t\t: ')
    while nama == '':
        print('Nama tidak boleh kosong!\n')
        nama = input('Masukan Nama\t\t: ')
    deskripsi = input('Masukan Deskripsi\t: ')

    isJumlahValid = False
    while not isJumlahValid:
        jumlah = input('Masukan Jumlah\t\t: ')
        if not jumlah.isdigit() or int(jumlah) < 0:
            print('Masukan tidak valid! Harus angka nol atau positif\n')
        else:
            jumlah = int(jumlah)
            isJumlahValid = True

    rarity = input('Masukan Rarity\t\t: ')
    while rarity != 'C' and rarity != 'B' and rarity != 'A' and rarity != 'S':
        print('Input rarity tidak valid! Harus C, B, A, atau S\n')
        rarity = input('Masukan Rarity\t\t: ')

    list_consum.append([id, nama, deskripsi, jumlah, rarity])
    print('\nItem consumable {0} telah berhasil ditambahkan ke database.\n'
    .format(nama))


# F06 - Menghapus Gadget atau Consumable
def hapus_item(list_gadget, list_consum, list_terhapus):
    # Return True jika sukses menghapus
    print('Masukan ID untuk menghapus, atau "batal" untuk kembali ke menu')
    isIdValid = False
    while not isIdValid:
        id = input('Masukan ID\t\t\t: ')
        if id == 'batal':
            return False
        igadget = alat.dapatkan_indeks(id, list_gadget)
        iconsum = alat.dapatkan_indeks(id, list_consum)
        if igadget != -1:
            list_gadget[igadget][const.G_JUM] = 0
            list_terhapus.append(list_gadget[igadget].copy())
            del (list_gadget[igadget])
            print('\nItem telah berhasil dihapus dari database')
            isIdValid = True
            return True
        elif iconsum != -1:
            del (list_consum[iconsum])
            print('\nItem telah berhasil dihapus dari database')
            isIdValid = True
            return True
        else:
            print('\nTidak ada item dengan ID tersebut! Coba lagi')


# F07 - Mengubah Jumlah Gadget atau Consumable pada Inventory
def ubah_jumlah(list_gadget, list_consum):
    print('Masukan ID yang ingin diedit, atau "batal" untuk kembali ke menu')
    isIdValid = False
    while not isIdValid:
        id = input('Masukan ID\t\t: ')
        if id == 'batal':
            return False
        igadget = alat.dapatkan_indeks(id, list_gadget)
        iconsum = alat.dapatkan_indeks(id, list_consum)
        if igadget != -1:
            jumlah = list_gadget[igadget][const.G_JUM]
            perubahan = input('Masukan Jumlah\t: ')
            while not perubahan.isdigit() and not (perubahan[0] == '-' and perubahan[1:].isdigit()):
                print('Masukan tidak valid! Harus berupa angka')
                perubahan = input('Masukan Jumlah\t: ')
            perubahan = int(perubahan)
            hasil = jumlah + perubahan
            print()
            if hasil >= 0:
                list_gadget[igadget][const.G_JUM] = hasil
                if perubahan >= 0:
                    print(perubahan, list_gadget[igadget][const.G_NAMA],
                          'berhasil ditambahkan. Stok sekarang:', hasil)
                else:
                    print(-1 * perubahan, list_gadget[igadget][const.G_NAMA],
                          'berhasil dibuang. Stok sekarang:', hasil)
                isIdValid = True
                return True
            else:
                print(-1 * perubahan, list_gadget[igadget][const.G_NAMA],
                      'gagal dibuang karena stok kurang. Stok sekarang:',
                      jumlah)
                return True

        elif iconsum != -1:
            jumlah = list_consum[iconsum][const.C_JUM]
            perubahan = input('Masukan Jumlah\t: ')
            while not perubahan.isdigit() and not (perubahan[0] == '-' and perubahan[1:].isdigit()):
                print('Masukan tidak valid! Harus berupa angka')
                perubahan = input('Masukan Jumlah\t: ')
            perubahan = int(perubahan)
            hasil = jumlah + perubahan
            print()
            if hasil >= 0:
                list_consum[iconsum][const.G_JUM] = hasil
                if perubahan >= 0:
                    print(perubahan, list_consum[iconsum][const.C_NAMA],
                          'berhasil ditambahkan. Stok sekarang:', hasil)
                else:
                    print(-1 * perubahan, list_consum[iconsum][const.C_NAMA],
                          'berhasil dibuang. Stok sekarang:', hasil)
                    isIdValid = True
                return True
            else:
                print(-1 * perubahan, list_consum[iconsum][const.C_NAMA],
                      'GAGAL DIBUANG!, karena stok kurang. Stok sekarang:',
                      jumlah)
                isIdValid = True
                return True

        else:
            print('Tidak ada item dengan ID tersebut!')
