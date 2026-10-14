"""Permite ejecutar el paquete con ``python -m json2csv``."""

import sys

from .json2csv import main

if __name__ == "__main__":
    sys.exit(main())
