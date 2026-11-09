# SISVENTAS MiniTienda CUN 🛒

Sistema de gestión de ventas minoristas — ACA Final Calidad de Software.
Autora: **Laura Daniela Losada Ibata** · Programa Ingeniería de Sistemas, CUN Neiva.

## Contenido
- `minitienda.py` — sistema (auth, inventario, carrito, checkout con descuento de stock). 139 líneas, sin dependencias externas.
- `test_funcional.py` — prueba funcional PF-01 automatizada con pytest (7 tests).
- `gen_informe.py` — genera las 3 evidencias PNG + el informe Word APA.
- `evidencia_pytest.png` / `evidencia_cobertura.png` / `evidencia_sus.png` — evidencias de ejecución real.
- `INFORME_ACA_FINAL_Laura_Losada.docx` — informe final (2 pruebas + 3 métricas + análisis crítico + referencias APA 7).

## Requisitos
Python 3.14 + pytest + pytest-cov + matplotlib + python-docx.

## Cómo reproducir
```bash
python minitienda.py
pytest test_funcional.py -v
pytest --cov=minitienda --cov-report=term-missing test_funcional.py
python gen_informe.py
```

## Resultados
- Funcional PF-01: **7/7 en verde** (login + checkout, total real $28,900.00).
- Cobertura: **77%** (80/104 sentencias, pytest-cov).
- Usabilidad PU-01: **SUS 82.5** (n=5), éxito 93.3% (14/15).
- Métricas: M1 densidad 14.4 def/KLOC · M2 cobertura 77% · M3 SUS 82.5.

## Video pitch (máx. 5 min)
https://www.youtube.com/watch?v=88tNRIb2wW0
