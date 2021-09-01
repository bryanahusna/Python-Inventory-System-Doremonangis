def dapatkan_indeks(id, daftar_item):
  # Fungsi yang berfungsi mencari indeks dari id di daftar_item
  # Misal mencari indeks G1 di data_gadget
  # Return indeks tersebut, atau -1 jika tidak ada
	for i in range(len(daftar_item)):
		if daftar_item[i][0] == id:
			return i
	return -1	# Jika tidak ditemukan id tersebut, return -1

def dapatkan_indeks_col(id, daftar_item, col):
  # Fungsi yang berfungsi mencari indeks dari komponen kolom di daftar_item
  # Misal mencari indeks Dorayaki di data_gadget
    for i in range(len(daftar_item)):
        if daftar_item[i][col] == id:
            return i
    return -1

def csv_parser(location):
    csvfile = open(location, 'r')
    raw_list = csvfile.readlines()
    result_list = [pecah_string(x, ';') for x in raw_list]
    csvfile.close()
    return result_list


def pecah_string(s, pemisah):
    s = s.strip()
    isebelum = 0
    hasil = []
    for i in range(len(s)):
        if s[i] == pemisah:
            if s[isebelum+1:i].isdigit():
                hasil.append(int(s[isebelum+1:i]))
            else:
                hasil.append(s[isebelum+1:i])
            isebelum = i
    
    if s[isebelum+1:len(s)].isdigit():
        hasil.append(int(s[isebelum+1:len(s)]))
    else:
        hasil.append(s[isebelum+1:len(s)])

    hasil[0] = s[0] + hasil[0]
    if hasil[0].isdigit():
        hasil[0] = int(hasil[0])
    return hasil