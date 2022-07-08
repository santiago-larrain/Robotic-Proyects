#------------------------------------------------------------------------------#
# Plot ellipsoid
#
#  x^2/a^2 + y^2/b^2 + z^2/c^2 = 1
#
# See also:
# https://stackoverflow.com/questions/7819498/plotting-ellipsoid-with-matplotlib
#
# execute typing: python ellipsoid.py
# Miguel Torres Torriti
# 2018.03.22

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def ellipsoid(rx, ry, rz):
    # Compute spherical angles:
    u = np.linspace(0, 2 * np.pi, 100) # Azimut
    v = np.linspace(0, np.pi, 100)     # Inclination = pi/2 - Elevation 

    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z
    
def plot_ellipsoid(x, y, z, max_radius):
    fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')

    # Adjustment of the axes, so that they all have the same span:
    
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

    plt.show()

def main():
    rx = 2.0
    ry = 1.0
    rz = 0.5
    
    x, y, z = ellipsoid(rx, ry, rz)
    max_radius =  max(rx, ry, rz)
    plot_ellipsoid(x, y, z, max_radius)
    
if __name__ == '__main__': main()
  