from PIL import Image
import glob
import os

# Ruta de los archivos BMP (ajusta según sea necesario)
input_folder = "../imagenes/"
output_folder = "../imagenes/convertidas"

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Buscar todas las imágenes BMP en la carpeta
bmp_files = glob.glob(os.path.join(input_folder, "*.BMP"))

# Convertir cada imagen
for file in bmp_files:
    # Cargar imagen
    img = Image.open(file)

    # Crear el nuevo nombre con extensión .jpeg
    filename = os.path.basename(file).replace(".BMP", ".jpeg")
    output_path = os.path.join(output_folder, filename)

    # Guardar como JPEG con calidad 95
    img.convert("RGB").save(output_path, "JPEG", quality=95)

    print(f"Convertido: {file} -> {output_path}")

print("Conversión completada.")

