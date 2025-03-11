import time
waktu_mulai = time.time()

def kantin_hilda():
    print("KANTIN AI HILDA")
    print("---------------")
    
    # Menu tersedia
    menu = {
        "Ayam Bumbu Bebek": 15000,
        "Es Teh": 5000,
        "Onigiri": 11000,
    }
    
    # Tampilkan menu
    for nama, harga in menu.items():
        print(f"{nama}: Rp {harga}")
    
    # Input pesanan
    n = int(input("\nJumlah jenis pesanan: "))
    
    total = 0
    
    # Proses pesanan
    for i in range(n):
        nama = input(f"Menu ke-{i+1}: ")
        harga = menu.get(nama, int(input("Harga: ")))
        jumlah = int(input("Jumlah: "))
        
        subtotal = harga * jumlah
        total += subtotal
        print(f"Subtotal: Rp {subtotal}\n")
    waktu_akhir = time.time()

    print(f"TOTAL: Rp {total}")
    print(f"Waktu: {waktu_akhir - waktu_mulai:.4f} detik")

kantin_hilda()
