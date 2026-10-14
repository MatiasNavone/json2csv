# CONTEXT.md — uso de herramientas de IA

Herramienta utilizada: Claude (Anthropic), en chat web. Los prompts se
transcriben tal como fueron escritos, en orden.

## Prompts utilizados

| # | Prompt (textual) | Adjuntos | Qué produjo la IA |
|---|---|---|---|
| 1 | "tengo que resolver el siguiente TP de ingenieria de software, que trata de gestion de calidad, dime que debo hacer en cada punto y si neceistas de algun material o algo que te pase, tengo una carpeta de soporte." | Enunciado del TP11 (PDF) | Guía por punto y lista del material de apoyo necesario |
| 2 | "te paso eseto que encontre" | Taller_Defectos.ipynb, guía de Kanban, artículos "Agile and software engineering" y "Marco para evaluar garantía", presentaciones de clase | Lectura del material y resumen de qué aporta a cada punto |
| 3 | "dale arranquemos con eso" | — | Borrador de requerimientos R y F de Collatz |
| 4 | "Te lo copie, esta bien? dea" | Captura de la tabla | Revisión de la tabla de requerimientos |
| 5 | "haceme todo vos" | — | Test cases, RTMX, sesiones de test ejecutadas, métricas, herramienta json2csv, proyecto con CI/CD y documento de resolución |
| 6 | "viste que tp tinee punto por punto, no esta numeado, dame la consigna tal cual y que va abajo, si no va nada decimelo y no le pongo nada" | — | Mapeo de las consignas del PDF con su contenido |
| 7 | "armame vos el traabajo asi como te dije" | — | Reorganización del documento por consigna |
| 8 | "Dame el paso a paso para este punto del trabajo" (con el texto de las consignas de json2csv y CI) | — | Guía de ejecución del proyecto y de la subida a GitHub |

Además hice consultas puntuales para resolver errores de ejecución en
PowerShell (rutas, sintaxis de variables de entorno y codificación de archivos).

## Alcance de la IA en este proyecto

- Generó el esqueleto con CookieCutter (cookiecutter-pypackage), el código de
  `json2csv`, los tests, el workflow de GitHub Actions y la documentación.
- Ejecutó localmente cada herramienta de calidad (ruff, black, pycodestyle,
  pydocstyle, mypy, pyright, bandit, pytest con cobertura).
- Yo verifiqué el resultado en mi máquina (Windows, Python 3.12.6):
  ruff, black, PEP8, PEP257, mypy, pyright y bandit sin errores, y pytest con
  23 tests aprobados y 93 % de cobertura.
