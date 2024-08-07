## Python file for visualizing Ring Geometry
## This file can be manipulated to add different elements as well
## The toughest part was in the dipoles to bend the trajectory and element placement, but other elements such as:
## Sextupoles, Octopoles can be added similar fashion way as in Quadrupoles.
## Currently included:
##      - Solenoids
##      - Quadrupoles
##      - Dipoles
## This python script can plot an accelerator ring lattice for visualizing the ring with elements.
## By defining a MAD-X like structure, Classes and Line element like cells, one can plot the ring visualization.
## Author: OluckyG
## Date: 08/07/2024


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
## Defining Classes like Elements for Mad-X like structure
class Quad:
    def __init__(self, l):
        self.l = l
    def lelement(self):
        return self.l

class Solenoid:
    def __init__(self, l):
        self.l = l

    def lelement(self):
        return self.l

class Dipole:
    def __init__(self, l, angle):
        self.l = l
        self.angle = angle

    def lelement(self):
        return self.l, (self.angle * np.pi / 180)

class Drift:
    def __init__(self, l):
        self.l = l

    def lelement(self):
        return self.l

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12,9))

# Initial position and global angle
position = np.array([0.0, 0.0])
global_angle = 0.0  # Initial orientation (in radians)

# Define scale factor
scale_factor = 0.05

# Define elements
DD = Drift(l=0.5*scale_factor)
Q00 = Quad(l=0.2*scale_factor)
Q01 = Quad(l=0.2*scale_factor)
Q02 = Quad(l=0.2*scale_factor)
Q03 = Quad(l=0.2*scale_factor)
MB = Dipole(l=1.0*scale_factor,angle=20.0)
## Periodic cell
element_array = [DD,Q00,DD,Q01,DD,MB,DD,Q02,DD,Q03,DD]
## Full ring array
extended_TEST = element_array * 18

# Visualization loop
for element in extended_TEST:
    if isinstance(element, Drift): ## Checking for Drifts
        length = element.lelement()
        dx = length * np.cos(global_angle)
        dy = length * np.sin(global_angle)
        ax.plot([position[0], position[0] + dx], [position[1], position[1] + dy], 'k-')
        position[0] += dx
        position[1] += dy

    elif isinstance(element, (Solenoid, Quad)):
        length = element.lelement()
        dx = length * np.cos(global_angle)
        dy = length * np.sin(global_angle)
        ax.plot([position[0], position[0] + dx], [position[1], position[1] + dy], 'k-')
        
        # Center the rectangle on the trajectory line
        rect_center_x = position[0] + dx / 2
        rect_center_y = position[1] + dy / 2
        rect_width = length
        rect_height = 0.1  # Set height of the rectangle
        
        # Calculate bottom-left corner based on the center
        bottom_left_x = rect_center_x - rect_width / 2 * np.cos(global_angle) + rect_height / 2 * np.sin(global_angle)
        bottom_left_y = rect_center_y - rect_width / 2 * np.sin(global_angle) - rect_height / 2 * np.cos(global_angle)

        # Draw the rectangle with its center on the trajectory
        rect = patches.Rectangle(
            (bottom_left_x, bottom_left_y), 
            rect_width, rect_height, angle=np.degrees(global_angle), facecolor="red", edgecolor="black"
        )
        ax.add_patch(rect)
        
        position[0] += dx
        position[1] += dy

    elif isinstance(element, Dipole):
        length, total_angle = element.lelement()
        half_length = length / 2
        half_angle = total_angle / 2

        # First half of the dipole (straight)
        dx1 = half_length * np.cos(global_angle)
        dy1 = half_length * np.sin(global_angle)
        ax.plot([position[0], position[0] + dx1], [position[1], position[1] + dy1], 'k-')
        position[0] += dx1
        position[1] += dy1

        # Bend by half the total angle
        global_angle += half_angle

        # Second half of the dipole (straight)
        dx2 = half_length * np.cos(global_angle)
        dy2 = half_length * np.sin(global_angle)
        ax.plot([position[0], position[0] + dx2], [position[1], position[1] + dy2], 'k-')

        # Update position
        position[0] += dx2
        position[1] += dy2

        # Rectangle placement for dipole
        # Since the rectangle is centered, we need to find the midpoint
        rect_center_x = position[0] - dx2 / 2
        rect_center_y = position[1] - dy2 / 2
        rect_width = length
        rect_height = 0.1  # Set height of the rectangle

        # Calculate bottom-left corner based on the center
        bottom_left_x = rect_center_x - rect_width / 2 * np.cos(global_angle) + rect_height / 2 * np.sin(global_angle)
        bottom_left_y = rect_center_y - rect_width / 2 * np.sin(global_angle) - rect_height / 2 * np.cos(global_angle)

        # Draw the rectangle with its center on the trajectory
        diprect = patches.Rectangle(
            (bottom_left_x, bottom_left_y), 
            rect_width, rect_height, angle=np.degrees(global_angle), facecolor="blue", edgecolor="black"
        )
        ax.add_patch(diprect)

        # Complete the remaining half of the bend
        global_angle += half_angle

        # Ensure sufficient space between dipole and next element
        additional_dx = half_length * np.cos(global_angle)
        additional_dy = half_length * np.sin(global_angle)
        ax.plot([position[0], position[0] + additional_dx], [position[1], position[1] + additional_dy], 'k-')
        position[0] += additional_dx
        position[1] += additional_dy

# Create representative rectangles for the legend
legend_elements = [
    patches.Patch(facecolor='red', edgecolor='black', label='Quadrupole'),
    patches.Patch(facecolor='blue', edgecolor='black', label='Dipole')
]

# Add the legend
ax.legend(handles=legend_elements,loc="upper right",fontsize=15)

# Set the aspect ratio and limits
ax.set_aspect('equal')
ax.set_xlim(-1.3,1.3)
ax.set_ylim(-0.1, 1.8)

# Remove axis labels and ticks
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')

# Display the plot
plt.show()
# plt.savefig("QuadrupoledoubletRingVisualization.png")

