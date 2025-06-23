import streamlit as st
import pandas as pd
import io
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Calculadora EPH Anual Separado", layout="wide")
st.title("📊 Calculadora EPH – Análisis Trimestral y Informe Anual")

st.markdown("Subí las **4 bases trimestrales de hogares e individuos** y el **instructivo en PDF**. La app analizará cada trimestre por separado y generará un informe anual integrado con las columnas principales.")

trimestres = [1, 2, 3, 4]
hogares_files = []
individuos_files = []

for t in trimestres:
    hogares_files.append(st.file_uploader(f"🏠 Base de Hogares T{t} (.xlsx)", type="xlsx", key=f"hog{t}"))
    individuos_files.append(st.file_uploader(f"👤 Base de Individuos T{t} (.xlsx)", type="xlsx", key=f"ind{t}"))

instructivo_pdf = st.file_uploader("📄 Instructivo PDF", type="pdf")

def extraer_diccionario_desde_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    doc.close()
    regex = re.compile(r"^(\w{2,})\s+[NC]\(\d+\)\s+(.+)$", re.MULTILINE)
    matches = regex.findall(text)
    return {codigo.strip(): desc.strip().capitalize() for codigo, desc in matches}

if all(hogares_files) and all(individuos_files) and instructivo_pdf:
    st.success("Todos los archivos fueron cargados correctamente ✅")

    mapa = extraer_diccionario_desde_pdf(instructivo_pdf)
    if not mapa:
        st.error("No se encontraron variables en el instructivo PDF.")
    else:
        resumenes_hogar = []
        resumenes_ind = []

        for i, t in enumerate(trimestres):
            df_hogar = pd.read_excel(hogares_files[i]).rename(columns=mapa)
            df_ind = pd.read_excel(individuos_files[i]).rename(columns=mapa)

            cols_hogar = [c for c in df_hogar.columns if any(x in c.lower() for x in ["ingreso", "región", "agua", "baño", "vivienda", "ipcf", "itf"])]
            cols_ind = [c for c in df_ind.columns if any(x in c.lower() for x in ["edad", "sexo", "educ", "actividad", "ingreso"])]

            resumen_hogar = df_hogar[cols_hogar].describe(include="all").transpose()
            resumen_ind = df_ind[cols_ind].describe(include="all").transpose()

            resumen_hogar["Trimestre"] = f"T{t}"
            resumen_ind["Trimestre"] = f"T{t}"

            resumenes_hogar.append(resumen_hogar)
            resumenes_ind.append(resumen_ind)

        resumen_anual_hogar = pd.concat(resumenes_hogar)
        resumen_anual_ind = pd.concat(resumenes_ind)

        st.subheader("📈 Informe Anual – Hogares")
        st.dataframe(resumen_anual_hogar)

        st.subheader("📈 Informe Anual – Individuos")
        st.dataframe(resumen_anual_ind)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            resumen_anual_hogar.to_excel(writer, sheet_name="Resumen Hogares")
            resumen_anual_ind.to_excel(writer, sheet_name="Resumen Individuos")
        output.seek(0)

        st.download_button(
            label="📥 Descargar informe anual en Excel",
            data=output,
            file_name="informe_anual_separado_eph.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("📥 Cargue las 4 bases trimestrales de hogares e individuos y el instructivo para comenzar.")
