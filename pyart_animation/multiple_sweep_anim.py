# Reading a radar netcdf file and taking all sweeps and creating a animation.
import numpy as np
import pyart
from matplotlib import pyplot as plt
from matplotlib import animation

# Read file with pyart, file location and name.
radar = pyart.io.read(
    '/home/zsherman/training_exercises/data/KLOT20130417_235520_V06.gz')

# Create a radar object for each sweep.
radars = []
for i in range(len(radar.sweep_number['data'])):
    sweep_number = radar.sweep_number['data'][i]
    one_sweep = radar.extract_sweeps([sweep_number])
    radars += [one_sweep]

# Create a plot for each sweep, and have each plot be a frame.
def animate(nframe):
    plt.clf()
    display = pyart.graph.RadarMapDisplay(radars[nframe])
    display.plot_ppi_map('reflectivity', resolution='l',
                         vmin=-8, vmax=64, mask_outside=False,
                         cmap=pyart.graph.cm.NWSRef,
                         lat_lines=None, lon_lines=None)
    display.basemap.drawcounties()

fig = plt.figure(figsize=(10, 8))
anim = animation.FuncAnimation(fig, animate, frames=len(radars))
anim.save('klot_reflectivity_animation.gif',
          writer='imagemagick', fps=2)
# Delete radars to conserve memory.
del radars
plt.close()
