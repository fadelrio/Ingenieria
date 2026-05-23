# TP2 - Diodo
# Simulacion TCAD con DEVSIM
# Funciones para generacion de graficos y extraer informacion de la simulacion

from devsim import (
    get_node_model_values,
    get_element_node_list,
    get_edge_model_values
)

## Devsim custom
import src.diode_common
from src.new_physics import *
from src.plot import *
## Graficos
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm as cm
## Numerico
import numpy as np

def plot_mesh_with_contacts(contactos, device, region):
    x = 1e4*np.array(get_node_model_values(device=device, region=region, name="x"))
    y = 1e4*np.array(get_node_model_values(device=device, region=region, name="y"))

    tri_list = get_element_node_list(device=device, region=region, reorder=True)
    triangles = np.array(tri_list)

    triang = tri.Triangulation(x, y, triangles)

    fig, ax = plt.subplots()
    plt.triplot(triang, color='k', linewidth=0.5, marker='o', markersize=2)  

    num_contactos = len(contactos)
    colormap = cm.get_cmap('viridis', num_contactos) 

    for idx, contact_name in enumerate(contactos):

        element_node_lists = get_element_node_list(
            device=device,
            region=region,
            contact=contact_name
        )

        unique_node_ids = set()
        for elm_nodes in element_node_lists:
            for node_id in elm_nodes:
                unique_node_ids.add(node_id)

        all_x = get_node_model_values(
            device=device,
            region=region,
            name="x"
        )
        all_y = get_node_model_values(
            device=device,
            region=region,
            name="y"
        )

        sorted_nodes = sorted(unique_node_ids)
        x_contact = [all_x[node_id] for node_id in sorted_nodes]
        y_contact = [all_y[node_id] for node_id in sorted_nodes]

        color = colormap(idx) 
        plt.scatter(
            1e4*np.array(x_contact),
            1e4*np.array(y_contact),
            color=color,
            marker='o',
            s=25,
            label=f"{contact_name}"
        )

    plt.xlabel("x [um]")
    plt.ylabel("y [um]")
    plt.title("Mallado")
    plt.legend(loc='best', fontsize='small')
    plt.show()

def plot_doping(device,region):
    x = 1e4*np.array(get_node_model_values(device=device, region=region, name="x"))
    y = 1e4*np.array(get_node_model_values(device=device, region=region, name="y"))
    doping = np.array(get_node_model_values(device=device, region=region, name="NetDoping")) 

    fig, ax = plt.subplots()
    ax.tricontour(x, y, doping, levels=18, linewidths=0.1, colors="k", extend="both")
    cntr = ax.tricontourf(x, y, doping, levels=18, cmap="rainbow", extend="both")
    fig.colorbar(cntr, ax=ax)
    plt.title("Dopaje total")
    plt.show()

def get_potential(device, region, voltage, plot):
    x = 1e4*np.array(get_node_model_values(device=device, region=region, name="x"))
    y = 1e4*np.array(get_node_model_values(device=device, region=region, name="y"))
    potential = np.array(get_node_model_values(device=device, region=region, name="Potential")) # Potencial

    y_min, y_max = float(y.min()), float(y.max())
    y_mid = 0.5*(y_min + y_max)
    tol = 0.02*(y_max - y_min)   
    mask = np.abs(y - y_mid) <= tol
    x_line = x[mask]
    pot_line = potential[mask]
    order = np.argsort(x_line)
    x_line = x_line[order]
    pot_line = pot_line[order]

    if plot:
        fig2, ax2 = plt.subplots()
        ax2.tricontour(x, y, potential, levels=18, linewidths=0.1, colors="k")
        cntr2 = ax2.tricontourf(x, y, potential, levels=18, cmap="rainbow")
        fig2.colorbar(cntr2, ax=ax2)
        plt.title("Potencial interno (Vd={}V)".format(voltage))
        plt.show()

    return pot_line

def get_carriers(device, region, voltage, plot):
    x = 1e4*np.array(get_node_model_values(device=device, region=region, name="x"))
    y = 1e4*np.array(get_node_model_values(device=device, region=region, name="y"))
    n = np.array(get_node_model_values(device=device, region=region, name="Electrons"), dtype=float)
    p = np.array(get_node_model_values(device=device, region=region, name="Holes"), dtype=float)
    y_min, y_max = float(y.min()), float(y.max())
    y_mid = 0.5*(y_min + y_max)
    tol = 0.002*(y_max - y_min)   
    mask = np.abs(y - y_mid) <= tol
    x_line = x[mask]
    n_line = n[mask]
    p_line = p[mask]
    order = np.argsort(x_line)
    x_line = x_line[order]
    n_line = n_line[order]
    p_line = p_line[order]

    if plot:
        plt.figure()
        plt.semilogy(x_line, n_line, label="Electrones")
        plt.semilogy(x_line, p_line, label="Huecos")
        plt.xlabel("x [um]")  
        plt.ylabel("Densidad [cm-3]")
        plt.title("Densidades de portadores (Vd={}V)".format(voltage))
        plt.legend()
        plt.grid(True)
        plt.show()

    return n_line,p_line

def get_Efield(device, region, voltage, plot):
    x = np.array(get_node_model_values(device=device, region=region, name="x"), float)
    y = np.array(get_node_model_values(device=device, region=region, name="y"), float)
    phi = np.array(get_node_model_values(device=device, region=region, name="Potential"), float)

    y_mid = 0.5*(y.min() + y.max())
    tol = 0.02*(y.max() - y.min())
    mask = np.abs(y - y_mid) <= tol

    x_line = x[mask]
    phi_line = phi[mask]

    order = np.argsort(x_line)
    x_line = x_line[order]
    phi_line = phi_line[order]

    Ex_line = -np.gradient(phi_line, x_line)

    if plot:
        plt.figure()
        plt.plot(1e4*x_line, 1e6*Ex_line)
        plt.xlabel("x [um]")  
        plt.ylabel("E [MV/cm]")
        plt.title("Campo eléctrico (Vd={}V)".format(voltage))
        plt.grid(True)
        plt.show()

    return x_line, Ex_line

def get_currents(device, region, voltage, plot):
    x = 1e4*np.array(get_edge_model_values(device=device, region=region, name="x_edge"))
    y = 1e4*np.array(get_edge_model_values(device=device, region=region, name="y_edge"))


    Jn = np.array(get_edge_model_values(device=device, region=region, name="Jn_arora_lf"), dtype=float)
    Jp = np.array(get_edge_model_values(device=device, region=region, name="Jp_arora_lf"), dtype=float)
    y_min, y_max = float(y.min()), float(y.max())
    y_mid = 0.5*(y_min + y_max)
    tol = 0.02*(y_max - y_min)   
    mask = np.abs(y - y_mid) <= tol
    x_line = x[mask]
    Jn_line = Jn[mask]
    Jp_line = Jp[mask]
    order = np.argsort(x_line)
    x_line = x_line[order]
    Jn_line = Jn_line[order]
    Jp_line = Jp_line[order]

    if plot:
        plt.figure()
        plt.plot(x_line, Jn_line, label="Electrones")
        plt.plot(x_line, Jp_line, label="Huecos")
        plt.xlabel("x [um]")  
        plt.ylabel("J [A/cm2]")
        plt.title("Densidad de corriente (Vd={}V)".format(voltage))
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()

    return Jn_line,Jp_line
