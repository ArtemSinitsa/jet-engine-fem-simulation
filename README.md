#  Jet Engine Component FEM Simulation

This project performs **Finite Element Analysis (FEA)** of a simplified jet engine component under **centrifugal and thermal loads** using Python and SfePy.

It models realistic **mechanical behavior**, **rotational body forces**, **multiphysics coupling**, and advanced meshing techniques. The mesh consists of **~370,000 volume elements**, solving for **displacement, stress, and internal force fields**.

---

##  Governing Mathematical Model

We solve the following coupled **thermoelastic PDEs**:

###  Linear Momentum Balance Equation

(displacement field under body and surface forces)

\[
\nabla \cdot \boldsymbol{\sigma} + \rho \mathbf{f} = \rho \ddot{\mathbf{u}}
\]

In quasi-static form (no acceleration), this simplifies to:

\[
\nabla \cdot \boldsymbol{\sigma} + \rho \mathbf{f} = 0
\]

---

###  Constitutive Equation (Hooke’s Law for isotropic materials)

\[
\boldsymbol{\sigma} = \lambda (\nabla \cdot \mathbf{u}) \mathbf{I} + 2\mu \boldsymbol{\varepsilon}
\]

with

\[
\boldsymbol{\varepsilon} = \frac{1}{2}(\nabla \mathbf{u} + \nabla \mathbf{u}^T)
\]

Where:

- \( \boldsymbol{\sigma} \) is the Cauchy stress tensor  
- \( \boldsymbol{\varepsilon} \) is the small strain tensor  
- \( \mathbf{u} \) is the displacement field  
- \( \lambda, \mu \) are Lamé parameters

---

###  Body Force Field (centrifugal)

\[
\mathbf{f}_{\text{centrifugal}} = \omega^2 \, \mathbf{r}_\perp
\]

where

\[
\mathbf{r}_\perp =
\begin{bmatrix}
x \\ y \\ 0
\end{bmatrix}
\]

---

###  Thermal Expansion (optional module)

\[
\boldsymbol{\sigma}_{\text{thermal}} = -3 K \alpha \Delta T \mathbf{I}
\]

added to

\[
\boldsymbol{\sigma}_{\text{total}} = \boldsymbol{\sigma}_{\text{elastic}} + \boldsymbol{\sigma}_{\text{thermal}}
\]

Where:

- \( K \) — bulk modulus  
- \( \alpha \) — thermal expansion coefficient  
- \( \Delta T \) — temperature rise

---

##  Technical Details

- Mesh format: `.mesh` (can be generated with Gmsh)
- FEA framework: `SfePy`
- Solver: `ScipyDirect` + Newton-Raphson
- Degrees of Freedom (DoF): ~1.1 million (vector displacement field)
- Solution time: under 10 minutes on standard workstation

---

##  Capabilities

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
