import streamlit as st
import pandas as pd
import io
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Calculadora EPH Anual Simple", layout="wide")
st.title("📊 Calculadora EPH – Análisis Anual por Base")

st.markdown("Subí una base de **hogares** y una base de **individuos** del año completo (consolidada o combinada), junto con el **instructivo en PDF**. La app generará un informe anual integrado con las variables principales.")

hogares_file = st.file_uploader("🏠 Base de Hogares anual (.xlsx)", type="xlsx")
individuos_file = st.file_uploader("👤 Base de Individuos anual (.xlsx)", type="xlsx")
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

if hogares_file and individuos_file and instructivo_pdf:
    st.success("Todos los archivos fueron cargados correctamente ✅")

    mapa = extraer_diccionario_desde_pdf(instructivo_pdf)
    if not mapa:
        st.error("No se encontraron variables en el instructivo PDF.")
    else:
        df_hogar = pd.read_excel(hogares_file).rename(columns=mapa)
        df_ind = pd.read_excel(individuos_file).rename(columns=mapa)

        cols_hogar = [c for c in df_hogar.columns if any(x in c.lower() for x in ["ingreso", "región", "agua", "baño", "vivienda", "ipcf", "itf"])]
        cols_ind = [c for c in df_ind.columns if any(x in c.lower() for x in ["edad", "sexo", "educ", "actividad", "ingreso"])]

        resumen_hogar = df_hogar[cols_hogar].describe(include="all").transpose()
        resumen_ind = df_ind[cols_ind].describe(include="all").transpose()

        st.subheader("📈 Informe Anual – Hogares")
        st.dataframe(resumen_hogar)

        st.subheader("📈 Informe Anual – Individuos")
        st.dataframe(resumen_ind)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            resumen_hogar.to_excel(writer, sheet_name="Resumen Hogares")
            resumen_ind.to_excel(writer, sheet_name="Resumen Individuos")
        output.seek(0)

        st.download_button(
            label="📥 Descargar informe anual en Excel",
            data=output,
            file_name="informe_anual_simple_eph.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("📥 Cargue la base de hogares, individuos y el instructivo para comenzar.")
