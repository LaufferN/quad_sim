import numpy as np
import math
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read data
path = "../recording/range_movement_data/"
file_names = ["new_data_0_clean", "new_data_1_clean", "new_data_2_clean", "new_data_3_clean", "new_data_4_clean", "new_data_5_clean", "new_data_6_clean", "new_data_7_clean", "new_data_8_clean"]
feature_list = [] 
offset_list = []
angle_offset_list = []
for file_name in file_names:
    with open(path + file_name) as f:
        for line in f:
            # action feature offset angle_offset abs_x abs_y abs_angle time
            line_list = line.split(" ")
            feature = map(float, line_list[1].split(","))
            assert(len(feature) == 940)
            offset = float(line_list[2])
            angle_offset = float(line_list[3])
            feature_list.append(np.asarray(feature))
            offset_list.append(offset)
            angle_offset_list.append(angle_offset)


pca = PCA(n_components = 3)
feature_list = np.asarray(feature_list)
feature_list_reduced = pca.fit_transform(feature_list)

offsets_graph = []
a_offsets_graph = []
offset_norm_graph = []
a_offset_norm_graph = []
inner_product_graph = []
step = 2
for i in range(0, len(feature_list_reduced) - step, step):
    feature_diff = feature_list_reduced[i+step] - feature_list_reduced[i]
    offset_diff = offset_list[i+step] - offset_list[i]
    angle_offset_diff = angle_offset_list[i+step] - angle_offset_list[i]

    offset_norm = np.linalg.norm(feature_diff/offset_diff)
    a_offset_norm = np.linalg.norm(feature_diff/angle_offset_diff)
    if (offset_norm < 1000000 and a_offset_norm < 1000000) or True:
        offsets_graph.append(offset_list[i])
        a_offsets_graph.append(angle_offset_list[i])
        # norms
        offset_norm_graph.append(math.log(offset_norm))
        a_offset_norm_graph.append(math.log(a_offset_norm))
        # inner product
        inner_product = (feature_diff/offset_diff).dot(feature_diff/angle_offset_diff)
        sign = np.sign(inner_product)
        inner_product_graph.append(sign * math.log(abs(inner_product)))


fig1 = plt.figure()
plot1 = fig1.add_subplot(111, projection='3d')
plot1.scatter(offsets_graph, a_offsets_graph, offset_norm_graph)

plot1.set_xlabel('Offset')
plot1.set_ylabel('Angle')
plot1.set_zlabel("Offset' Norm")
# plot1.set_yscale('log')

fig2 = plt.figure()
plot2 = fig2.add_subplot(111, projection='3d')
plot2.scatter(offsets_graph, a_offsets_graph, a_offset_norm_graph)

plot2.set_xlabel('Offset')
plot2.set_ylabel('Angle')
plot2.set_zlabel("Angle' Norm")
# plot2.set_yscale('log')

fig3 = plt.figure()
plot3 = fig3.add_subplot(111, projection='3d')
plot3.scatter(offsets_graph, a_offsets_graph, inner_product_graph)

plot3.set_xlabel('Offset')
plot3.set_ylabel('Angle')
plot3.set_zlabel("Inner Product Norm")
# plot3.set_yscale('log')

fig1.show()
fig2.show()
fig3.show()
raw_input("")


