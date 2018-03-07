import numpy as np
import math
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PI = 3.1415

def sign_log(value):
    sign = np.sign(value)
    return sign * math.log(abs(value))

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
            if angle_offset < -1.5:
                angle_offset += PI
            feature_list.append(np.asarray(feature))
            offset_list.append(offset)
            angle_offset_list.append(angle_offset)


pca = PCA(n_components = 3)
feature_list = np.asarray(feature_list)
feature_list_reduced = pca.fit_transform(feature_list)

offsets_graph = []
a_offsets_graph = []
comp1_offset_graph = []
comp2_offset_graph = []
comp3_offset_graph = []
comp1_angle_graph = []
comp2_angle_graph = []
comp3_angle_graph = []
step = 2
for i in range(0, len(feature_list_reduced) - step, step):
    feature_diff = feature_list_reduced[i+step] - feature_list_reduced[i]
    offset_diff = offset_list[i+step] - offset_list[i]
    angle_offset_diff = angle_offset_list[i+step] - angle_offset_list[i]

    if True:
        offsets_graph.append(offset_list[i])
        a_offsets_graph.append(angle_offset_list[i])
        # pca component differences
        comp1_offset_graph.append(sign_log(feature_diff[0]/offset_diff))
        comp2_offset_graph.append(sign_log(feature_diff[1]/offset_diff))
        comp3_offset_graph.append(sign_log(feature_diff[2]/offset_diff))
        comp1_angle_graph.append(sign_log(feature_diff[0]/angle_offset_diff))
        comp2_angle_graph.append(sign_log(feature_diff[1]/angle_offset_diff))
        comp3_angle_graph.append(sign_log(feature_diff[2]/angle_offset_diff))


fig1 = plt.figure()
plot1 = fig1.add_subplot(111, projection='3d')
plot1.scatter(offsets_graph, a_offsets_graph, comp1_offset_graph)

plot1.set_xlabel('Offset')
plot1.set_ylabel('Angle')
plot1.set_zlabel("PCA Component 1 wrt Offset")
# plot1.set_yscale('log')

fig4 = plt.figure()
plot4 = fig4.add_subplot(111, projection='3d')
plot4.scatter(offsets_graph, a_offsets_graph, comp1_angle_graph)

plot4.set_xlabel('Offset')
plot4.set_ylabel('Angle')
plot4.set_zlabel("PCA Component 1 wrt Angle")
# plot4.set_yscale('log')

fig2 = plt.figure()
plot2 = fig2.add_subplot(111, projection='3d')
plot2.scatter(offsets_graph, a_offsets_graph, comp2_offset_graph)

plot2.set_xlabel('Offset')
plot2.set_ylabel('Angle')
plot2.set_zlabel("PCA Component 2 wrt Offset")
# plot2.set_yscale('log')

fig5 = plt.figure()
plot5 = fig5.add_subplot(111, projection='3d')
plot5.scatter(offsets_graph, a_offsets_graph, comp2_angle_graph)

plot5.set_xlabel('Offset')
plot5.set_ylabel('Angle')
plot5.set_zlabel("PCA Component 2 wrt Angle")
# plot5.set_yscale('log')

fig3 = plt.figure()
plot3 = fig3.add_subplot(111, projection='3d')
plot3.scatter(offsets_graph, a_offsets_graph, comp3_offset_graph)

plot3.set_xlabel('Offset')
plot3.set_ylabel('Angle')
plot3.set_zlabel("PCA Component 3 wrt Offset")
# plot3.set_yscale('log')

fig6 = plt.figure()
plot6 = fig6.add_subplot(111, projection='3d')
plot6.scatter(offsets_graph, a_offsets_graph, comp3_angle_graph)

plot6.set_xlabel('Offset')
plot6.set_ylabel('Angle')
plot6.set_zlabel("PCA Component 3 wrt Angle")
# plot6.set_yscale('log')

fig1.show()
fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig6.show()
raw_input("")


