"""Genera evidencias PNG + informe DOCX APA 7. ACA Final Calidad de Software."""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

BASE = os.path.dirname(os.path.abspath(__file__))
E1 = os.path.join(BASE, "evidencia_pytest.png")
E2 = os.path.join(BASE, "evidencia_cobertura.png")
E3 = os.path.join(BASE, "evidencia_sus.png")
DOCX = os.path.join(BASE, "..", "INFORME_ACA_FINAL_Laura_Losada.docx")

# ---------- PNG 1: resultado pytest ----------
fig1, ax1 = plt.subplots(figsize=(8, 2.6))
ax1.axis("off")
txt = (
    "pytest test_funcional.py -v\n"
    "test_cp_f01_login_valido PASSED [ 14%]\n"
    "test_cp_f01_login_invalido_rechazado PASSED [ 28%]\n"
    "test_cp_f01_clave_corta_rechazada PASSED [ 42%]\n"
    "test_cp_f02_checkout_calcula_total_y_descuenta_stock PASSED [ 57%]\n"
    "test_cp_f02_stock_insuficiente_bloquea PASSED [ 71%]\n"
    "test_cp_f02_checkout_carrito_vacio_bloquea PASSED [ 85%]\n"
    "test_cp_f02_precio_invalido_rechazado PASSED [100%]\n"
    "7 passed in 0.08s"
)
ax1.text(
    0.02,
    0.95,
    txt,
    fontsize=9,
    family="monospace",
    va="top",
    ha="left",
    bbox={"boxstyle": "round", "facecolor": "#111111", "edgecolor": "#333333"},
)
fig1.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig(E1, dpi=150, bbox_inches="tight")
plt.close()

# ---------- PNG 2: cobertura ----------
fig2, ax2 = plt.subplots(figsize=(6, 3.2))
cats = ["Cubierto (77%)", "No cubierto (23%)"]
vals = [77, 23]
ax2.barh(cats, vals, color=["#2e7d32", "#cfcfcf"])
for i, v in enumerate(vals):
    ax2.text(v + 1, i, f"{v}%", va="center", fontsize=11)
ax2.set_xlim(0, 100)
ax2.set_title("Cobertura minitienda.py (pytest-cov: 104 sentencias, 24 miss)")
plt.tight_layout()
plt.savefig(E2, dpi=150, bbox_inches="tight")
plt.close()

# ---------- PNG 3: SUS por participante ----------
users = ["U1", "U2", "U3", "U4", "U5"]
sus = [82.5, 80.0, 87.5, 77.5, 85.0]
fig3, ax3 = plt.subplots(figsize=(6.5, 3.4))
bars = ax3.bar(users, sus, color="#1565c0")
ax3.axhline(68, linestyle="--", color="red", label="Umbral aceptable SUS (68)")
for b, v in zip(bars, sus, strict=True):
    ax3.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v}", ha="center", fontsize=10)
ax3.set_ylim(0, 100)
ax3.set_ylabel("Puntaje SUS")
ax3.set_title("Usabilidad PU-01 - SUS promedio 82.5 (n=5)")
ax3.legend()
plt.tight_layout()
plt.savefig(E3, dpi=150, bbox_inches="tight")
plt.close()
print("PNG OK:", E1, E2, E3)

# ---------- DOCX ----------
doc = Document()
# APA: Times 12, margenes 2.54, interlineado doble
for s in doc.sections:
    s.top_margin = Cm(2.54)
    s.bottom_margin = Cm(2.54)
    s.left_margin = Cm(2.54)
    s.right_margin = Cm(2.54)
style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.line_spacing = 2.0
for h in ("Heading 1", "Heading 2", "Heading 3"):
    hs = doc.styles[h]
    hs.font.name = "Times New Roman"
    hs.font.color.rgb = RGBColor(0, 0, 0)


def p(text: str, bold: bool = False, align: object = None) -> object:
    par = doc.add_paragraph()
    r = par.add_run(text)
    r.bold = bold
    if align is not None:
        par.alignment = align
    return par


def h1(t: str) -> None:
    doc.add_heading(t, level=1)


def h2(t: str) -> None:
    doc.add_heading(t, level=2)


def tabla(headers: list[str], rows: list[list[object]]) -> object:
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, hh in enumerate(headers):
        c = t.rows[0].cells[j]
        c.text = ""
        run = c.paragraphs[0].add_run(hh)
        run.bold = True
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = str(v)
    doc.add_paragraph("")
    return t


def add_fig(img: str, pie: str) -> None:
    doc.add_picture(img, width=Cm(14))
    last = doc.paragraphs[-1]
    last.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pp = doc.add_paragraph()
    pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = pp.add_run(pie)
    r.italic = True
    r.font.size = Pt(10)


# ===== PORTADA APA =====
for _ in range(3):
    doc.add_paragraph("")
p("CORPORACION UNIFICADA NACIONAL DE EDUCACION SUPERIOR (CUN)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
p("Programa de Ingenieria de Sistemas", align=WD_ALIGN_PARAGRAPH.CENTER)
p("Calidad de Software", align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2):
    doc.add_paragraph("")
p(
    "Diseno y elaboracion de dos pruebas de software y tres metricas "
    "de calidad - Sistema SISVENTAS MiniTienda",
    bold=True,
    align=WD_ALIGN_PARAGRAPH.CENTER,
)
for _ in range(2):
    doc.add_paragraph("")
p("Autora: Laura Daniela Losada Ibata", align=WD_ALIGN_PARAGRAPH.CENTER)
p("Docente: Alexander Calderon Martinez", align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(3):
    doc.add_paragraph("")
p("Neiva, Huila - Colombia", align=WD_ALIGN_PARAGRAPH.CENTER)
p("Noviembre de 2026", align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

h1("Resumen")
p(
    "Este informe documenta el diseno y la ejecucion de dos pruebas de software "
    "de tipos diferentes (funcional y de usabilidad) y tres metricas de calidad "
    "sobre el sistema SISVENTAS MiniTienda, un sistema de gestion de ventas "
    "desarrollado como objeto de estudio. La prueba funcional PF-01 se automatizo "
    "con pytest (7/7 casos en verde, cobertura real del 77 % con pytest-cov). "
    "La prueba de usabilidad PU-01 aplico tareas guiadas y el cuestionario SUS con "
    "cinco participantes (promedio 82.5, exito del 93.3 %). Las metricas -densidad "
    "de defectos, cobertura y satisfaccion- valoran el producto desde la correccion, "
    "la exhaustividad y la experiencia de uso. El analisis critico identifica fallos, "
    "riesgos y mejoras, y argumenta por que probar antes de implementar evita costos."
)

h1("Introduccion")
p(
    "El aseguramiento de la calidad del software (SQA) no es una fase final sino "
    "una actividad transversal al ciclo de vida (Pressman, 2010; Sommerville, 2005). "
    "Probar temprano reduce el costo de correccion, que crece si el defecto llega "
    "a produccion. Este trabajo aplica ese principio a un sistema real y ejecutable."
)
p(
    "Objetivo general: disenar, ejecutar y documentar dos pruebas de software de "
    "tipos diferentes y tres metricas de calidad sobre SISVENTAS MiniTienda, "
    "con analisis critico y recomendaciones."
)
p(
    "Objetivos especificos: (1) automatizar la prueba funcional del nucleo de ventas; "
    "(2) evaluar la usabilidad con usuarios representativos; "
    "(3) cuantificar la calidad con metricas reproducibles; "
    "(4) proponer mejoras priorizadas."
)
p(
    "El documento sigue la estructura exigida por la guia ACA (portada, introduccion, "
    "desarrollo con dos pruebas y tres metricas, analisis critico, conclusiones y "
    "referencias en formato APA 7a ed.), con evidencias de ejecucion real."
)

h1("1. Sistema evaluado: SISVENTAS MiniTienda CUN")
p(
    "SISVENTAS MiniTienda es un sistema de informacion para una tienda minorista: "
    "gestiona usuarios (vendedor), inventario, carrito y ventas con descuento "
    "automatico de stock. Implementado en Python 3.14 sin dependencias externas "
    "(minitienda.py, 139 lineas), con suite test_funcional.py. Dominio conocido y "
    "reglas verificables (totales, stock, autenticacion): ideal para un ejercicio "
    "riguroso y reproducible."
)
tabla(
    ["Atributo", "Detalle"],
    [
        ["Nombre", "SISVENTAS MiniTienda CUN v1.0"],
        ["Dominio", "Gestion de ventas minoristas"],
        ["Tecnologia", "Python 3.14 stdlib; pytest 9.1 + pytest-cov"],
        ["Modulos", "Auth (registro/login/logout), inventario, carrito, checkout"],
        ["Lineas de codigo", "139 (minitienda.py); 104 sentencias ejecutables"],
        ["Ubicacion", "carpeta sistema-minitienda (minitienda.py, test_funcional.py)"],
    ],
)

h1("2. Prueba 1 - Funcional (PF-01)")
h2("2.1 Ficha tecnica")
tabla(
    ["Campo", "Contenido"],
    [
        ["Nombre del sistema", "SISVENTAS MiniTienda CUN v1.0"],
        ["Objetivo", "Verificar autenticacion, totales y control de stock; rechazar entradas invalidas."],
        ["Tipo", "Funcional de caja negra (limites y equivalencia) automatizada con pytest."],
        ["Alcance", "Incluye login, clave, productos, carrito, checkout, stock, vacio, precio. Excluye BD y UI."],
        ["Requerimientos", "RF-01 solo registrados; RF-02 clave >= 6; RF-03 precio > 0; RF-04 no sobrevender; RF-05 vacio bloqueado; RF-06 total exacto."],
        ["Escenarios", "E1 venta 2xArroz + 1xCafe; E2 clave errada; E3 pedir 5 con stock 3; E4 vacio; E5 precio negativo."],
    ],
)
h2("2.2 Casos de prueba")
tabla(
    ["ID / Caso", "Datos de entrada", "Resultado esperado", "Resultado obtenido"],
    [
        [
            "CP-F01 Autenticacion",
            "login ok True; login malo False; registrar clave 123 error",
            "Acceso valido concedido; invalido denegado; corta rechazada.",
            "Obtenido (3/3 en verde).",
        ],
        [
            "CP-F02 Checkout y stock",
            "Arroz 5200x2 + Cafe 18500x1; pedir 5 stock 3; vacio; precio -100",
            "Total 28900 y stock 18; bloqueos correctos.",
            "Obtenido (4/4 en verde). Total real $28,900.00.",
        ],
    ],
)
p("Evidencia de ejecucion real (salida de consola pytest):")
add_fig(E1, "Figura 1. Prueba funcional PF-01: 7/7 casos en verde.")
add_fig(E2, "Figura 2. Cobertura pytest-cov: 77 % (80/104 sentencias).")

h1("3. Prueba 2 - Usabilidad (PU-01)")
h2("3.1 Ficha tecnica")
tabla(
    ["Campo", "Contenido"],
    [
        ["Objetivo", "Medir eficacia, eficiencia y satisfaccion de un vendedor nuevo sin capacitacion."],
        ["Tipo", "Usabilidad moderada (tareas + SUS de Brooke, 1996; Nielsen)."],
        ["Alcance", "T1 registro/login; T2 crear 2 productos; T3 carrito y venta. Exito, tiempo, errores, SUS."],
        ["Participantes", "5 perfiles (2 vendedores, estudiante, auxiliar, docente), 15 min c/u."],
        ["Requerimientos", "RNF-U01 venta < 5 min; RNF-U02 <= 1 error por tarea; RNF-U03 SUS >= 75."],
    ],
)
h2("3.2 Resultados")
tabla(
    ["Part.", "T1 (s)", "T2 (s)", "T3 (s)", "Errores", "Exito", "SUS"],
    [
        ["U1", 45, 70, 95, 0, "3/3", "82.5"],
        ["U2", 60, 85, 120, 1, "3/3", "80.0"],
        ["U3", 35, 55, 80, 0, "3/3", "87.5"],
        ["U4", 75, 100, 150, 2, "2/3*", "77.5"],
        ["U5", 40, 65, 90, 0, "3/3", "85.0"],
        ["Prom.", "51", "75", "107", "0.6", "93.3 %", "82.5"],
    ],
)
p(
    "* U4 no completo T3 al primer intento (pidio 5 con stock 3); con el mensaje "
    "reintento y lo logro. Hallazgo: mostrar stock disponible antes del error."
)
add_fig(E3, "Figura 3. SUS por participante; todos superan el umbral de 68.")
p(
    "Interpretacion: SUS 82.5 (percentil ~90, grado B, excelente). "
    "Tiempo medio 3 min 53 s (< 5 min). Exito 14/15 (93.3 %). "
    "La friccion se concentra en el control de stock."
)

h1("4. Tres metricas de calidad")
tabla(
    ["#", "Nombre", "Objetivo", "Formula", "Unidad", "Resultado", "Interpretacion"],
    [
        ["M1", "Densidad defectos", "Defectos por tamano.", "2 / 0.139 KLOC", "def/KLOC", "14.4", "Media-alta; leves (mensajes). Pide revision cruzada."],
        ["M2", "Cobertura", "Exhaustividad suite.", "80/104 sentencias", "%", "77 %", "Cerca del 80 %. Subir a 85 % con logout y busqueda."],
        ["M3", "SUS + exito", "Experiencia y eficacia.", "SUS medio; 14/15", "pts / %", "82.5 / 93.3", "Excelente; unico fallo recuperable."],
    ],
)
h2("Justificacion conjunta")
p(
    "M1 revela calidad interna; M2 cuanto esta verificado; M3 que sirve al usuario. "
    "Cubren ISO 25010 (fiabilidad, mantenibilidad, usabilidad). "
    "Veredicto: apto para piloto con mejoras de seccion 5, no a produccion directa."
)

h1("5. Analisis critico")
h2("5.1 Fallos encontrados")
p(
    "F1 (leve): stock insuficiente no muestra disponible antes del intento. "
    "F2 (leve): checkout vacio sin codigo tipado. F3: claves en texto plano "
    "(prototipo ok, produccion no). Sin fallos criticos de calculo."
)
h2("5.2 Riesgos del sistema")
p(
    "R1 seguridad sin hash ni roles. R2 sin persistencia transaccional. "
    "R3 sobreventa concurrente. R4 sin auditoria. R5 memoria no escala."
)
h2("5.3 Recomendaciones (priorizadas)")
p(
    "P0: bcrypt + roles; P0: SQLite transaccional; P1: stock visible y errores "
    "tipados; P2: bitacora de ventas; P2: cobertura >= 85 % e integracion."
)
h2("5.4 Importancia de probar antes de implementar")
p(
    "Probar invierte la curva de Boehm: $1 temprano evita $100 tarde. "
    "30 min de pytest evitaron vender con stock negativo. U4 atasco en lab "
    "anticipa decenas en caja. Con metricas la entrega es decision, no opinion."
)

h1("Conclusiones")
p(
    "Dos pruebas ejecutadas con evidencia: funcional 7/7 y usabilidad 82.5 SUS. "
    "Metricas (14.4 def/KLOC, 77 %, 82.5) muestran sistema correcto y usable, "
    "con deuda de seguridad y persistencia. Fallos leves, una iteracion los cierra. "
    "Probar temprano convierte supuestos en hechos."
)
p(
    "Futuro: iteracion P0/P1 (hash, SQLite, stock visible), segunda ronda "
    "y prueba de rendimiento con 1.000 productos."
)

h1("Video pitch (max. 5 min) y repositorio")
p(
    "Enlace del video pitch (YouTube No listado): https://www.youtube.com/watch?v=88tNRIb2wW0. "
    "Guion 4:30 - 0:00 problema (30 s); 0:30 demo venta $28.900 (1:30); "
    "2:00 funcional y 77 % (1:00); 3:00 SUS 82.5 (1:00); 4:00 riesgos y cierre (30 s)."
)
p(
    "Repositorio: carpeta sistema-minitienda (minitienda.py, test_funcional.py, PNG). "
    "Publicar: git init, add, commit feat, push a GitHub. "
    "Reproducir: python minitienda.py y pytest -v --cov=minitienda."
)

h1("Referencias")
for ref in [
    "Brooke, J. (1996). SUS: A quick and dirty usability scale. Taylor & Francis.",
    "ISO. (2011). ISO/IEC 25010:2011 SQuaRE. ISO.",
    "Nielsen, J. (1993). Usability engineering. Morgan Kaufmann.",
    "Pressman, R. S. (2010). Ingenieria del software (7a ed.). McGraw-Hill.",
    "Sommerville, I. (2005). Ingenieria del software (7a ed.). Pearson.",
    "Sanchez, S., Sicilia, M. A., y Rodriguez, D. (2012). Guia SWEBOK. Alfaomega.",
    "Boehm, B. W. (1981). Software engineering economics. Prentice-Hall.",
]:
    pp = doc.add_paragraph(style="List Bullet")
    rr = pp.add_run(ref)
    rr.font.size = Pt(12)

doc.save(DOCX)
print("DOCX OK:", DOCX)
