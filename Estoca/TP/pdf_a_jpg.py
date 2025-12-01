import os
from pdf2image import convert_from_path

# === CONFIGURACIÓN ===
directorio = "./graficos_pdf"          # Carpeta con los PDFs
salida = "./graficos_jpg"              # Carpeta donde guardar los JPG
dpi = 1200                      # Resolución alta (podés subirlo si necesitás)

# Crear directorio de salida si no existe
os.makedirs(salida, exist_ok=True)

# Listar todos los archivos PDF del directorio
pdfs = [f for f in os.listdir(directorio) if f.lower().endswith(".pdf")]

if not pdfs:
    print("No se encontraron archivos PDF en el directorio.")
    exit()

for pdf in pdfs:
    ruta_pdf = os.path.join(directorio, pdf)
    nombre_base = os.path.splitext(pdf)[0]

    print(f"Convirtiendo: {pdf} ...")

    # Convertir cada página a imagen
    paginas = convert_from_path(ruta_pdf, dpi=dpi)

    for i, pagina in enumerate(paginas):
        nombre_salida = f"{nombre_base}_pag{i+1}.jpg"
        ruta_salida = os.path.join(salida, nombre_salida)
        pagina.save(ruta_salida, "JPEG", quality=100)
    
    print(f"✔ Listo: {pdf}")

print("\nConversión completa.")

