# PRUEBA DE INSTALACION DE DEVSIM

##### IMPORTAR LIBRERIAS
## Manejo de archivos
import os
## Devsim standard
from devsim import *

## Devsim custom
import src.diode_common as diode_common
from src.new_physics import *
from src.plot import *
## Graficos
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm as cm
## Numerico
import numpy as np

##### PARAMETROS GLOBALES FIJOS
device = "Diodo"
region = "AreaDiodo"

#####################################################################
##### PARAMETROS GLOBALES
altura = 10e-4 # [cm] Altura del diodo. A mayor altura, mayor corriente
Wp = 10e-4 # [cm] Extension lado P (incluyendo QNR-P y zona de vaciamiento P)
Wn = 10e-4 # [cm] Extension lado N (incluyendo QNR-N y zona de vaciamiento N)
Wtotal = Wp + Wn # [cm] Extension total del diodo 
interfaz = Wtotal/2

##### CREAR MALLADO Y MOSTRARLO
low_res = 0.5e-4
high_res = low_res/50
diode_common.Create2DMesh(device, region, interface=interfaz, height=altura, total_width=Wtotal, low_res=low_res, high_res=high_res)

contactos = ["Anodo", "Catodo"]

plot_mesh_with_contacts(contactos=contactos, device=device, region=region)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("PRUEBA EJECUTADA CON ÉXITO")
print("FIN DEL SCRIPT")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")