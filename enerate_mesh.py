mport gmsh

def generate_jet_engine_mesh():
    gmsh.initialize()
    gmsh.model.add("jet_engine_part")

    # Example: create simple rotor blade geometry (simplified)
    gmsh.model.occ.addBox(0, 0, 0, 1, 0.2, 0.05) 

    gmsh.model.occ.synchronize()

    # Mesh settings
    gmsh.option.setNumber("Mesh.ElementOrder", 2)  # quadratic elements
    gmsh.model.mesh.generate(3)

    gmsh.write("jet_engine_mesh.msh")
    gmsh.finalize()

if __name__ == "__main__":
    generate_jet_engine_mesh()
