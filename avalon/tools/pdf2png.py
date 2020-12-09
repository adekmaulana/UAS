import os
import cloudconvert
import typing
import pathlib

from alive_progress import alive_bar
from avalon.tools import windows, suppress_stdout
from avalon.tools.docx2pdf import convert
from avalon.tools.subprocess import Command


def run() -> typing.Union[str, pathlib.Path]:
    tasks = {
        "tasks": {
            "upload-file": {
                "operation": "import/upload"
            },
            "convert-file-png": {
                "operation": "convert",
                "input": "upload-file",
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

    tools = 'avalon/tools'

    with alive_bar(6, title='Mencetak', spinner='classic') as bar:

        # convert ke PDF
        if windows is True:
            convert(f'{tools}/temp.docx')
        else:
            command = Command(f'unoconv -f pdf {tools}/temp.docx')
            command.run()
        bar()  # 1

        # Initialized API_KEY
        cloudconvert.configure(api_key=API_KEY)

        # Buat job pada server
        job = cloudconvert.Job.create(payload=tasks)
        bar()  # 2

        # Upload file ke server
        upload_task_id = job['tasks'][0]['id']
        upload_task = cloudconvert.Task.find(id=upload_task_id)
        res = cloudconvert.Task.upload(file_name=f'{tools}/temp.pdf', task=upload_task)
        bar()  # 3

        # mulai convert pada server
        convert_task_id = job['tasks'][1]['id']
        res = cloudconvert.Task.wait(id=convert_task_id)  # pdf to png
        bar()  # 4

        # download converted file di server ke local
        download_task_id = job['tasks'][2]['id']
        res = cloudconvert.Task.wait(id=download_task_id)
        files = res.get("result").get("files")[0]
        bar()  # 5

        if os.path.exists(f"{tools}/{files['filename']}"):
            os.remove(f"{tools}/{files['filename']}")

        with suppress_stdout():
            res = cloudconvert.download(
                filename=f"{tools}/{files['filename']}", url=files['url'])
        bar()  # 6

        os.remove(f'{tools}/temp.docx')
        os.remove(f'{tools}/temp.pdf')

    return f"{tools}/{files['filename']}"
