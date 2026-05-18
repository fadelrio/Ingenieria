# Prueba de instalación de DEVSIM
Universdad de Buenos Aires - Facultad de Ingeniería

Dispositivos Semiconductores - TB070

## Instalacion con un Virtual Environment de Python

Importante: debe contar con una versión de Python igual a 3.7 o superior.

1. Crear una carpeta donde se alojará el proyecto.
2. Abrir una consola y posicionarse en dicha carpeta.
3. Crear el virtual environment con la siguiente línea: 

> python3 -mvenv denv 

(de acuerdo a su instalación, puede que necesite reemplazar python3 por python o py).

4. Activar el environment:
- En Linux: source denv/bin/activate
- En Windows (en una CMD): ./denv/Scripts/activate.bat
  
5. Instalar paquetes de soporte en el siguiente orden:

> pip install numpy
> pip install mkl
> pip install matplotlib
> pip install devsim

## Instalación con Anaconda

1. Descargar Anaconda: https://www.anaconda.com/download
2. Instalar Python usando Anaconda. Asegurarse de tener una version superior a la 3.13.
> conda install python

3. Crear una carpeta donde se alojará el proyecto.
4. Abrir una consola y posicionarse en dicha carpeta.
5. Crear el virtual environment con la siguiente línea: 
> conda create -n denv

6. Activar el environment: 
> conda activate denv

7. Instalar paquetes de soporte en el siguiente orden:

> conda install numpy 
>
> conda install mkl
> 
> conda install matplotlib
> 
> conda install pip
> 
> pip install devsim

## Ejecución de la prueba

Una vez instalado Devsim y los paquetes necesarios, correr el script `prueba_instalacion.py`

Deberá aparecer un gráfico llamado "Mallado". En el gráfico, debe haber una leyenda que indique la existencia de dos contactos: ánodo y cátodo.

Luego de cerrar el gráfico, el script deberá reportar:

> PRUEBA EJECUTADA CON ÉXITO
> 
> FIN DEL SCRIPT 

Si ha logrado completar todos estos pasos, entonces su instalación de Devsim se encuentra lista para los trabajos prácticos de la materia.