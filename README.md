# Spinning Drop Profile Simulation

## Project Overview

This Python script numerically integrates the profile of a liquid drop spinning rapidly around an axis while levitating. The equilibrium shape is governed by the **Young-Laplace Equation**, which balances two forces:

1.  **Capillary Pressure:** Due to surface tension ($\sigma$).
2.  **Centrifugal Pressure:** Due to rotation ($\omega$).

## Physics and Non-Dimensionalization

To simplify the governing equations, lengths are scaled by the **Rotational Capillary Length Scale ($L_c$)**:

$$L_c = \left( \frac{\sigma}{\Delta\rho \cdot \omega^2} \right)^{1/3}$$

The `spinning_drop_profile_solver` function solves the non-dimensional ODE system using the Euler method (implemented iteratively). The key ODE governing the change in angle $\psi$ is derived from the Young-Laplace equation:

$$\frac{d\psi}{ds} = \frac{2}{R_{\text{top}}} + \frac{z^2}{2\lambda^3} - \frac{\sin(\psi)}{r}$$

## Requirements

* Python 3.x
* `numpy`
* `matplotlib`

## How to Run

1.  **Save the Code:** Ensure the provided Python script is saved as `spinning_drop.py` (or similar).
2.  **Ensure Data Directory:** The script expects a `data` folder to exist in the same directory for saving the output data (`spin.txt`) and the plot (`spin_profile.pdf`).
    ```
    mkdir data
    ```
3.  **Execute:** Run the script from your terminal:
    ```
    python spinning_drop.py
    ```

### **Output Files**

The script generates two main output files in the `data/` directory:

1.  **`data/spin.txt`**: Raw non-dimensional data columns: `r_nd`, `z_nd`, `psi_nd`, `dPsi_nd/ds`, and `L_c`.
2.  **`data/spin_profile.pdf`**: A PDF visualization of the calculated drop profile, showing the full 2D cross-section in millimeters (mm).

## Example Output

The figure below shows the calculated profile based on the default parameters (`\sigma = 72 \text{ mN/m}`, $\Delta\rho = 1000 \text{ kg/m}^3$, $\omega = 759 \text{ rad/s}$):
