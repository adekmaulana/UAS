### Project UAS

Tema: **Penjualan dan Pembelian**  

Program lanjutan mentah (tanpa GUI) untuk melakukan pembelian barang yang terhubung dengan database (PostgreSQL) server [heroku](https://heroku.com). Program ini membutuhkan koneksi internet, sebelum menjalankan program ini diwajibkan menginstall beberapa modul dan beberapa aksi pengguna.


### Inisialisasi

Dibutuhkan koneksi internet.

* Buka file `CodeNewRoman NF.otf` dan pilih install.
* Jalankan command ini di dalam root folder program `python -m pip install -r requirements.txt` dengan menggunakan terminal pada Linux atau command prompt pada Windows.

Dua langkah tersebut sangat dibutuhkan untuk kelancaran jalannya program dan kesempurnaan program.


### Running

`python -m avalon`


### Struktur

```
/project
├── CodeNewRoman NF.otf
├── output.png
├── requirements.txt
├── avalon
    ├── __init__.py
    └── __main__.py
    ├── helper
    │   ├── __init__.py
    │   └── manager.py
    └── tools
        └── __init__.py
        ├── data2docx.py
        ├── docx2pdf.py
        ├── pdf2png.py
        ├── receipt_linux.docx
        └── receipt_windows.docx
        ├── subprocess.py
```


### Output

<img src="https://raw.githubusercontent.com/adekmaulana/UAS/main/output.png" width="950px">
