import os
import sys
import locale

from shutil import get_terminal_size
from contextlib import contextmanager

windows = False
if os.name == 'nt':
    windows = True


class Lagi(Exception):
    pass


def clear():
    print("\n" * get_terminal_size().lines, end='')


def delete_last_lines(n=1):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.flush()


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
