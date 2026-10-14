"""Convierte JSON a CSV con estrategia de filtro (stdin -> stdout).

Uso::

    python json2csv.py [-i input.txt] [-o output.txt] [-d delimitador]

Si no se indica ``-i`` se lee de la entrada estándar y si no se indica ``-o``
se escribe en la salida estándar. El delimitador por defecto es la coma.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections.abc import Sequence
from typing import Any, cast

DELIMITADOR_DEFECTO = ","


class ConversionError(Exception):
    """Error controlado durante la lectura, conversión o escritura."""


def validar_delimitador(valor: str) -> str:
    """Valida que el delimitador sea un único carácter utilizable en CSV."""
    if len(valor) != 1 or valor in {'"', "\n", "\r"}:
        raise argparse.ArgumentTypeError(
            "el delimitador debe ser un único carácter distinto de comilla "
            "doble y de salto de línea"
        )
    return valor


def cargar_registros(texto: str) -> list[dict[str, Any]]:
    """Interpreta ``texto`` como un objeto JSON o una lista de objetos."""
    try:
        datos: object = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ConversionError(f"JSON inválido: {exc}") from exc
    if isinstance(datos, dict):
        elementos: list[object] = [cast("dict[str, Any]", datos)]
    elif isinstance(datos, list):
        elementos = cast("list[object]", datos)
    else:
        raise ConversionError("se espera un objeto JSON o una lista de objetos")
    registros: list[dict[str, Any]] = []
    for elemento in elementos:
        if not isinstance(elemento, dict):
            raise ConversionError("se espera un objeto JSON o una lista de objetos")
        registros.append(cast("dict[str, Any]", elemento))
    return registros


def _celda(valor: Any) -> str:
    """Convierte un valor JSON en el texto de una celda CSV."""
    if valor is None:
        return ""
    if isinstance(valor, str):
        return valor
    return json.dumps(valor, ensure_ascii=False)


def convertir(texto: str, delimitador: str = DELIMITADOR_DEFECTO) -> str:
    """Convierte un texto JSON en texto CSV (encabezado + una fila por objeto)."""
    registros = cargar_registros(texto)
    columnas = list(dict.fromkeys(clave for r in registros for clave in r))
    salida = io.StringIO()
    if columnas:
        escritor = csv.writer(salida, delimiter=delimitador, lineterminator="\n")
        escritor.writerow(columnas)
        for registro in registros:
            escritor.writerow([_celda(registro.get(c)) for c in columnas])
    return salida.getvalue()


def leer_entrada(ruta: str | None) -> str:
    """Lee el JSON desde ``ruta`` o, si es ``None``, desde la entrada estándar."""
    try:
        if ruta is None:
            return sys.stdin.read()
        with open(ruta, encoding="utf-8") as archivo:
            return archivo.read()
    except UnicodeDecodeError as exc:
        raise ConversionError(f"la entrada no está codificada en UTF-8: {exc}") from exc
    except OSError as exc:
        raise ConversionError(f"no se pudo leer la entrada: {exc}") from exc


def escribir_salida(texto: str, ruta: str | None) -> None:
    """Escribe el CSV en ``ruta`` o, si es ``None``, en la salida estándar."""
    try:
        if ruta is None:
            sys.stdout.write(texto)
            sys.stdout.flush()
        else:
            with open(ruta, "w", encoding="utf-8", newline="") as archivo:
                archivo.write(texto)
    except OSError as exc:
        raise ConversionError(f"no se pudo escribir la salida: {exc}") from exc


def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="json2csv.py", description="Convierte un archivo JSON en CSV."
    )
    parser.add_argument("-i", dest="entrada", help="archivo JSON (por defecto stdin)")
    parser.add_argument("-o", dest="salida", help="archivo CSV (por defecto stdout)")
    parser.add_argument(
        "-d",
        dest="delimitador",
        type=validar_delimitador,
        default=DELIMITADOR_DEFECTO,
        help="delimitador de campos (por defecto coma)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada: devuelve 0 si todo salió bien y 1 ante un error."""
    args = crear_parser().parse_args(argv)
    try:
        texto = leer_entrada(args.entrada)
        escribir_salida(convertir(texto, args.delimitador), args.salida)
    except ConversionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
