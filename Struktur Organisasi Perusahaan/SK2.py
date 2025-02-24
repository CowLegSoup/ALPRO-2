from collections import deque

# Inisialisasi struktur data
data_karyawan = {}

def tambah_karyawan():
    """
    Menambahkan karyawan baru ke dalam struktur data berdasarkan input pengguna.
    """
    id = input("Masukkan ID karyawan: ")
    if id in data_karyawan:
        print(f"Karyawan dengan ID {id} sudah ada.")
        return

    nama = input("Masukkan nama karyawan: ")
    jabatan = input("Masukkan jabatan karyawan: ")
    atasan = input("Masukkan ID atasan (kosongkan jika tidak ada): ")

    data_karyawan[id] = {
        "Nama": nama,
        "Jabatan": jabatan,
        "Atasan": atasan if atasan else None,
        "Bawahan": []
    }

    if atasan:
        if atasan in data_karyawan:
            data_karyawan[atasan]["Bawahan"].append(id)
        else:
            print(f"Atasan dengan ID {atasan} tidak ditemukan.")

def hapus_karyawan():
    """
    Menghapus karyawan berdasarkan ID yang dimasukkan pengguna.
    """
    id = input("Masukkan ID karyawan yang ingin dihapus: ")
    if id not in data_karyawan:
        print(f"Karyawan dengan ID {id} tidak ditemukan.")
        return

    # Hapus dari daftar bawahan atasan
    atasan = data_karyawan[id]["Atasan"]
    if atasan:
        data_karyawan[atasan]["Bawahan"].remove(id)

    # Hapus semua bawahan (rekursif)
    for bawahan in list(data_karyawan[id]["Bawahan"]):
        hapus_karyawan_by_id(bawahan)

    # Hapus karyawan dari data
    del data_karyawan[id]
    print(f"Karyawan dengan ID {id} telah dihapus.")

def hapus_karyawan_by_id(id):
    """
    Fungsi helper untuk menghapus karyawan secara rekursif.
    """
    if id not in data_karyawan:
        return

    atasan = data_karyawan[id]["Atasan"]
    if atasan:
        data_karyawan[atasan]["Bawahan"].remove(id)

    for bawahan in list(data_karyawan[id]["Bawahan"]):
        hapus_karyawan_by_id(bawahan)

    del data_karyawan[id]

def tampilkan_semua_karyawan():
    """
    Menampilkan semua karyawan dalam urutan hierarki.
    """
    def dfs_print(node_id, level=0):
        if node_id not in data_karyawan:
            return
        karyawan = data_karyawan[node_id]
        print("  " * level + f"ID: {node_id}, Nama: {karyawan['Nama']}, Jabatan: {karyawan['Jabatan']}")
        for bawahan in karyawan["Bawahan"]:
            dfs_print(bawahan, level + 1)

    # Cari semua root (karyawan tanpa atasan) dan tampilkan seluruh tree
    root_found = False
    for id, karyawan in data_karyawan.items():
        if not karyawan["Atasan"]:
            dfs_print(id)
            root_found = True

    if not root_found:
        print("Tidak ada karyawan.")

def tampilkan_subtree():
    """
    Menampilkan semua node dalam subtree tertentu berdasarkan ID yang dimasukkan pengguna.
    """
    node_id = input("Masukkan ID karyawan untuk menampilkan subtree: ")
    if node_id not in data_karyawan:
        print(f"Karyawan dengan ID {node_id} tidak ditemukan.")
        return

    def dfs_print(node_id, level=0):
        karyawan = data_karyawan[node_id]
        print("  " * level + f"ID: {node_id}, Nama: {karyawan['Nama']}, Jabatan: {karyawan['Jabatan']}")
        for bawahan in karyawan["Bawahan"]:
            dfs_print(bawahan, level + 1)

    dfs_print(node_id)

def cari_karyawan():
    """
    Mencari karyawan berdasarkan nama atau ID yang dimasukkan pengguna.
    """
    pilihan = input("Cari berdasarkan (1) Nama atau (2) ID? Masukkan pilihan (1/2): ")
    if pilihan == "1":
        nama = input("Masukkan nama karyawan: ")
        ditemukan = False
        for id, karyawan in data_karyawan.items():
            if karyawan["Nama"] == nama:
                print(f"ID: {id}, Nama: {karyawan['Nama']}, Jabatan: {karyawan['Jabatan']}")
                ditemukan = True
        if not ditemukan:
            print(f"Karyawan dengan nama {nama} tidak ditemukan.")
    elif pilihan == "2":
        id = input("Masukkan ID karyawan: ")
        if id in data_karyawan:
            karyawan = data_karyawan[id]
            print(f"ID: {id}, Nama: {karyawan['Nama']}, Jabatan: {karyawan['Jabatan']}")
        else:
            print(f"Karyawan dengan ID {id} tidak ditemukan.")
    else:
        print("Pilihan tidak valid.")

def generate_data_otomatis():
    """
    Menghasilkan data karyawan secara otomatis untuk pengujian.
    """
    # Data atasan (Manajemen)
    data_karyawan["1"] = {"Nama": "John Doe", "Jabatan": "CEO", "Atasan": None, "Bawahan": []}
    data_karyawan["2"] = {"Nama": "Jane Smith", "Jabatan": "Manager Operasional", "Atasan": "1", "Bawahan": []}
    data_karyawan["3"] = {"Nama": "Michael Johnson", "Jabatan": "Manager Keuangan", "Atasan": "1", "Bawahan": []}
    # Hubungkan root
    data_karyawan["1"]["Bawahan"].extend(["2", "3"])

    # Data supervisor
    data_karyawan["4"] = {"Nama": "Alice Brown", "Jabatan": "Supervisor Operasional", "Atasan": "2", "Bawahan": []}
    data_karyawan["5"] = {"Nama": "Bob White", "Jabatan": "Supervisor Logistik", "Atasan": "2", "Bawahan": []}
    data_karyawan["6"] = {"Nama": "Charlie Green", "Jabatan": "Supervisor IT", "Atasan": "2", "Bawahan": []}
    data_karyawan["7"] = {"Nama": "Diana Blue", "Jabatan": "Supervisor Akuntansi", "Atasan": "3", "Bawahan": []}
    data_karyawan["8"] = {"Nama": "Eva Black", "Jabatan": "Supervisor Perpajakan", "Atasan": "3", "Bawahan": []}
    data_karyawan["9"] = {"Nama": "Frank Gray", "Jabatan": "Supervisor Investasi", "Atasan": "3", "Bawahan": []}
    # Hubungkan supervisor dengan manajemen
    data_karyawan["2"]["Bawahan"].extend(["4", "5", "6"])
    data_karyawan["3"]["Bawahan"].extend(["7", "8", "9"])

    # Data staff
    data_karyawan["10"] = {"Nama": "Grace Yellow", "Jabatan": "Staff Operasional", "Atasan": "4", "Bawahan": []}
    data_karyawan["11"] = {"Nama": "Henry Pink", "Jabatan": "Staff Operasional", "Atasan": "4", "Bawahan": []}
    data_karyawan["12"] = {"Nama": "Ivy Purple", "Jabatan": "Staff Logistik", "Atasan": "5", "Bawahan": []}
    data_karyawan["13"] = {"Nama": "Jack Orange", "Jabatan": "Staff Logistik", "Atasan": "5", "Bawahan": []}
    data_karyawan["14"] = {"Nama": "Kevin Brown", "Jabatan": "Staff IT", "Atasan": "6", "Bawahan": []}
    data_karyawan["15"] = {"Nama": "Laura White", "Jabatan": "Staff IT", "Atasan": "6", "Bawahan": []}
    data_karyawan["16"] = {"Nama": "Mike Green", "Jabatan": "Staff Akuntansi", "Atasan": "7", "Bawahan": []}
    data_karyawan["17"] = {"Nama": "Nancy Blue", "Jabatan": "Staff Akuntansi", "Atasan": "7", "Bawahan": []}
    data_karyawan["18"] = {"Nama": "Oscar Black", "Jabatan": "Staff Perpajakan", "Atasan": "8", "Bawahan": []}
    data_karyawan["19"] = {"Nama": "Pauline Gray", "Jabatan": "Staff Perpajakan", "Atasan": "8", "Bawahan": []}
    data_karyawan["20"] = {"Nama": "Quincy Yellow", "Jabatan": "Staff Investasi", "Atasan": "9", "Bawahan": []}
    data_karyawan["21"] = {"Nama": "Rachel Pink", "Jabatan": "Staff Investasi", "Atasan": "9", "Bawahan": []}
    # Hubungkan staff dengan supervisor
    data_karyawan["4"]["Bawahan"].extend(["10", "11"])
    data_karyawan["5"]["Bawahan"].extend(["12", "13"])
    data_karyawan["6"]["Bawahan"].extend(["14", "15"])
    data_karyawan["7"]["Bawahan"].extend(["16", "17"])
    data_karyawan["8"]["Bawahan"].extend(["18", "19"])
    data_karyawan["9"]["Bawahan"].extend(["20", "21"])

    # Tambahan karyawan untuk mencapai 30 node
    data_karyawan["22"] = {"Nama": "Steve Purple", "Jabatan": "Staff Operasional", "Atasan": "4", "Bawahan": []}
    data_karyawan["23"] = {"Nama": "Tina Orange", "Jabatan": "Staff Logistik", "Atasan": "5", "Bawahan": []}
    data_karyawan["24"] = {"Nama": "Uma Brown", "Jabatan": "Staff IT", "Atasan": "6", "Bawahan": []}
    data_karyawan["25"] = {"Nama": "Victor White", "Jabatan": "Staff Akuntansi", "Atasan": "7", "Bawahan": []}
    data_karyawan["26"] = {"Nama": "Wendy Green", "Jabatan": "Staff Perpajakan", "Atasan": "8", "Bawahan": []}
    data_karyawan["27"] = {"Nama": "Xander Blue", "Jabatan": "Staff Investasi", "Atasan": "9", "Bawahan": []}
    data_karyawan["28"] = {"Nama": "Yara Black", "Jabatan": "Staff Operasional", "Atasan": "4", "Bawahan": []}
    data_karyawan["29"] = {"Nama": "Zack Gray", "Jabatan": "Staff Logistik", "Atasan": "5", "Bawahan": []}
    data_karyawan["30"] = {"Nama": "Amy Yellow", "Jabatan": "Staff IT", "Atasan": "6", "Bawahan": []}

    # Pastikan setiap karyawan yang memiliki atasan didaftarkan sebagai bawahan di data atasan
    for id, karyawan in data_karyawan.items():
        atasan = karyawan["Atasan"]
        if atasan:
            if id not in data_karyawan[atasan]["Bawahan"]:
                data_karyawan[atasan]["Bawahan"].append(id)

def main_menu():
    """
    Menampilkan menu utama dan memproses pilihan pengguna.
    """
    # Generate data otomatis saat program dimulai
    generate_data_otomatis()

    while True:
        print("\n=== Sistem Manajemen Karyawan ===")
        print("1. Tambah Karyawan")
        print("2. Hapus Karyawan")
        print("3. Tampilkan Semua Karyawan")
        print("4. Tampilkan Subtree")
        print("5. Cari Karyawan")
        print("6. Keluar")
        pilihan = input("Masukkan pilihan (1-6): ")

        if pilihan == "1":
            tambah_karyawan()
        elif pilihan == "2":
            hapus_karyawan()
        elif pilihan == "3":
            tampilkan_semua_karyawan()
        elif pilihan == "4":
            tampilkan_subtree()
        elif pilihan == "5":
            cari_karyawan()
        elif pilihan == "6":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main_menu()

