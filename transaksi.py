import const
import additional_tools

hari_bulan_biasa = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
hari_bulan_kabisat = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isKabisat(tahun):
  if (tahun % 400) == 0:
    return True
  elif (tahun % 100) != 0 and (tahun % 4) == 0:
    return True
  else:
    return False

def cek_tanggal(tanggal):
  tanggal = tanggal.strip()
  if tanggal[0:2].isdigit() and tanggal[3:5].isdigit():
    if tanggal[6] == '-' and tanggal[7:11].isdigit() and len(tanggal) == 11:
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

# F08 - Meminjam Gadget
def pinjam_gadget(list_gadget, riwayat_pinjam_gadget, id_user):
    print('Masukan ID Gadget yang ingin dipinjam, atau 99 untuk batal')
    isIdValid = False
    while not isIdValid:
      id_item = input('Masukan ID item: ')
      if id_item == '99':
        return False
      indeks = additional_tools.dapatkan_indeks(id_item,list_gadget)
      if indeks == -1:
        print('ID item tidak ada di inventori')
      else:
        isIdValid = True

    jumlah_tersedia = list_gadget[indeks][const.G_JUM]
    nama_gadget = list_gadget[indeks][const.G_NAMA]
    print('{0}, jumlah tersedia: {1}'.format(nama_gadget, jumlah_tersedia))
      
    jumlah = input('Jumlah peminjaman: ')
    isJumlahValid = False
    while not isJumlahValid:
      if not jumlah.isdigit():
        print('Masukan jumlah tidak valid! Coba lagi')
        jumlah = input('Jumlah peminjaman: ')
      elif int(jumlah) > jumlah_tersedia:
        print('Gagal! Jumlah item di inventori kurang dari yang ingin dipinjam! Coba lagi')
        print('Jumlah item {0} di Inventori: {1}'.format(list_gadget[indeks][const.G_NAMA], jumlah_tersedia))
        jumlah = input('Jumlah peminjaman: ')
      else:
        isJumlahValid = True
        jumlah = int(jumlah)

    isTanggalValid = False
    while not isTanggalValid:
      tanggal = input('Tanggal peminjaman (dd/mm/yyyy): ')
      isTanggalValid = cek_tanggal(tanggal)
      if not isTanggalValid:
        print('Masukan tanggal tidak valid! Tanggal tidak benar/Format harus dd/mm/yyyy')

    riwayat_pinjam_gadget.append(['PG' + str(len(riwayat_pinjam_gadget)+1), id_user, id_item, tanggal, jumlah, False])
    list_gadget[indeks][const.G_JUM] -= jumlah
    print('Item {0} ({1}) berhasil dipinjam!'.format(nama_gadget, jumlah))
    print('Sisa item {0} di inventori: {1}'.format(nama_gadget, jumlah_tersedia-jumlah))
    return True
      
# F09 - Mengembalikan Gadget
def kembali_gadget(list_gadget, riwayat_kembali_gadget, riwayat_pinjam, id_user, list_gadget_terhapus):
    print("Daftar yang Dipinjam")
    print("No. Nama Gadget x jumlah | ID Peminjaman | Tanggal Peminjaman")

    urut = 1
    daftar_id_pinjam = []
    for i in range(len(riwayat_pinjam)):
        if id_user == riwayat_pinjam[i][const.PG_ID_PEMINJAM] and riwayat_pinjam[i][const.PG_ISKEMBALI] == False:
            id_peminjaman = riwayat_pinjam[i][const.PG_ID] 
            id_gadget = riwayat_pinjam[i][const.PG_ID_GADGET]
            igadget = additional_tools.dapatkan_indeks(id_gadget, list_gadget)
            nama_gadget = list_gadget[igadget][const.G_NAMA]
            tanggal_pinjam = riwayat_pinjam[i][const.PG_TANGGAL]
            jumlah = riwayat_pinjam[i][const.PG_JUMLAH]

            print('{0}. {1} x {2} | ID: {3} | {4}'.format(urut, nama_gadget, jumlah, id_peminjaman, tanggal_pinjam))
            daftar_id_pinjam.append(id_peminjaman)
            urut += 1
            #jumlah_pinjam = riwayat_pinjam[i][const.PG_JUMLAH]
            
            #for entri in daftar_barang_user:
            #  if id_gadget in entri:
            #    entri[0].append(riwayat_pinjam[i][0])
            #    entri[3] += jumlah_pinjam[i][0]
            #  else:
            #    daftar_barang_user.append([[riwayat_pinjam[i][[0]], id_gadget, #list_gadget[igadget][const.G_NAMA], jumlah_pinjam, igadget]])

    #for j in range(len(daftar_barang_user)):
    #  print('{0}. {1} | {2}'.format(j+1, daftar_barang_user[j][2], daftar_barang_user[j][3]))
    print('\n-99. Kembali ke Menu Utama\n')
    isPilihanValid = False
    while not isPilihanValid:
      nomor_pilihan = input('Masukan nomor: ')
      if nomor_pilihan == '-99':
        return False
      elif not nomor_pilihan.isdigit():
        print('Masukan tidak valid! Coba lagi')
        nomor_pilihan = input('Masukan nomor peminjaman: ')
      elif nomor_pilihan == '0' or int(nomor_pilihan) > (urut - 1):
        print('Pilihan di luar batas! Coba lagi')
        nomor_pilihan = input('Masukan nomor peminjaman: ')
      else:
        isPilihanValid = True
        nomor_pilihan = int(nomor_pilihan)

    isTanggalValid = False
    while not isTanggalValid:
      tanggal = input('Tanggal pengembalian (dd/mm/yyyy): ')
      isTanggalValid = cek_tanggal(tanggal)
      if not isTanggalValid:
        print('Masukan tanggal tidak valid! Tanggal tidak benar/Format harus dd/mm/yyyy')
    
    id_peminjaman_terpilih = daftar_id_pinjam[nomor_pilihan - 1]
    indeks_terpilih = additional_tools.dapatkan_indeks(id_peminjaman_terpilih, riwayat_pinjam)

    riwayat_pinjam[indeks_terpilih][const.PG_ISKEMBALI] = True
    riwayat_kembali_gadget.append(['KG' + str(len(riwayat_kembali_gadget)+1), id_peminjaman_terpilih, tanggal])

    jumlah_kembali = riwayat_pinjam[indeks_terpilih][const.PG_JUMLAH]
    id_gadget = riwayat_pinjam[indeks_terpilih][const.PG_ID_GADGET]
    igadget = additional_tools.dapatkan_indeks(id_gadget, list_gadget)
    if igadget == -1:
      igadgethapus = additional_tools.dapatkan_indeks(id_gadget, list_gadget_terhapus)
      nama_gadget = list_gadget_terhapus[igadgethapus][const.G_NAMA]
      list_gadget_terhapus[igadgethapus][const.G_JUM] = jumlah_kembali
      list_gadget.append(list_gadget_terhapus[igadgethapus].copy())
      del(list_gadget_terhapus[igadgethapus])
    else:
      list_gadget[igadget][const.G_JUM] += jumlah_kembali
      nama_gadget = list_gadget[igadget][const.G_NAMA]
    print('Pengembalian {0} x {1} berhasil!'.format(nama_gadget, jumlah_kembali))
    return True
    #barang_terpilih = daftar_barang_user[nomor_pilihan-1]
    #urutan = barang_terpilih[0]
    #id_gadget = barang_terpilih[1]
    #nama_gadget = barang_terpilih[2]
    #jumlah_kembali = barang_terpilih[3]
    #gadget_indeks = barang_terpilih[4]

    #for i in riwayat_pinjam:
    #  if riwayat_pinjam[i][const.PG_ID_GADGET] == id_gadget:
    #    riwayat_pinjam[i][const.PG_ISKEMBALI] = True
    #    id_kembali = len(riwayat_kembali_gadget)+1
    #    id_peminjaman = riwayat_pinjam[i][const.PG_ID]
    #    riwayat_kembali_gadget.append([id_kembali, id_peminjaman, tanggal])
        
    #print('Item {0} sebanyak {1} telah dikembalikan'.format(nama_gadget, jumlah_kembali))
    #gadget_indeks = additional_tools.dapatkan_indeks(id_gadget, list_gadget)
    #if gadget_indeks == -1:
    #  new_gadget = [id_gadget, '', '', jumlah_kembali, '', '']
    #  list_gadget.append(new_gadget)
    #else:
    #  list_gadget[gadget_indeks][const.G_JUM] += jumlah_kembali

# F10 - Meminta Consumable
def minta_consum(list_consum, riwayat_ambil_consum, id_user):
    print('Masukan ID consum untuk mengambil, atau 99 untuk batal')
    id_consum = input('Masukan ID consum: ')
    if id_consum == '99':
      return False
    iconsum = additional_tools.dapatkan_indeks(id_consum, list_consum)
    while iconsum == -1:
        print('ID tidak ada di inventori consum! Coba lagi')
        id_consum = input('Masukan ID consum: ')
        if id_consum == '99':
          return False
        iconsum = additional_tools.dapatkan_indeks(id_consum, list_consum)
        
    jumlah_tersedia = list_consum[iconsum][const.C_JUM]
    nama_consum = list_consum[iconsum][const.C_NAMA]
    print('Consum {0}, jumlah tersedia: {1}'.format(nama_consum, jumlah_tersedia))

    isJumlahValid = False
    while not isJumlahValid:
      jumlah_minta = input('Jumlah Minta: ')
      if not jumlah_minta.isdigit():
        print('Masukan tidak valid! Harus angka 0 atau positif')
      else:
        jumlah_minta = int(jumlah_minta)
        if jumlah_minta > jumlah_tersedia:
          print('Gagal! Permintaan melebihi stok yang tersedia, coba lagi')
        else:
          isJumlahValid = True

    isTanggalValid = False
    while not isTanggalValid:
      tanggal = input('Tanggal permintaan (dd/mm/yyyy): ')
      isTanggalValid = cek_tanggal(tanggal)
      if not isTanggalValid:
        print('Masukan tanggal tidak valid! Tanggal tidak benar/Format harus dd/mm/yyyy')
    
    list_consum[iconsum][const.C_JUM] -= jumlah_minta
    riwayat_ambil_consum.append(['MC' + str(len(riwayat_ambil_consum)+1), id_user, id_consum, tanggal, jumlah_minta])

    print('Berhasil diambil item {0} sebanyak {1}'.format(list_consum[iconsum][const.C_NAMA], jumlah_minta))
    return True