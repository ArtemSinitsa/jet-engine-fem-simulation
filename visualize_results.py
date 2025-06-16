import pyvista as pv

# Load VTK result
mesh = pv.read("result.vtk")

# Plot displacement magnitude
displacement = mesh.point_data['u']
mesh['Displacement Magnitude'] = (displacement**2).sum(axis=1)**0.5

plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars='Displacement Magnitude', cmap="viridis")
plotter.show()

