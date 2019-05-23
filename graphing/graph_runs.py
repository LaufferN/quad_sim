import matplotlib.pyplot as plt

# paths = [ '../run_1_rise_4/', '../run_1_rise_5/', '../run_2_rise_5/', '../run_2_rise_4/','../run_1_rise_6/','../run_2_rise_6/', ]
# paths = ['../recorded_runs/run_1_rise_5/', '../recorded_runs/run_2_rise_5/', '../recorded_runs/run_1_rise_6/', '../recorded_runs/run_2_rise_6/', '../recorded_runs/run_1_rise_8/', '../recorded_runs/run_2_rise_8/', '../recorded_runs/run_1_rise_10/', '../recorded_runs/run_2_rise_10/']
path = '../recorded_runs/gradient_runs/dec_2018_good/'
PI = 3.1415
widths = [int(float(i)/2.0)+1 for i in range(100)]
num_quads = 1

for width, rel_path in zip(widths, range(num_quads)):
    offsets = []
    with open(path + str(rel_path) + '/y_offset', 'r') as in_offsets:
        for o in in_offsets:
            offsets.append(float(o))

    yaws = []
    with open(path + str(rel_path) + '/yaw', 'r') as in_yaws:
        for y in in_yaws:
            yaws.append(float(y) )

    actions = []
    with open(path + str(rel_path) + '/action', 'r') as in_actions:
        for a in in_actions:
            actions.append(a[:-1])
    actions.append('end')

    min_len = min([len(offsets), len(yaws), len(actions)])
    offsets = offsets[:min_len]
    yaws = yaws[:min_len]
    actions = actions[:min_len]

    colors = {'forward': 'blue','forward (with b=4)': 'blue', 'left': 'red', 'right': 'green'}

    prev_i = 0
    for i in range(len(actions)-1):
        if actions[i] != actions[i+1]:
            plt.plot(yaws[prev_i:i+1], offsets[prev_i:i+1], c=colors[actions[i]], linewidth=width)
            prev_i = i

plt.show()
