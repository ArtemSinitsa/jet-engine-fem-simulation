import numpy as np
from sfepy import data_dir
from sfepy.discrete.fem import Mesh, FEDomain, Field
from sfepy.discrete import (FieldVariable, Material, Problem)
from sfepy.terms import Term
from sfepy.discrete.conditions import EssentialBC
from sfepy.solvers.ls import ScipyDirect
from sfepy.solvers.nls import Newton

# Load mesh
mesh = Mesh.from_file('jet_engine_mesh.mesh')

# Define domain
domain = FEDomain('domain', mesh)
min_x, max_x = domain.get_mesh_bounding_box()[:, 0]
eps = 1e-8
omega = domain.create_region('Omega', 'all')
left = domain.create_region('Left', f'vertices in x < {min_x + eps}', 'facet')

# Create field (displacement)
field = Field.from_args('displacement', np.float64, 'vector', omega, approx_order=1)

# Variables
u = FieldVariable('u', 'unknown', field)
v = FieldVariable('v', 'test', field, primary_var_name='u')

# Material properties
young_modulus = 70e9  # Pa (aluminum alloy)
poisson_ratio = 0.33

lam = young_modulus * poisson_ratio / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))
mu = young_modulus / (2 * (1 + poisson_ratio))
D = np.array([[lam + 2*mu, lam, lam, 0, 0, 0],
              [lam, lam + 2*mu, lam, 0, 0, 0],
              [lam, lam, lam + 2*mu, 0, 0, 0],
              [0, 0, 0, mu, 0, 0],
              [0, 0, 0, 0, mu, 0],
              [0, 0, 0, 0, 0, mu]])

material = Material('solid', D=D)

# Define weak form (linear elasticity)
integral = 2
t1 = Term.new('dw_lin_elastic(solid.D, v, u)', integral, omega, solid=material, v=v, u=u)

# Boundary conditions (fixed left face)
fix = EssentialBC('fix', left, {'u.all': 0.0})

# Problem setup
pb = Problem('elasticity', equations={'balance': t1})
pb.set_bcs(ebcs=fix)

# Solver setup
pb.set_solver(nls=Newton({}, lin_solver=ScipyDirect({})))

# Solve
status = pb.solve()
pb.save_state('result.vtk', status)

print("Simulation complete.")

