import datetime

from random import sample
from time import sleep
from typing import List
from avalon.helper.manager import get_item, update_item
from avalon.tools import rupiah_format, windows, delete_last_lines, clear, Lagi
from avalon.tools.subprocess import Command
from avalon.tools.data2docx import merge
from avalon.tools.pdf2png import run


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
    XXL = rupiah_format(get_harga('XXL'))
    XL = rupiah_format(get_harga('XL'))
    L = rupiah_format(get_harga('L'))
    M = rupiah_format(get_harga('M'))
    S = rupiah_format(get_harga('S'))
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
    print(f"|   • XXL ->  {XXL}                             |")
    print(f"|   • XL  ->  {XL}                             |")
    print(f"|   •  L  ->  {L}                             |")
    print(f"|   •  M  ->  {M}                             |")
    print(f"|   •  S  ->  {S}                             |")
    print("-------------------------------------------------------")


def main():
    jumlah_beli: int = 0
    list_boxer: List[str] = []
    list_harga: List[int] = []
    list_banyak: List[int] = []
    list_ukuran: List[str] = []

    while True:
        cetak_katalog()
        kode = input("Masukkan kode item '[PTH/HTM/AB2/NVY]': ")
        # Jika kode tidak terdaftar, ulang looping
        if kode.upper() not in ['PTH', 'HTM', 'AB2', 'NVY']:
            print("Kode tidak terdaftar!")
            sleep(2.5)
            clear()
            continue
        ukuran = input("Pilih ukuran '[XXL/XL/L/M/S]': ")
        harga = get_harga(ukuran.upper())
        # Jika ukuran tidak terdaftar, ulang looping
        if harga is None:
            print("Maaf ukuran belum ada...")
            sleep(2.5)
            clear()
            continue
        try:
            banyak_beli = int(input("Masukkan banyak beli: "))
        except ValueError:
            print("Maaf yang anda masukkan bukan angka")
            sleep(2.5)
            clear()
            continue
        # Initialized item dan check stock boxer pada database
        boxer = get_item(kode.upper())
        quantity = boxer.ukuran.get(ukuran.upper()).get('quantity')
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
        list_ukuran.append(ukuran.upper())
        jumlah_beli += 1
        # Kurangi stock pada database ketika logika di atas sudah terpenuhi
        update_item(boxer, ukuran.upper(), banyak_beli)
        print()
        lagi = None
        try:
            while lagi not in ['Y', 'N']:
                lagi = input("Tambah barang lagi? '[Y/N]': ")
                if lagi.upper() == "Y":
                    raise Lagi
                elif lagi.upper() == "N":
                    break
                else:
                    print('Jawaban anda di luar pertanyaan')
                    sleep(2.5)
                    clear()
                    continue
        except Lagi:
            # lagi = Y
            clear()
            continue
        else:
            # lagi = N
            break
    clear()
    d = datetime.datetime.now()
    no = sample(range(1, 100), 3)
    order = f"#AV{no[0]}{no[1]}{no[2]}"
    print("\t*===AVALON SPORTS===*\t")
    print()
    print(f"{d:%d}/{d:%m}/{d:%y} {d:%I}:{d:%M}:{d:%S} {d:%p}\t  ORDER: {order}")
    print()

    total_bayar: List[int] = []
    list_belanja: List[str] = []

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

    data: List[int, ...] = [raw_total, tax, total, uang_bayar, uang_bayar - total]

    ans = input("Cetak struk belanja? '[Y/N]': ")
    if ans.upper() == "Y":
        print()
        merge(d, no, list_belanja, total_bayar, data)
        filename = run()
        if windows is False:
            cmd = f'xdg-open {filename}'
        else:
            cmd = f'start "Struk Belanja" {filename}'
        command = Command(cmd)
        command.run()


if __name__ == '__main__':
    main()
