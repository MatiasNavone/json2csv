# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [0.1.0] - 2026-10-08
### Agregado
- Conversión de JSON (objeto o lista de objetos) a CSV con estrategia de filtro.
- Argumentos `-i`, `-o` y `-d` (coma por defecto).
- Manejo controlado de errores (archivo inexistente, JSON inválido, codificación,
  salida no escribible, delimitador inválido).
- Tests con pytest (cobertura > 85 %), CI/CD en GitHub Actions y documentación con pdoc.
- Esqueleto de proyecto generado con CookieCutter (cookiecutter-pypackage).
