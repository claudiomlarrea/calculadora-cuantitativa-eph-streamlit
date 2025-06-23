# 📊 Calculadora EPH – INDEC - UCCuyo

Esta calculadora interactiva permite cargar bases de datos del **4º trimestre de la Encuesta Permanente de Hogares (EPH)** del INDEC, junto con el instructivo de variables correspondiente, y obtener automáticamente un **análisis cuantitativo general**.

## 🧰 Funcionalidades

- 📂 Carga de base de **hogares**
- 📂 Carga de base de **individuos**
- 📄 Carga de instructivo PDF (extrae nombres nominales)
- 📊 Análisis descriptivo automático de todas las columnas
- 📥 Exportación del informe en formato Excel

## 🚀 Cómo usar en Streamlit

1. Subí este repositorio a tu cuenta de GitHub.
2. Iniciá sesión en [streamlit.io/cloud](https://streamlit.io/cloud).
3. Seleccioná el repositorio y el archivo `streamlit_app.py`.
4. Ejecutá la app online.

## 📁 Estructura del repositorio

```
├── streamlit_app.py       # Código principal de la aplicación Streamlit
├── requirements.txt       # Lista de dependencias necesarias
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Documentación del proyecto
```

## 📌 Requisitos

- Python 3.8 o superior
- Streamlit
- Pandas
- openpyxl
- PyMuPDF

## 📄 Créditos

Desarrollado para análisis públicos de datos abiertos de la EPH – INDEC.
