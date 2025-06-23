import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Calculadora EPH Avanzada", layout="wide")
st.title("📊 Calculadora de Análisis Cuantitativo EPH – INDEC")

st.markdown("Subí las bases de **hogares**, **individuos** y el **instructivo de variables**. La app renombrará las columnas automáticamente y generará análisis cuantitativos descargables.")

# Cargar archivos
hogares_file = st.file_uploader("📂 Base de Hogares (.xlsx)", type=["xlsx"])
individuos_file = st.file_uploader("📂 Base de Individuos (.xlsx)", type=["xlsx"])
instructivo_file = st.file_uploader("📄 Instructivo (.xlsx, .csv o .txt)", type=["xlsx", "csv", "txt"])

def procesar_instructivo(file):
    if file.name.endswith(".xlsx"):
        df_inst = pd.read_excel(file)
    elif file.name.endswith(".csv"):
        df_inst = pd.read_csv(file)
    elif file.name.endswith(".txt"):
        df_inst = pd.read_csv(file, delimiter="\t", header=None)
    else:
        return {}

    if df_inst.shape[1] < 2:
        st.error("⚠️ El instructivo debe tener al menos dos columnas: código y descripción.")
        return {}

    df_inst.columns = ["codigo", "descripcion"]
    return dict(zip(df_inst["codigo"].astype(str), df_inst["descripcion"].astype(str)))

# Renombrar y analizar
if hogares_file and individuos_file and instructivo_file:
    st.success("Archivos cargados correctamente ✅")

    # Cargar datos
    df_hogar = pd.read_excel(hogares_file)
    df_ind = pd.read_excel(individuos_file)
    mapa_variables = procesar_instructivo(instructivo_file)

    # Renombrar columnas si hay mapeo válido
    df_hogar = df_hogar.rename(columns=mapa_variables)
    df_ind = df_ind.rename(columns=mapa_variables)

    st.subheader("📈 Análisis descriptivo – Hogares")
    desc_hogar = df_hogar.describe(include='all').transpose()
    st.dataframe(desc_hogar)

    st.subheader("📈 Análisis descriptivo – Individuos")
    desc_ind = df_ind.describe(include='all').transpose()
    st.dataframe(desc_ind)

    # Descarga de resultados
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
    st.info("🔽 Cargue todos los archivos requeridos para comenzar el análisis.")
