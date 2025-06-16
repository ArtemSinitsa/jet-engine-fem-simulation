import gmsh
import sys
import os

def generate_jet_engine_mesh():
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("jet_engine")

    # Create a simple disk + blade block to simulate a rotor hub

    # Rotor disk (cylinder)
    disk = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, 0.2, 0.5)

    # Simplified blade (box on top of disk)
    blade = gmsh.model.occ.addBox(0.15, 0, 0.2, 0.1, 0.05, 0.2)

    gmsh.model.occ.fuse([(3, disk)], [(3, blade)], removeObject=True, removeTool=True)
    gmsh.model.occ.synchronize()

    # Mesh parameters
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.02)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.05)

    gmsh.model.mesh.generate(3)
    gmsh.write("jet_engine_mesh.msh")

    gmsh.finalize()

if __name__ == "__main__":
    generate_jet_engine_mesh()
sfepy-convert jet_engine_mesh.msh jet_engine_mesh.mesh
