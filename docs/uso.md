# Documentación básica de json2csv

Módulo `json2csv.json2csv`:

- `convertir(texto, delimitador=",")`: JSON (str) -> CSV (str).
- `main(argv=None)`: punto de entrada de la CLI; devuelve el código de salida.
- `ConversionError`: error controlado que `main` informa por stderr.

La referencia completa de la API se genera con pdoc en `docs/api/` y se
actualiza con cada PR exitoso (job `docs` del workflow).
