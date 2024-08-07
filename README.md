# Ring-Lattice-Visualization---Accelerator-Physics

This python script creates a ring visualization for accelerator physics. It is a simple python script, that bends the main trajectory based on the bending angle of the dipoles.
The elements are placed as rectangles on the main trajectory. The script, takes in as Mad-X type input with defined classes.

Only elements that are included in the script are:
  - Solenoid
  - Quadrupole
  - Dipoles

It is straight forward to add other elements such as, Sextupoles, Octopoles and so on since they do not have any bending included, it will be similar to that quadrupole and solenoid part of the script.


## Usage

Usage of the script is pretty straightforward!
Define the elements:
``` python
DD = Drift(l=0.5*scale_factor)

Q00 = Quad(l=0.2*scale_factor)
Q01 = Quad(l=0.2*scale_factor)
Q02 = Quad(l=0.2*scale_factor)
Q03 = Quad(l=0.2*scale_factor)
MB = Dipole(l=1.0*scale_factor,  angle= 20.0) ## Angle in degrees

CELL = [DD,Q00,DD,Q01,DD,MB,DD,Q02,DD,Q03,DD] ## Array type cell

extended_cells = CELL * 18 ## For ring, 18*20 = 360 bending!
```

It also visualizes, straight sections as well which can be added as above just make sure to append to the main array.
