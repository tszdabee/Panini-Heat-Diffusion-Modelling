# Panini Heat Diffusion Modelling in Python with the Finite Difference Method
Refer to the [Explanation_Report.pdf](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/Explanation_Report.pdf) for a detailed explanation of the following sections.

## Table of Contents
- [Objective](#objective)
- [Physics Model](#physics-model)
- [PDE Model](#pde-model)
- [Initial & Boundary Values](#initial---boundary-values)
  * [Initial Values](#initial-values)
  * [Boundary Values](#boundary-values)
- [Numerical Method](#numerical-method)
- [Discretisation](#discretisation)
  * [Discretisation of boundary conditions](#discretisation-of-boundary-conditions)
- [Results](#results)
- [Additional Remarks](#additional-remarks)

## Objective
To model a heat diffusion within a frozen chicken panini with the explicit finite difference method for PDE's. 

## Physics Model
For simplicity, the following assumptions were made for the physics model of the chicken panini:
* The panini is a perfectly-homogeneous solid cuboid with square-faced bread.
* Boundary conditions are imposed symmetrically, thereby allowing the central cross-section of the panini to be analysed in 2D.
* There are no air gaps in between or within the solids.
* Thermal contact resistance is negligible between panini constituents.
* No temperature fluctuations exist at boundaries (uniformly distributed temperatures).
* Press has a perfectly-flat surface with uniformly distributed temperature.
* The bread and chicken have differing thermal properties, but these properties are invariant in time and space.
* Panini does not experience deformation or internal property changes (e.g. thermal conductivity, k) over time, temperature, or pressure changes.

## PDE Model
The 3D heat diffusion equation in Cartesian coordinates is given as follows:

![Cartesian 3D Heat Diff](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/1.png)

By applying the assumptions listed above under 'Physics Model' to simplify the heat diffusion equation to the following:

![Simplified Heat Diff](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/2.png)

Refer to the [Explanation_Report.pdf](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/Explanation_Report.pdf) for additional steps. The obtained equation is in the form of a parabolic PDE bounded in space but open-ended in time.

## Initial & Boundary Values
### Initial Values
The initial values in the physics model are defined as follows:
* Bread thickness
* Chicken thickness
* Side length of the sandwich
* Initial temperature of entire panini
* The convective heat transfer coefficient of the panini (assumed to be globally constant at 10 W/m$^2$K)
* Thermal properties of the bread and chicken such as conductivity, density, and specific heat capacity at constant pressure
* Ambient air temperature
* Panini press plate temperature

### Boundary Values
The heat flux along the panini height satisfies the von Neumann boundary condition as it is exposed to air, described as follows:

![Von Neumann Boundary Conditions](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/3.png)

Additional chicken-bread boundary conditions are as follows, but are not considered strictly as proper boundary conditions in the mathematical sense:

![Boundary Conditions](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/4.png)

## Numerical Method
The explicit finite difference numerical method is applied to solve the relevant heat diffusion equation, where the problem models 3 variables (2 in space, and 1 in time). Refer to the equation outlined under 'PDE Model'.

A summary of the major steps undertaken for the numerical method:

1. The panini is discretised into a matrix representing a mesh, where each element represents a node in the panini.
2. The code creates a null 3D array which can be thought of as a list of null matrices. Each matrix will be a snapshot of the panini at a point in time. 
3. Every element in the first matrix is then filled with the initial temperature value of 0 degrees Celsius (Frozen panini).
4. The code then checks the convergence of the numerical method and warns the user of any potential issues if they are detected.
5. The numerical method is then deployed for every time instance, first defining boundary conditions and then calculating all internal nodes with an explicit method.
6. The code then generates a coloured contour plot (heat map) of the final state of the panini, with dotted lines indicating the chicken-bread boundaries.
7. The code then begins the process of generating an animation of a heat map of the panini changing over time. 
8. Finally, a summary of the parameters is delivered to the user, and warnings are administered where necessary, such as when there is a poor temperature distribution, a risk of burning, or a still cold panini.

## Discretisation
With the substitutions ![T_xx](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/5.1.png), ![T_yy](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/5.2.png) and ![T_t](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/5.3.png), the heat diffusion equation becomes:

![Discretized Heat Diffusion Equation](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/6.png)

After additional manipulation, the heat diffusion equation can be generalised as follows:

![Generalized Heat Diffusion Equation](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/7.png)

Subscripts i,j correspond to spatial steps in x,y, and superscript t correspond to time step t.

A relationship between time step and mesh size for convergence can also be found as follows:

![Convergence Conditions](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/8.png)

### Discretisation of boundary conditions
As previously mentioned, four boundary conditions have been identified and are summarized as follows:

For the left-hand side of the panini:

![LHS Panini BC](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/9.png)

For the right-hand side of the panini:

![RHS Panini BC](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/9.1.png)

For bread nodes at the chicken-bread boundary:

![Chicken-Bread BC](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/9.2.png)

For chicken nodes at the chicken-bread boundary:

![Chicken Nodes BC](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/equations_img/9.3.png)

## Results
For raw animated videos of the heatmaps with time evolution, click on the following images to download the relevant mp4s, or navigate through the Results folder to find the relevant animated videos.

Corase mesh with h = 1 mm and k = 0.5 s:
[![coarse](https://j.gifs.com/K8m2lz.gif)](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/b2e951c14533c12fb95d07f3be3707f19bc6c037/Results/30s_coarse_mesh/panini.mp4)

Fine mesh with h = 1 mm and k = 0.5 s:

[![coarse](https://j.gifs.com/WPmlAX.gif)](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/Results/30s_fine_mesh/panini.mp4)

Animation capture for the above fine mesh:

<img src="https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/Results/30s_fine_mesh/vidcapfine.PNG?raw=true" />

## Additional Remarks
Refer to the [Explanation_Report.pdf](https://github.com/tszdabee/Panini-Heat-Diffusion-Modelling/blob/main/Explanation_Report.pdf) for further information. 
