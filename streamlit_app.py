import streamlit as st
import pandas as pd
import io
import fitz  # PyMuPDF

st.set_page_config(page_title="Calculadora EPH Avanzada", layout="wide")
st.title("📊 Calculadora EPH con Instructivo PDF")

st.markdown("Subí las bases de **hogares**, **individuos** y el **instructivo en PDF**. La app extraerá automáticamente los nombres descriptivos de las variables y generará análisis descargables.")

# Cargar archivos
hogares_file = st.file_uploader("📂 Base de Hogares (.xlsx)", type=["xlsx"])
individuos_file = st.file_uploader("📂 Base de Individuos (.xlsx)", type=["xlsx"])
instructivo_pdf = st.file_uploader("📄 Instructivo PDF", type=["pdf"])

def extraer_diccionario_desde_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    doc.close()

    # Extraer líneas con formato CÓDIGO TIPO(DESCRIPCIÓN)
    import re
    regex = re.compile(r"^(\w{2,})\s+[NC]\(\d+\)\s+(.+)$", re.MULTILINE)
    matches = regex.findall(text)
    return {codigo.strip(): desc.strip().capitalize() for codigo, desc in matches}

if hogares_file and individuos_file and instructivo_pdf:
    st.success("Archivos cargados correctamente ✅")

    df_hogar = pd.read_excel(hogares_file)
    df_ind = pd.read_excel(individuos_file)

    # Procesar instructivo PDF
    mapa_variables = extraer_diccionario_desde_pdf(instructivo_pdf)

    if not mapa_variables:
        st.error("❌ No se encontraron variables en el instructivo PDF.")
    else:
        # Renombrar columnas
        df_hogar = df_hogar.rename(columns=mapa_variables)
        df_ind = df_ind.rename(columns=mapa_variables)

        st.subheader("📈 Análisis descriptivo – Hogares")
        desc_hogar = df_hogar.describe(include='all').transpose()
        st.dataframe(desc_hogar)

        st.subheader("📈 Análisis descriptivo – Individuos")
        desc_ind = df_ind.describe(include='all').transpose()
        st.dataframe(desc_ind)

        # Excel de salida
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            desc_hogar.to_excel(writer, sheet_name="Hogares")
            desc_ind.to_excel(writer, sheet_name="Individuos")
        output.seek(0)

        st.download_button(
            label="📥 Descargar análisis en Excel",
            data=output,
            file_name="analisis_eph_renombrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("🔽 Cargue todos los archivos para comenzar el análisis.")
