# json2csv

Herramienta de línea de comandos que convierte archivos **JSON a CSV** con
estrategia de **filtro** (lee de stdin y escribe en stdout por defecto).
Solo usa la biblioteca estándar de Python (>= 3.12).

## Uso

```
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

| Argumento | Descripción | Por defecto |
|---|---|---|
| `-i` | archivo JSON de entrada | entrada estándar |
| `-o` | archivo CSV de salida | salida estándar |
| `-d` | delimitador (un solo carácter) | coma `,` |

```
$ echo '[{"nombre":"Ana","edad":30},{"nombre":"Luis"}]' | python json2csv.py
nombre,edad
Ana,30
Luis,
```

Reglas de conversión: la entrada es un objeto o una lista de objetos; las
columnas son la unión de las claves (en orden de aparición); `null` queda
vacío y los valores anidados (objetos, listas) o booleanos se escriben como
JSON. Código de salida: `0` correcto, `1` error controlado (mensaje en
stderr), `2` argumentos inválidos.

## Desarrollo

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest                      # cobertura mínima 85 %
ruff check . && black --check src tests
pycodestyle --max-line-length=88 src tests
pydocstyle --convention=pep257 src
mypy && pyright && bandit -q -r src
PYTHONPATH=src pdoc json2csv -o docs/api   # documentación
```

El flujo de CI/CD está en `.github/workflows/ci.yml`. El esqueleto del
proyecto parte de [cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage).
Versión en `VERSION`, número de build en `BUILD` (lo escribe el workflow).

Licencia: MIT.
