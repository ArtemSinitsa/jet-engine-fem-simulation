#  Jet Engine Component FEM Simulation

This project performs **Finite Element Analysis (FEA)** of a simplified jet engine component under **centrifugal and thermal loads** using Python and SfePy.

It models realistic mechanical behavior, rotational body forces, multiphysics coupling, and advanced meshing techniques. The mesh consists of ~370,000 volume elements, solving for displacement, stress, and internal force fields.

---

##  Governing Mathematical Model

We solve the following coupled thermoelastic PDEs:

### Linear Momentum Balance Equation

(displacement field under body and surface forces)

Div(sigma) + rho * f = rho * (d²u/dt²)

In quasi-static form (no acceleration), this simplifies to:

Div(sigma) + rho * f = 0

---

### Constitutive Equation (Hooke’s Law for isotropic materials)

sigma = lambda * (Div(u)) * I + 2 * mu * epsilon

with

epsilon = 0.5 * (Grad(u) + Grad(u)^T)

Where:

- sigma is the Cauchy stress tensor
- epsilon is the small strain tensor
- u is the displacement field
- lambda, mu are Lamé parameters

---

### Body Force Field (centrifugal)

f_centrifugal = omega² * r_perpendicular

where r_perpendicular = [x, y, 0]

---

### Thermal Expansion (optional module)

sigma_thermal = -3 * K * alpha * Delta_T * I

added to total stress:

sigma_total = sigma_elastic + sigma_thermal

Where:

- K — bulk modulus
- alpha — thermal expansion coefficient
- Delta_T — temperature rise

---

## Technical Details

- Mesh format: `.mesh` (can be generated with Gmsh)
- FEA framework: `SfePy`
- Solver: `ScipyDirect` + Newton-Raphson
- Degrees of Freedom (DoF): ~1.1 million (vector displacement field)
- Solution time: under 10 minutes on standard workstation

---

## Capabilities

- Centrifugal stress from rotor spin
- Material property definition
- 3D volumetric meshing
- Future-ready for:
  - Contact mechanics
  - Modal (vibration) analysis
  - Nonlinear material models
  - Time-dependent thermal fields

---

##  Output

- Results saved in `.vtk` format, viewable with ParaView
- Displacement fields
- Stress contours
- Deformed mesh animation (optional with tools like PyVista)
