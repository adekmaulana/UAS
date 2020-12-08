# https://github.com/AlJohri/docx2pdf
import sys
from pathlib import Path


def windows(paths, keep_active):
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    wdFormatPDF = 17
    docx_filepath = Path(paths["input"]).resolve()
    pdf_filepath = Path(paths["output"]).resolve()
    doc = word.Documents.Open(str(docx_filepath))
    doc.SaveAs(str(pdf_filepath), FileFormat=wdFormatPDF)
    doc.Close()

    if not keep_active:
        word.Quit()


def resolve_paths(input_path, output_path):
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve() if output_path else None
    output = {}
    if input_path.is_dir():
        output["batch"] = True
        output["input"] = str(input_path)
        if output_path:
            assert output_path.is_dir()
        else:
            output_path = str(input_path)
        output["output"] = output_path
    else:
        output["batch"] = False
        assert str(input_path).endswith(".docx")
        output["input"] = str(input_path)
        if output_path and output_path.is_dir():
            output_path = str(output_path / (str(input_path.stem) + ".pdf"))
        elif output_path:
            assert str(output_path).endswith(".pdf")
        else:
            output_path = str(input_path.parent / (str(input_path.stem) + ".pdf"))
        output["output"] = output_path
    return output


def convert(input_path, output_path=None, keep_active=False):
    paths = resolve_paths(input_path, output_path)
    if sys.platform == "win32":
        return windows(paths, keep_active)
    else:
        raise NotImplementedError(
            "docx2pdf is not implemented for linux as it requires Microsoft Word to be installed"
        )
