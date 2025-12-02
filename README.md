💧 Spinning Drop Profile Simulation

Project Overview

This Python script numerically integrates the profile of a liquid drop spinning rapidly while levitating. The equilibrium shape is governed by the Young-Laplace Equation, which balances two forces:

Capillary Pressure: Due to surface tension ($\sigma$).

Centrifugal Pressure: Due to rotation ($\omega$).

The code utilizes the Shooting Method by performing an Initial Value Problem (IVP) integration along the arc length ($s$) and adjusting the initial curvature to satisfy the boundary condition (either volume or shape closure).

 Physics and Non-Dimensionalization

To simplify the governing equations, all physical lengths are scaled by the Rotational Capillary Length Scale ($L_c$):

$$L_c = \left( \frac{\sigma}{\Delta\rho \cdot \omega^2} \right)^{1/3}$$

The spinning_drop_profile_solver function solves the non-dimensional ODE system using a fixed-step Euler method (implemented iteratively). The key ODE governing the change in angle $\psi$ is derived from the Young-Laplace equation:

$$\frac{d\psi}{ds} = \frac{1}{R_1} + \frac{1}{R_2}$$

Where the principal radii of curvature ($R_1$ and $R_2$) are expanded to include the centrifugal pressure term, $R_1$ and $R_2$ are the principal radii of curvature. The non-dimensional form solved is:

$$\frac{d\psi}{ds} = \left( \frac{2}{R_{\text{neck}}} \right)_{\text{ND}} + \left( \frac{r^2}{2} \right)_{\text{ND}} - \frac{\sin(\psi)}{r}$$

🛠️ Requirements

Python 3.x

numpy

matplotlib

How to Run

Save the Code: Ensure the provided Python script is saved as spinning_drop.py (or similar).

Ensure Data Directory: The script expects a data folder to exist in the same directory for saving the output data (spin.txt) and the plot (spin.pdf).

mkdir data


Execute: Run the script from your terminal:

python spinning_drop.py


Output Files

The script generates two main output files in the data/ directory:

data/spin.txt: Raw non-dimensional data columns: r_nd, z_nd, psi_nd, dPsi_nd/ds, and L_c.

data/spin.pdf: A PDF visualization of the calculated drop profile, showing the full 2D cross-section in millimeters (mm).

Example Output

The figure below shows the calculated profile based on the default parameters (\sigma = 72 \text{ mN/m}, $\Delta\rho = 1000 \text{ kg/m}^3$, $\omega = 759 \text{ rad/s}$):
