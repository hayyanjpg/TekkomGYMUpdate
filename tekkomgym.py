import json

# Data database
users = [
    {'user_id': 1, 'alamat': 'Jl. Fitness', 'nama': 'Hayyan'},
    {'user_id': 2, 'alamat': 'Jl. Kesehatan', 'nama': 'Aisyah'},
    {'user_id': 3, 'alamat': 'Jl. Kebugaran', 'nama': 'Rudi'},
    {'user_id': 4, 'alamat': 'Jl. Olahraga', 'nama': 'Dewi'},
    {'user_id': 5, 'alamat': 'Jl. Sehat', 'nama': 'Joko'},
]

products = [
    {'produk_id': 1, 'nama_produk': 'Suplemen', 'jumlah_produk': 50},
    {'produk_id': 2, 'nama_produk': 'Membership Bulanan', 'jumlah_produk': 100},

]

tax_categories = [
    {'item_category': 'S', 'tax_rate': 0.15},  # Suplemen dengan 15% pajak
    {'item_category': 'M', 'tax_rate': 0.1}   # Membership dengan 10% pajak
]

# Fungsi untuk menyimpan data ke berkas JSON
def save_data_to_file():
    data = {
        "users": users,
        "products": products,
        "tax_categories": tax_categories,
    }
    with open('data.json', 'w') as file:
        json.dump(data, file)
    print("Data berhasil disimpan ke data.json")

# Fungsi untuk memuat data dari berkas JSON
def load_data_from_file():
    global users, products, tax_categories
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            users = data['users']
            products = data['products']
            tax_categories = data['tax_categories']
        print("Data berhasil dimuat dari data.json")
    except FileNotFoundError:
        print("Berkas data.json tidak ditemukan, menggunakan data default.")

# Fungsi untuk menampilkan menu
def display_menu():
    print("\n=== Menu Aplikasi Gym ===")
    print("1. Hitung Pajak Penjualan")
    print("2. Cari Anggota Gym")
    print("3. Cari Produk Gym")
    print("4. Tambah Produk")
    print("5. Update Jumlah Produk")
    print("6. Hapus Produk")
    print("0. Keluar")

# Prosedur untuk menghitung pajak penjualan
def compute_sales_tax(item_type: str, sales_amount: int):
    if not isinstance(sales_amount, (int, float)) or sales_amount < 0:
        print("Jumlah penjualan harus berupa angka positif")
        return None

    for category in tax_categories:
        if item_type.upper() == category['item_category']:
            sales_tax = sales_amount * category['tax_rate']
            print(f"Pajak untuk item {item_type.upper()}: {sales_tax}")
            return sales_tax

    print("Item tidak valid. Gunakan 'S' untuk Suplemen atau 'M' untuk Membership")
    return None

# Prosedur lain (find_user_by_id, find_product_by_id, add_product, update_product_quantity, delete_product) di sini...

# Fungsi untuk menjalankan program
def main():
    load_data_from_file()  # Memuat data saat program dimulai
    while True:
        display_menu()  # Menampilkan menu
        choice = input("Pilih opsi (0-6): ")

        if choice == '1':
            item_type = input("Masukkan jenis item (S untuk Suplemen, M untuk Membership): ")
            sales_amount = float(input("Masukkan jumlah penjualan: "))
            compute_sales_tax(item_type, sales_amount)

        elif choice == '2':
            user_id = int(input("Masukkan ID pengguna: "))
            find_user_by_id(user_id)

        elif choice == '3':
            produk_id = int(input("Masukkan ID produk: "))
            find_product_by_id(produk_id)

        elif choice == '4':
            produk_id = int(input("Masukkan ID produk: "))
            nama_produk = input("Masukkan nama produk: ")
            jumlah_produk = int(input("Masukkan jumlah produk: "))
            add_product(produk_id, nama_produk, jumlah_produk)

        elif choice == '5':
            produk_id = int(input("Masukkan ID produk yang ingin diupdate: "))
            jumlah_produk = int(input("Masukkan jumlah produk baru: "))
            update_product_quantity(produk_id, jumlah_produk)

        elif choice == '6':
            produk_id = int(input("Masukkan ID produk yang ingin dihapus: "))
            delete_product(produk_id)

        elif choice == '0':
            save_data_to_file()  # Menyimpan data saat keluar
            print("Terima kasih! Program selesai.")
            break

        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
