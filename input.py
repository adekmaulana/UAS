import sys
import datetime

from random import sample
from receipt import parse_data, parse_order, cv, rupiah_format, windows, subprocess_run
from time import sleep
from shutil import get_terminal_size
from sql_helper.manager import get_item, update_item


def delete_last_lines(n=1):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.flush()


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
    print("|                    Avalon Sports                    |")
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
            continue
        # Jika ukuran tidak terdaftar, ulang looping
        if harga is None:
            print("Maaf ukuran belum ada...")
            sleep(2.5)
            clear()
            continue
        banyak_beli = int(input("Masukkan banyak beli: "))
        # Check stock boxer pada database
        quantity = boxer.ukuran.get(ukuran).get('quantity')
        # Beritahu jika stock tidak ada
        if quantity == 0:
            print(f"Maaf, {boxer.warna.upper()} ({ukuran.upper()}) belum tersedia")
            sleep(2.5)
            clear()
            continue
        elif banyak_beli > quantity:
            print(f"Maaf, {boxer.warna.upper()} ({ukuran.upper()}) hanya tersedia {quantity}")
            sleep(2.5)
            clear()
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
        elif lagi.upper() == "N":
            break
        else:
            print('Jawaban anda diluar pertanyaan')
            break
    clear()
    d = datetime.datetime.now()
    no = sample(range(1, 100), 3)
    order = f"#AV{no[0]}{no[1]}{no[2]}"
    print("\t*===AVALON SPORTS===*\t")
    print()
    print(f"{d:%d}/{d:%m}/{d:%y} {d:%I}:{d:%M}:{d:%S} {d:%p}\t  ORDER: {order}")
    print()

    total_bayar = []
    list_belanja = []

    for i in range(jumlah_beli):
        list_belanja.append(
            f"{list_banyak[i]} {list_boxer[i].upper()} ({list_ukuran[i]})")
        jumlah = list_harga[i] * list_banyak[i]
        total_bayar.append(jumlah)
        print(f"\t{list_belanja[i]}\t| {rupiah_format(jumlah)}")

    raw_total = sum(total_bayar)
    tax = round(raw_total * 0.1)
    total = raw_total + tax

    print()
    print(f"\tSUBTOTAL\t| {rupiah_format(raw_total)}")
    print(f"\tPPN 10%\t\t| {rupiah_format(tax)}")
    print(f"\tTOTAL\t\t| {rupiah_format(total)}")

    uang_bayar = int(input("\tUANG\t\t| Rp. "))
    # Loop jika uang bayar kurang dari total bayar
    while uang_bayar < total:
        if uang_bayar < total:
            if windows is False:
                # Bersihkan stdout jika user input kurang dari total bayar
                delete_last_lines(1)
            else:
                clear()
                print("\t*===AVALON SPORTS===*\t")
                print()
                print(f"{d:%d}/{d:%m}/{d:%y} {d:%I}:{d:%M}:{d:%S} {d:%p}\t  ORDER: {order}")
                print()
                for i in range(len(list_belanja)):
                    print(f"\t{list_belanja[i]}\t| {rupiah_format(total_bayar[i])}")
                print()
                print(f"\tSUBTOTAL\t| {rupiah_format(raw_total)}")
                print(f"\tPPN 10%\t\t| {rupiah_format(tax)}")
                print(f"\tTOTAL\t\t| {rupiah_format(total)}")
        uang_bayar = int(input("\tUANG\t\t| Rp. "))
    kembali = rupiah_format(uang_bayar - total)
    if windows is False:
        delete_last_lines(1)
    else:
        clear()
        print("\t*===AVALON SPORTS===*\t")
        print()
        print(f"{d:%d}/{d:%m}/{d:%y} {d:%I}:{d:%M}:{d:%S} {d:%p}\t  ORDER: {order}")
        print()
        for i in range(len(list_belanja)):
            print(f"\t{list_belanja[i]}\t| {rupiah_format(total_bayar[i])}")
        print()
        print(f"\tSUBTOTAL\t| {rupiah_format(raw_total)}")
        print(f"\tPPN 10%\t\t| {rupiah_format(tax)}")
        print(f"\tTOTAL\t\t| {rupiah_format(total)}")
    print(f"\tUANG\t\t| {rupiah_format(uang_bayar)}")
    print(f"\tCHANGE\t\t| {kembali}")
    print()

    data = [raw_total, tax, total, uang_bayar, uang_bayar - total]

    ans = input("Cetak struk belanja? '[Y/N]': ")
    if ans.upper() == "Y":
        parse_data(d, no)
        parse_order(list_belanja, total_bayar, data)
        filename = cv()
        print("Struk belanja berhasil dicetak")
        if windows is False:
            cmd = f'xdg-open {filename}'
        else:
            cmd = f'start "Struk Belanja" {filename}'
        subprocess_run(cmd)
