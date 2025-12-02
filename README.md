# Spinning Drop Profile Simulation

## Project Overview

This Python script numerically integrates the profile of a liquid drop spinning rapidly around an axis while levitating. The equilibrium shape is governed by the **Young-Laplace Equation**, which balances two forces:

1.  **Capillary Pressure:** Due to surface tension ($\sigma$).
2.  **Centrifugal Pressure:** Due to rotation ($\omega$).

## Physics and Non-Dimensionalization

To simplify the governing equations, lengths are scaled by the **Rotational Capillary Length**:

$$\lambda = \left( \frac{\sigma}{\Delta\rho \cdot \omega^2} \right)^{1/3}$$

The `spinning_drop_profile_solver` function solves the non-dimensional ODE system using the Euler method (implemented iteratively). The key ODE governing the change in interface angle to the horizontal $\psi$ is derived from the Young-Laplace equation:

$$\frac{d\psi}{ds} = \frac{2}{R_{\text{top}}} + \frac{z^2}{2\lambda^3} - \frac{\sin(\psi)}{r}$$

Where $s$ is the arc length along the drop interface, starting from the tip/neck. This is the integration coordinate.

$\psi$ is the Interface Angle (or Angle of Inclination). This is the angle the tangent to the drop profile makes with the axis of rotation. It starts at $\psi=0$ at the tip and approaches $\psi=\pi$ at the far pole (if the drop closes).

$R_{\text{top}}$ is the radius of curvature at the starting point (the tip of the drop). This value is the critical *shooting parameter* that must be adjusted to find a closed, stable drop profile.

$z$ is the axial coordinate (distance from the center of rotation along the axis).

$r$ is the radial oordinate (distance from the axis of rotation).

## Requirements

* Python 3.x
* `numpy`
* `matplotlib`

## How to Run

Run the script from your terminal:
    ```
    python spinning_drop.py
    ```

### **Output Files**

The script generates two main output files in the `data/` directory:

1.  **`data/spin.txt`**: Raw non-dimensional data columns: `r`, `z`, `psi`, `dPsi/ds`, and `lambda`.
2.  **`data/spin.pdf`**: A PDF visualization of the calculated drop profile, showing the full 2D cross-section in millimeters (mm).

## Example Output

The figure below shows the calculated profile based on the default parameters (`\sigma = 72 \text{ mN/m}`, $\Delta\rho = 1000 \text{ kg/m}^3$, $\omega = 759 \text{ rad/s}$):

![Calculated Profile of the Spinning Drop](data/spin.svg)
