from scipy import interpolate
import numpy as np
import itertools
import matplotlib.pyplot as plt

def polyval2d(x, y, m):
    order = int(np.sqrt(len(m))) - 1
    ij = itertools.product(range(order+1), range(order+1))
    z = np.zeros_like(x)
    for a, (i,j) in zip(m, ij):
        z += a * x**i * y**j
    return z

def polyfit2d(x, y, z, order=2):
    ncols = (order + 1)**2
    G = np.zeros((x.size, ncols))
    ij = itertools.product(range(order+1), range(order+1))
    for k, (i,j) in enumerate(ij):
        G[:,k] = x**i * y**j
    m, _, _, _ = np.linalg.lstsq(G, z)
    return m

# (offset, angle): (0, -PI/4) (2, -PI/4) (-2, -PI/4) (0, 0) (2, 0) (-2, 0) (0, PI/4) (2, PI/4) (-2, PI/4) 
PI = 3.1415
xs = np.array([0, 2, -2, 0, 2, -2, 0, 2, -2])
ys = np.array([-PI/4, -PI/4, -PI/4, 0, 0, 0, PI/4, PI/4, PI/4])

zs = []

with open('data', 'r') as f:
    for i, line in zip(range(9), f):
        line_list = map(float, line.split(", "))
        zs.append(line_list)

zs = np.asarray(zs)
zs_ = zs.T

f_approx = []
for i in range(len(zs)):
    f_approx.append(polyfit2d(xs, ys, zs_[i]))

print(f_approx[0])


# nx, ny = 20, 20
# xx, yy = np.meshgrid(np.linspace(xs.min(), xs.max(), nx), 
#                              np.linspace(ys.min(), ys.max(), ny))
# zz = polyval2d(xx, yy, m)

# # Plot
# plt.imshow(zz, extent=(xs.min(), ys.max(), xs.max(), ys.min()))
# plt.scatter(xs, ys, c=zs/zs.max())
# plt.show()

# # f = interpolate.interp2d(xs, ys, zs_[0], kx=2, ky=2)


