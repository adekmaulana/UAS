import sys
import datetime
import locale

from random import sample
from time import sleep
from shutil import get_terminal_size
from sql_helper.manager import get_item, update_item


def rupiah_format(angka, with_prefix=False, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
    rupiah = locale.format_string("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah


def clear():
    print("\n" * get_terminal_size().lines, end='')


def get_harga(ukuran: str) -> str:
    data = {
        "XXL": 160000,
        "XL": 157500,
        "L": 155000,
        "M": 152500,
        "S": 150000
    }
    return data.get(ukuran)


def cetak_katalog():
    print("-------------------------------------------------------")
    print("|                    Boxer Olahraga                   |")
    print("|                        Avalon                       |")
    print("|-----------------------------------------------------|")
    print("|  Kode Item  |   Warna Item   |        Ukuran        |")
    print("|     PTH     |      PUTIH     |   XXL, XL, L, M, S   |")
    print("|     HTM     |      HITAM     |   XXL, XL, L, M, S   |")
    print("|     AB2     |     ABU-ABU    |   XXL, XL, L, M, S   |")
    print("|     NVY     |      NAVY      |   XXL, XL, L, M, S   |")
    print("|-----------------------------------------------------|")
    print("|                        Harga                        |")
    print("|-----------------------------------------------------|")
    print("|   • XXL ->  Rp. 160.000                             |")
    print("|   • XL  ->  Rp. 157.500                             |")
    print("|   •  L  ->  Rp. 155.000                             |")
    print("|   •  M  ->  Rp. 152.500                             |")
    print("|   •  S  ->  Rp. 150.000                             |")
    print("-------------------------------------------------------")


if __name__ == "__main__":
    jumlah_beli = 0
    list_boxer = []
    list_harga = []
    list_banyak = []
    list_ukuran = []

    while True:
        cetak_katalog()
        kode = input("Masukkan kode item '[PTH/HTM/AB2/NVY]': ")
        ukuran = input("Pilih ukuran boxer '[XXL/XL/L/M/S]': ")
        boxer = get_item(kode.upper())
        harga = get_harga(ukuran.upper())
        # Jika kode tidak terdaftar, ulang looping
        if boxer is None:
            print("Kode boxer tidak terdaftar!")
            sleep(2.5)
            clear()
            cetak_katalog()
            continue
        # Jika ukuran tidak terdaftar, ulang looping
        if harga is None:
            print("Maaf ukuran belum ada...")
            sleep(2.5)
            clear()
            cetak_katalog()
            continue
        banyak_beli = int(input("Masukkan banyak beli: "))
        # Check stock boxer pada database
        quantity = boxer.ukuran.get(ukuran).get('quantity')
        # Beritahu jika stock tidak ada
        if quantity == 0:
            print(f"Maaf, {boxer.warna.upper()} ({ukuran.upper()}) belum tersedia")
            sleep(2.5)
            clear()
            cetak_katalog()
            continue
        elif banyak_beli > quantity:
            print(f"Maaf, {boxer.warna.upper()} ({ukuran.upper()}) hanya tersedia {quantity}")
            sleep(2.5)
            clear()
            cetak_katalog()
            continue
        list_boxer.append(boxer.warna)
        list_harga.append(harga)
        list_banyak.append(banyak_beli)
        list_ukuran.append(ukuran)
        jumlah_beli += 1
        # Kurangi stock pada database ketika logika di atas sudah terpenuhi
        update_item(boxer, ukuran, banyak_beli)
        print()
        lagi = input("Tambah barang lagi? '[Y/N]': ")
        if lagi.upper() == "Y":
            clear()
            continue
        else:
            break
    clear()
    d = datetime.datetime.now()
    no = sample(range(1, 100), 3)
    order = f"#GG{no[0]}{no[1]}{no[2]}"
    print("\t*---Avalon Sports---*\t")
    print()
    print(f"{d:%d}/{d:%m}/{d:%y} {d:%H}:{d:%M}:{d:%S} {d:$p}\t  ORDER: {order}")
    print()
    total_bayar = []
    for i in range(jumlah_beli):
        jumlah = list_harga[i] * list_banyak[i]
        total_bayar.append(jumlah)
        print(f"\t{list_banyak[i]} {list_boxer[i].upper()} ({list_ukuran[i]})\t| "
              f"{rupiah_format(jumlah, with_prefix=True, desimal=0)}")
    raw_total = sum(total_bayar)
    tax = round(raw_total * 0.1)
    total = raw_total + tax
    print(f"\tSUBTOTAL\t| {rupiah_format(raw_total, with_prefix=True, desimal=0)}")
    print(f"\tPPN 10%\t\t| {rupiah_format(tax, with_prefix=True, desimal=0)}")
    print(f"\tTOTAL\t\t| {rupiah_format(total, with_prefix=True, desimal=0)}")
    uang_bayar = int(input("\tUANG\t\t| Rp. "))
    # Loop jika uang bayar kurang dari total bayar
    while uang_bayar < total:
        if uang_bayar < total:
            # Bersihkan stdout jika user input kurang dari total bayar
            sys.stdout.write("\033[1A\033[2K")
        uang_bayar = int(input("\tUANG\t\t| Rp. "))
    kembali = rupiah_format(uang_bayar - total, with_prefix=True, desimal=0)
    sys.stdout.write("\033[1A\033[2K")
    print(f"\tUANG\t\t| {rupiah_format(uang_bayar, with_prefix=True, desimal=0)}")
    print(f"\tCHANGE\t\t| {kembali}")
