import os
import sys
import datetime
import cloudconvert
import locale

from contextlib import contextmanager
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE


def rupiah_format(angka, with_prefix=True, desimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'id_ID.UTF-8')
    rupiah = locale.format_string("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah


@contextmanager
def suppress_stdout():
    """ Didapat dari https://stackoverflow.com/a/60327812 """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def convert() -> None:
    tasks = {
        "tasks": {
            "upload-file": {
                "operation": "import/upload"
            },
            "convert-file-pdf": {
                "operation": "convert",
                "input": "upload-file",
                "input_format": "docx",
                "output_format": "pdf",
                "engine": "office",
                "engine_version": "2019",
                "filename": "temp.pdf",
                "optimize_print": True
            },
            "convert-file-png": {
                "operation": "convert",
                "input": "convert-file-pdf",
                "input_format": "pdf",
                "output_format": "png",
                "engine": "poppler",
                "engine_version": "0.71.0",
                "filename": "receipt.png"
            },
            "download-converted-file": {
                "operation": "export/url",
                "input": "convert-file-png"
            }
        }
    }

    # Initialized API_KEY
    cloudconvert.configure(api_key=API_KEY)

    # Buat job pada server
    job = cloudconvert.Job.create(payload=tasks)

    # Upload file ke server
    upload_task_id = job['tasks'][0]['id']
    upload_task = cloudconvert.Task.find(id=upload_task_id)
    res = cloudconvert.Task.upload(file_name='temp.docx', task=upload_task)

    # mulai convert pada server
    convert_task_id = [job['tasks'][1]['id'], job['tasks'][2]['id']]
    res = cloudconvert.Task.wait(id=convert_task_id[0])  # docx to pdf
    res = cloudconvert.Task.wait(id=convert_task_id[1])  # pdf to png

    # download converted file di server ke local
    download_task_id = job['tasks'][3]['id']
    res = cloudconvert.Task.wait(id=download_task_id)
    files = res.get("result").get("files")[0]
    with suppress_stdout():
        res = cloudconvert.download(
            filename=files['filename'], url=files['url'])

    os.remove('temp.docx')


def parse_data(d: datetime.datetime, no: list) -> None:
    order = f"#AV{no[0]}{no[1]}{no[2]}"
    cells_text = [
        f"{d:%d}/{d:%m}/{d:%y} {d:%-I}:{d:%M}:{d:%S} {d:%p}",
        f"{order}"
    ]
    document = Document('receipt.docx')
    table = document.tables[1].rows[0]

    # styles = document.styles
    # style = styles.add_style('Abadi MT Std', WD_STYLE_TYPE.PARAGRAPH)
    # style.font.name = 'Abadi MT Std'
    for index, cell in enumerate(table.cells):
        paragraphs = cell.paragraphs
        for paragraph in paragraphs:
            run = paragraph.add_run()
            font = run.font
            font.name = 'Abadi MT Std'
            font.size = Pt(12)
            font.bold = True
            run.text = cells_text[index]
    return document.save('temp.docx')


def parse_order(list_belanja: list, total_bayar: list, data: list) -> None:
    TEXT = ["SUBTOTAL", "PPN 10%", "TOTAL", "UANG", "CHANGE"]

    document = Document('temp.docx')
    table = document.tables[2]

    total = len(list_belanja) + 5
    for row in range(total):
        table.add_row()
    rows = table.rows

    # Tulis belanjaan pada struk belanja
    for index, belanja in enumerate(list_belanja):
        for i, cell in enumerate(rows[index].cells):
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                run = paragraph.add_run()
                font = run.font
                font.name = 'Abadi MT Std'
                font.size = Pt(12)
                font.bold = True
                if i == 0:
                    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    run.text = list_belanja[index]
                elif i == 1:
                    run.text = rupiah_format(total_bayar[index])

    # Tulis SUBTOTAL, PPN, TOTAL, UANG, CHANGE/KEMBALIAN
    i = len(list_belanja) + 1
    while i <= total:
        for index, cell in enumerate(rows[i].cells):
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                run = paragraph.add_run()
                font = run.font
                font.name = 'Abadi MT Std'
                font.size = Pt(12)
                font.bold = True
                if index == 0:
                    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    run.text = TEXT[i - 4]
                elif index == 1:
                    run.text = rupiah_format(data[i - 4])
        i += 1

    return document.save('temp.docx')
