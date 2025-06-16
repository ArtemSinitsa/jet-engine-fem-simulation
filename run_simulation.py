import numpy as np
from sfepy.discrete.fem import Mesh, FEDomain, Field
from sfepy.discrete import FieldVariable, Material, Problem
from sfepy.terms import Term
from sfepy.discrete.conditions import EssentialBC
from sfepy.solvers.ls import ScipyDirect
from sfepy.solvers.nls import Newton
import os

mesh = Mesh.from_file('data/jet_engine_mesh.mesh')
domain = FEDomain('domain', mesh)
min_x, max_x = domain.get_mesh_bounding_box()[:, 0]
eps = 1e-8
omega = domain.create_region('Omega', 'all')
left = domain.create_region('Left', f'vertices in x < {min_x + eps}', 'facet')

field = Field.from_args('displacement', np.float64, 'vector', omega, approx_order=1)

u = FieldVariable('u', 'unknown', field)
v = FieldVariable('v', 'test', field, primary_var_name='u')

# Material parameters
young_modulus = 70e9  # Pa
poisson_ratio = 0.33
density = 2700  # kg/m³ (aluminum)

lam = young_modulus * poisson_ratio / ((1 + poisson_ratio) * (1 - 2 * poisson_ratio))
mu = young_modulus / (2 * (1 + poisson_ratio))
D = np.array([[lam + 2*mu, lam, lam, 0, 0, 0],
              [lam, lam + 2*mu, lam, 0, 0, 0],
              [lam, lam, lam + 2*mu, 0, 0, 0],
              [0, 0, 0, mu, 0, 0],
              [0, 0, 0, 0, mu, 0],
              [0, 0, 0, 0, 0, mu]])

material = Material('solid', D=D, rho=density)

# Angular velocity
omega_rot = 5000 * 2*np.pi / 60  # convert RPM to rad/s

# Create centrifugal force function
def centrifugal_load(ts, coors, mode=None, **kwargs):
    if mode != 'qp': return
    x, y, z = coors[:,0], coors[:,1], coors[:,2]
    r = np.sqrt(x**2 + y**2)
    fx = density * omega_rot**2 * x
    fy = density * omega_rot**2 * y
    fz = np.zeros_like(fx)
    val = np.vstack([fx, fy, fz]).T
    return {'val': val}

# Register force function
from sfepy.discrete import Function, Material
centrifugal = Material('centrifugal', function=Function('centrifugal_load', centrifugal_load))

integral = 2
t1 = Term.new('dw_lin_elastic(solid.D, v, u)', integral, omega, solid=material, v=v, u=u)
t2 = Term.new('dw_volume_lvf(centrifugal.val, v)', integral, omega, centrifugal=centrifugal, v=v)

fix = EssentialBC('fix', left, {'u.all': 0.0})

pb = Problem('elasticity', equations={'balance': t1 + t2})
pb.set_bcs(ebcs=fix)
pb.set_solver(nls=Newton({}, lin_solver=ScipyDirect({})))

status = pb.solve()

os.makedirs('data', exist_ok=True)
pb.save_state('data/result.vtk', status)

print("FEM simulation with centrifugal loading completed: data/result.vtk")

