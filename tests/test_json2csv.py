"""Tests unitarios de json2csv."""

import argparse
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from json2csv import json2csv as j2c


def test_lista_de_objetos_a_csv():
    texto = json.dumps([{"a": 1, "b": "x"}, {"a": 2, "b": "y"}])
    assert j2c.convertir(texto) == "a,b\n1,x\n2,y\n"


def test_objeto_unico_es_una_fila():
    assert j2c.convertir('{"a": 1}') == "a\n1\n"


def test_columnas_son_la_union_de_claves_y_faltantes_quedan_vacios():
    texto = '[{"a": 1}, {"b": 2}]'
    assert j2c.convertir(texto) == "a,b\n1,\n,2\n"


def test_valores_anidados_nulos_y_booleanos():
    texto = '[{"a": null, "b": {"x": 1}, "c": [1, 2], "d": true}]'
    assert j2c.convertir(texto) == 'a,b,c,d\n,"{""x"": 1}","[1, 2]",true\n'


def test_delimitador_personalizado():
    assert j2c.convertir('[{"a": 1, "b": 2}]', ";") == "a;b\n1;2\n"


def test_lista_vacia_y_objeto_vacio_dan_salida_vacia():
    assert j2c.convertir("[]") == ""
    assert j2c.convertir("{}") == ""


@pytest.mark.parametrize("texto", ["", "{no es json", "42", '"hola"', "[1, 2]"])
def test_entradas_invalidas_lanzan_conversion_error(texto):
    with pytest.raises(j2c.ConversionError):
        j2c.convertir(texto)


@pytest.mark.parametrize("valor", ["", ";;", '"', "\n"])
def test_delimitador_invalido(valor):
    with pytest.raises(argparse.ArgumentTypeError):
        j2c.validar_delimitador(valor)


def test_main_con_archivos(tmp_path: Path):
    entrada = tmp_path / "in.txt"
    salida = tmp_path / "out.txt"
    entrada.write_text('[{"a": 1, "b": 2}]', encoding="utf-8")
    codigo = j2c.main(["-i", str(entrada), "-o", str(salida), "-d", "|"])
    assert codigo == 0
    assert salida.read_text(encoding="utf-8") == "a|b\n1|2\n"


def test_main_como_filtro_stdin_stdout(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO('[{"a": "ñ"}]'))
    assert j2c.main([]) == 0
    assert capsys.readouterr().out == "a\nñ\n"


def test_main_archivo_inexistente(tmp_path: Path, capsys):
    codigo = j2c.main(["-i", str(tmp_path / "no_existe.txt")])
    assert codigo == 1
    assert "Error:" in capsys.readouterr().err


def test_main_json_invalido(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("{roto"))
    assert j2c.main([]) == 1
    assert "JSON inválido" in capsys.readouterr().err


def test_main_entrada_no_utf8(tmp_path: Path, capsys):
    entrada = tmp_path / "latin.txt"
    entrada.write_bytes(b'[{"a": "\xe9"}]')
    assert j2c.main(["-i", str(entrada)]) == 1
    assert "UTF-8" in capsys.readouterr().err


def test_main_salida_no_escribible(tmp_path: Path, capsys):
    entrada = tmp_path / "in.txt"
    entrada.write_text("[]", encoding="utf-8")
    destino = tmp_path / "no_existe" / "out.txt"
    assert j2c.main(["-i", str(entrada), "-o", str(destino)]) == 1
    assert "no se pudo escribir" in capsys.readouterr().err


def test_main_delimitador_invalido_termina_con_codigo_2():
    with pytest.raises(SystemExit) as exc:
        j2c.main(["-d", ";;"])
    assert exc.value.code == 2


def test_ejecucion_como_modulo(tmp_path: Path):
    entrada = tmp_path / "in.txt"
    entrada.write_text('[{"a": 1}]', encoding="utf-8")
    resultado = subprocess.run(
        [sys.executable, "-m", "json2csv", "-i", str(entrada)],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"},
        check=False,
    )
    assert resultado.returncode == 0
    assert resultado.stdout == "a\n1\n"
