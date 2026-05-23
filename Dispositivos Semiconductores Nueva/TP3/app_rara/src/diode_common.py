# TP2 - Diodo
# Simulacion TCAD con DEVSIM

from devsim import (
    add_2d_contact,
    add_2d_mesh_line,
    add_2d_region,
    create_2d_mesh,
    create_device,
    finalize_mesh,
    get_contact_list,
    set_node_values,
    set_parameter
)
from src.new_physics import *

from devsim.python_packages.model_create import CreateNodeModel, CreateSolution

from devsim.python_packages.simple_physics import (
    GetContactBiasName,
    SetSiliconParameters
)

def Create2DMesh(device, region, interface, height, total_width, low_res=0.5e-4, high_res=0.05e-4):
    
    # Estructura del diodo
    create_2d_mesh(mesh="dio")
    add_2d_mesh_line(mesh="dio", dir="x", pos=0, ps=low_res)
    add_2d_mesh_line(mesh="dio", dir="x", pos=total_width, ps=low_res)
    add_2d_mesh_line(mesh="dio", dir="x", pos=interface, ps=high_res)
    add_2d_mesh_line(mesh="dio", dir="y", pos=0, ps=low_res)
    add_2d_mesh_line(mesh="dio", dir="y", pos=height, ps=low_res)

    # Los contactos no pueden estar en el final del mallado
    add_2d_mesh_line(mesh="dio", dir="x", pos=-high_res, ps=high_res)
    add_2d_mesh_line(mesh="dio", dir="x", pos=total_width+high_res, ps=high_res) 
    add_2d_mesh_line(mesh="dio", dir="y", pos=-high_res, ps=high_res)
    add_2d_mesh_line(mesh="dio", dir="y", pos=height+high_res, ps=high_res)   

    # Asociar materiales
    add_2d_region(mesh="dio", material="Si", region=region)
    add_2d_region(mesh="dio", material="air", region="air1", xl=-high_res, xh=0)
    add_2d_region(mesh="dio", material="air", region="air2", xl=total_width, xh=total_width+high_res)
    add_2d_region(mesh="dio", material="air", region="air3", yl=-high_res, xh=0)
    add_2d_region(mesh="dio", material="air", region="air4", yl=height, yh=height+high_res)

    add_2d_contact(
        mesh="dio",
        name="Anodo",
        material="metal",
        region=region,
        yl=0,
        xl=0,
        yh=height,
        xh=2*high_res,
        bloat=1e-6,
    )
    add_2d_contact(
        mesh="dio",
        name="Catodo",
        material="metal",
        region=region,
        yl = height,
        xl=total_width,
        yh = 0,
        xh=total_width,
        bloat=1e-6,
    )

    finalize_mesh(mesh="dio")
    create_device(mesh="dio", device=device)


def SetParameters(device, region):
    """
    Set parameters for 300 K
    """
    SetSiliconParameters(device, region, 300)


def SetNetDoping(device, region, Na, Nd, interface):
    """
    NetDoping
    """
    CreateNodeModel(device, region, "Donors", "{}*step(x-{})".format(Nd, interface))
    CreateNodeModel(device, region, "Acceptors", "{}*step({}-x)".format(Na, interface))
    CreateNodeModel(device, region, "NetDoping", "Donors-Acceptors")


def InitialSolution(device, region, circuit_contacts=None):
    # Create Potential, Potential@n0, Potential@n1
    CreateSolution(device, region, "Potential")

    # Create potential only physical models
    CreateSiliconPotentialOnly(device, region)

    # Set up the contacts applying a bias
    for i in get_contact_list(device=device):
        if circuit_contacts and i in circuit_contacts:
            CreateSiliconPotentialOnlyContact(device, region, i, True)
        else:
            ###print "FIX THIS"
            ### it is more correct for the bias to be 0, and it looks like there is side effects
            set_parameter(device=device, name=GetContactBiasName(i), value=0.0)
            CreateSiliconPotentialOnlyContact(device, region, i)


def DriftDiffusionInitialSolution(device, region, enable_SRH=True, circuit_contacts=None):
    ####
    #### drift diffusion solution variables
    ####
    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")

    ####
    #### create initial guess from dc only solution
    ####
    set_node_values(
        device=device, region=region, name="Electrons", init_from="IntrinsicElectrons"
    )
    set_node_values(
        device=device, region=region, name="Holes", init_from="IntrinsicHoles"
    )

    ###
    ### Set up equations
    ###
    opts = CreateAroraMobilityLF(device, region)
    CreateSiliconDriftDiffusion(device, region, enable_SRH,  **opts)
    for i in get_contact_list(device=device):
        CreateSiliconDriftDiffusionContact(device, region, i, Jn=opts['Jn'], Jp=opts['Jp'])
