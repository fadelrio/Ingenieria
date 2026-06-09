# TP2 - Diodo
# Simulacion TCAD con DEVSIM

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

##### DECLARACION DE VARIABLES
totalCurrent = []
appliedVoltage = []
electronCurrent = []
holeCurrent = []

##### PARAMETROS GLOBALES FIJOS
device = "Diodo"
region = "AreaDiodo"

#####################################################################
##### PARAMETROS GLOBALES MODIFICABLES
## Tension aplicada
Va_min = -0.3 # [V] Minima tension en reversa
Va_max = 0.4 # [V] Maxima tension en directa
paso = 0.005 # [V] Pasos de tension en el barrido

##### Dimensiones, dopajes y tiempos de vida
Na = 3e15 # [cm-3] Dopaje aceptor lado P
Nd = 1e15 # [cm-3] Dopaje donor lado N
Wp = 10e-4 # [cm] Extension lado P (incluyendo QNR-P y zona de vaciamiento P)
Wn = 10e-4 # [cm] Extension lado N (incluyendo QNR-N y zona de vaciamiento N)
taup = 40e-6 # Tiempo de vida de los minoritarios
taun = 40e-6 # Tiempo de vida de los minoritarios

##### Habilitador del modelo Shockley-Reed-Hall
enable_SRH = False

##### Mostrar graficos
show_plots = True

#####################################################################

##### OTROS PARAMETROS GLOBALES FIJOS
altura = 10e-4 # [cm] Altura del diodo. A mayor altura, mayor corriente
Wtotal = Wp + Wn # [cm] Extension total del diodo 
interfaz = Wtotal/2

##### CREAR MALLADO Y MOSTRARLO
low_res = 0.5e-4
high_res = low_res/50
diode_common.Create2DMesh(device, region, interface=interfaz, height=altura, total_width=Wtotal, low_res=low_res, high_res=high_res)

contactos = ["Anodo", "Catodo"]

if show_plots:
    plot_mesh_with_contacts(contactos=contactos, device=device, region=region)

##### ASOCIAR PARAMETROS DEL SILICIO
diode_common.SetParameters(device=device, region=region)
set_parameter(device=device, region=region, name="taun", value=taun)
set_parameter(device=device, region=region, name="taup", value=taup)

##### ASOCIAR DOPAJES
diode_common.SetNetDoping(device=device, region=region, Na=Na, Nd=Nd, interface=interfaz)

##### GRAFICAR DOPAJES
if show_plots:
    plot_doping(device,region)

###################################################################
########### VD = 0V / ETD #########################################
###################################################################

###### RESOLVER EL DIODO CUANDO Vd = 0V 
## Para hallar una semilla sobre la cual generar el barrido posterior
# Primera solucion considerando solamente la ecuación de Poisson
diode_common.InitialSolution(device, region)
CreateEField(device, region)

solve(type="dc", absolute_error=1.0, relative_error=1e-12, maximum_iterations=30)
# Mejorar solucion incorporando las ecuaciones de arrastre y difusion J = Jarr + Jdif
diode_common.DriftDiffusionInitialSolution(device, region, enable_SRH)
solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

edge_from_node_model(device=device, region=region, node_model="x")
edge_from_node_model(device=device, region=region, node_model="y")
edge_model(device=device, region=region, name="x_edge", equation="0.5*(x@n0 + x@n1)")
edge_model(device=device, region=region, name="y_edge", equation="0.5*(y@n0 + y@n1)")

###### GRAFICAR LA DENSIDAD DE PORTADORES CUANDO Vd = 0V
n_etd, p_etd = get_carriers(device, region, 0, show_plots)
###### GRAFICAR EL CAMPO ELECTRICO INTERNO CUANDO Vd = 0V
x_Efield, E_etd = get_Efield(device, region, 0, show_plots)
###### GRAFICAR EL POTENCIAL INTERNO CUANDO Vd = 0V
phi_etd = get_potential(device, region, 0, show_plots)
###### GRAFICAR LAS CORRIENTES INTERNAS CUANDO Vd = 0V
Jn_etd, Jp_etd = get_currents(device, region, 0, False)

###################################################################
########### VD = VA_MIN / REVERSA #################################
###################################################################

###### LLEVAR EL DIODO A REVERSA
v = 0.0
while v > Va_min:
    set_parameter(device=device, name=GetContactBiasName("Anodo"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    v -= paso

###### GRAFICAR LA DENSIDAD DE PORTADORES EN REVERSA
n_Vamin, p_Vamin = get_carriers(device, region, Va_min, show_plots)
###### GRAFICAR EL CAMPO ELECTRICO INTERNO EN REVERSA
x_Efield, E_Vamin = get_Efield(device, region, Va_min, show_plots)
###### GRAFICAR EL POTENCIAL INTERNO EN REVERSA
phi_Vamin = get_potential(device, region, Va_min, show_plots)
###### GRAFICAR LAS CORRIENTES INTERNAS EN REVERSA
Jn_Vamin, Jp_Vamin = get_currents(device, region, Va_min, show_plots)

###################################################################
########### VD = VA_MAX / DIRECTA #################################
###################################################################

###### LLEVAR EL DIODO A DIRECTA Y ALMACENAR LAS CORRIENTES EN SU RECORRIDO
while v < Va_max:
    set_parameter(device=device, name=GetContactBiasName("Anodo"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

    electronCurrent_i = get_contact_current(
        device=device, contact="Anodo", equation="ElectronContinuityEquation"
    )
    holeCurrent_i = get_contact_current(
        device=device, contact="Anodo", equation="HoleContinuityEquation"
    )
    electronCurrent.append(electronCurrent_i)
    holeCurrent.append(holeCurrent_i)
    totalCurrent.append(electronCurrent_i + holeCurrent_i)
    appliedVoltage.append(v)    
    v += paso

###### GRAFICAR LA DENSIDAD DE PORTADORES EN DIRECTA
n_Vamax, p_Vamax = get_carriers(device, region, Va_max, show_plots)
###### GRAFICAR EL CAMPO ELECTRICO INTERNO EN DIRECTA
x_Efield, E_Vamax = get_Efield(device, region, Va_max, show_plots)
###### GRAFICAR EL POTENCIAL INTERNO EN DIRECTA
phi_Vamax = get_potential(device, region, Va_max, show_plots)
###### GRAFICAR LAS CORRIENTES INTERNAS EN DIRECTA
Jn_Vamax, Jp_Vamax = get_currents(device, region, Va_max, show_plots)

###### GUARDAR RESULTADOS
folder_path = "data_sin_SRH"
os.makedirs(folder_path, exist_ok=True)

if enable_SRH == False:
    ## Barrido de tension
    np.save('data_sin_SRH/voltage.npy', appliedVoltage)
    np.save('data_sin_SRH/electron_current.npy', electronCurrent)
    np.save('data_sin_SRH/hole_current.npy', holeCurrent)
    np.save('data_sin_SRH/total_current.npy', totalCurrent)

    ## Valores en funcion de la posicion cuando Vd = 0V
    np.save('data_sin_SRH/n_etd.npy', n_etd)
    np.save('data_sin_SRH/p_etd.npy', p_etd)
    np.save('data_sin_SRH/Efield_etd.npy', E_etd)
    np.save('data_sin_SRH/phi_etd.npy', phi_etd)
    np.save('data_sin_SRH/Jn_etd.npy', Jn_etd)
    np.save('data_sin_SRH/Jp_etd.npy', Jp_etd)

    ## Valores en funcion de la posicion cuando Vd = Va_min
    np.save('data_sin_SRH/n_Va_min.npy', n_Vamin)
    np.save('data_sin_SRH/p_Va_min.npy', p_Vamin)
    np.save('data_sin_SRH/Efield_Va_min.npy', E_Vamin)
    np.save('data_sin_SRH/phi_Va_min.npy', phi_Vamin)
    np.save('data_sin_SRH/Jn_Va_min.npy', Jn_Vamin)
    np.save('data_sin_SRH/Jp_Va_min.npy', Jp_Vamin)

    ## Valores en funcion de la posicion cuando Vd = Va_max
    np.save('data_sin_SRH/n_Va_max.npy', n_Vamax)
    np.save('data_sin_SRH/p_Va_max.npy', p_Vamax)
    np.save('data_sin_SRH/Efield_Va_max.npy', E_Vamax)
    np.save('data_sin_SRH/phi_Va_max.npy', phi_Vamax)
    np.save('data_sin_SRH/Jn_Va_max.npy', Jn_Vamax)
    np.save('data_sin_SRH/Jp_Va_max.npy', Jp_Vamax)

    ## Guardar vector de coordenadas en X
    x = 1e4*np.array(get_node_model_values(device=device, region=region, name="x"))
    np.save('data_sin_SRH/x_vector.npy', x)
    np.save('data_sin_SRH/x_vector_Efield.npy', x_Efield)
else:
    ## Barrido de tension
    np.save('data_sin_SRH/electron_current_srh.npy', electronCurrent)
    np.save('data_sin_SRH/hole_current_srh.npy', holeCurrent)
    np.save('data_sin_SRH/total_current_srh.npy', totalCurrent)

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("FIN DEL SCRIPT")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")