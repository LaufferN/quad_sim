import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
import tf

import numpy as np
import csv

# /cmd_vel geometry_msgs/Twist



path = "classifs/dec_2018_classif_gradient/" #"classif/4" is the best
prefix = "dec18GOOD"
vector_len = 839
num_quads = 1


control_classif = {'w': [np.empty([1, vector_len]), np.empty([1, vector_len]), np.empty([1, vector_len])], 'b': []}

with open(path + prefix + 'class1w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][0][0][i] = float(value[0])

with open(path + prefix + 'class2w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][1][0][i] = float(value[0])

with open(path + prefix + 'class3w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][2][0][i] = float(value[0])

with open(path + prefix + 'class1b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))

with open(path + prefix + 'class2b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))

with open(path + prefix + 'class3b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))

def classifier(xData, classifs, mode):


    ### truth table
    # 1 vs 2    1   -1   ? 
    # 2 vs 3    ?    1   -1 
    # 1 vs 3    1    ?   -1
    classvec = []
    margvec = []
    for i in range(3):
        margvec.append(classifs['w'][i][0].dot(xData) + classifs['b'][i])
        classvec.append(np.sign(classifs['w'][i][0].dot(xData) + classifs['b'][i]))
                                 

    labB = 1
    # if mode == 1:
    #     if (classvec[0] <= 0 and classvec[1] <= 0): # minind[0] == 1
    #         labB = 1
    #     elif (classvec[0] > 0 and classvec[2] > 0): # minind[0] == 2
    #         labB = 2
    #     elif (classvec[1] > 0 and classvec[2] < 0): # minind[0] == 3
    #         labB = 3
    #     else:
    #         labB = 4
    # else:
    #     print("invalid mode!")

    if mode == 1:
        if (classvec[0] <= 0 and classvec[1] > 0): 
            labB = 1
        elif (classvec[2] > 0):
            labB = 2
        else: 
            labB = 3
    else:
        print("invalid mode!")

    return labB

forward = Twist()
forward.linear.x = 1.0

left = Twist()
left.angular.z = 0.2

right = Twist()
right.angular.z = -.2

movements = [forward, right, left, forward]
movements_str = ["forward", "right", "left", "forward (with b=4)"]

position = PoseStamped().pose.position
angle = [0]*3

feature = [[0]*839]*9
time = [[]]*9
position = [[]]*9
angle = [[]]*9



def range_callback0(data):
    global feature
    feature[0] = data.ranges[60:-81]
    feature[0] = feature[0][60:-41]

def pos_callback0(data):
    global position
    global angle
    global time
    time[0] = data.header.stamp
    position[0] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[0] = euler

def range_callback1(data):
    global feature
    feature[1] = data.ranges[60:-81]
    feature[1] = feature[1][60:-41]

def pos_callback1(data):
    global position
    global angle
    global time
    time[1] = data.header.stamp
    position[1] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[1] = euler

def range_callback2(data):
    global feature
    feature[2] = data.ranges[60:-81]
    feature[2] = feature[2][60:-41]

def pos_callback2(data):
    global position
    global angle
    global time
    time[2] = data.header.stamp
    position[2] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[2] = euler

def range_callback3(data):
    global feature
    feature[3] = data.ranges[60:-81]
    feature[3] = feature[3][60:-41]

def pos_callback3(data):
    global position
    global angle
    global time
    time[3] = data.header.stamp
    position[3] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[3] = euler

def range_callback4(data):
    global feature
    feature[4] = data.ranges[60:-81]
    feature[4] = feature[4][60:-41]

def pos_callback4(data):
    global position
    global angle
    global time
    time[4] = data.header.stamp
    position[4] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[4] = euler

def range_callback5(data):
    global feature
    feature[5] = data.ranges[60:-81]
    feature[5] = feature[5][60:-41]

def pos_callback5(data):
    global position
    global angle
    global time
    time[5] = data.header.stamp
    position[5] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[5] = euler

def range_callback6(data):
    global feature
    feature[6] = data.ranges[60:-81]
    feature[6] = feature[6][60:-41]

def pos_callback6(data):
    global position
    global angle
    global time
    time[6] = data.header.stamp
    position[6] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[6] = euler

def range_callback7(data):
    global feature
    feature[7] = data.ranges[60:-81]
    feature[7] = feature[7][60:-41]

def pos_callback7(data):
    global position
    global angle
    global time
    time[7] = data.header.stamp
    position[7] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[7] = euler

def range_callback8(data):
    global feature
    feature[8] = data.ranges[60:-81]
    feature[8] = feature[8][60:-41]

def pos_callback8(data):
    global position
    global angle
    global time
    time[8] = data.header.stamp
    position[8] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[8] = euler

def main():
    rospy.init_node('recording_runs', anonymous=True)

    range_callbacks = [range_callback0,range_callback1,range_callback2,range_callback3,range_callback4,range_callback5,range_callback6,range_callback7,range_callback8]
    pos_callbacks = [pos_callback0,pos_callback1,pos_callback2,pos_callback3,pos_callback4,pos_callback5,pos_callback6,pos_callback7,pos_callback8]

    for i, range_callback, pos_callback in zip(range(num_quads), range_callbacks, pos_callbacks):
        rospy.Subscriber('quad' + str(i) + '/scan', LaserScan, range_callback)
        rospy.Subscriber('quad' + str(i) + '/ground_truth_to_tf/pose', PoseStamped, pos_callback)

    pubs = []
    for i in range(num_quads):
        pub = rospy.Publisher('quad' + str(i) + '/cmd_vel', Twist, queue_size=10)
        pubs.append(pub)

    rospy.sleep(.5) # let ros finish connecting

    # readings
    features = [[], [], [], [], [], [], [], [], []]
    mode_classifs = [[], [], [], [], [], [], [], [], []]
    actions = [[], [], [], [], [], [], [], [], []]
    y_offsets = [[], [], [], [], [], [], [], [], []]
    yaws = [[], [], [], [], [], [], [], [], []]
    
    global feature
    global position
    global angle

    done = False
    max_y_offset = 0
    while not done and not rospy.is_shutdown() and max_y_offset < 15:

        for i in range(num_quads):

            feature_reading = feature[i]

            num_50 = 0
            # should only happen if the quad has reached the end of the valley
            for reading in feature_reading:
                if reading == 50.0:
                    num_50 += 1

            if num_50 > 2:
                done = True
                break

            features[i].append(feature_reading)
            y_offsets[i].append(position[i].y)
            if abs(position[i].y) > abs(max_y_offset):
                max_y_offset = abs(position[i].y)
            yaws[i].append(angle[i][2]) # for yaw

            classification = classifier(feature_reading, control_classif, mode=1)
            mode_classification = classification

            if classification == -1:
                print("classification is -1")

            action = movements[classification-1]
            action_str = movements_str[classification-1]
            actions[i].append(action_str)
            mode_classifs[i].append(mode_classification)

            pubs[i].publish(action)
            # print("publishing " + str(action_str))

            rospy.sleep(.001)


    for i in range(num_quads):
        # write data to file
        direc = '/home/niklas/code/hector_quad/recorded_runs/gradient_runs/dec_2018_good/'
        out_feature = open(direc + str(i) + '/feature', 'w')
        out_classif = open(direc + str(i) + '/classif', 'w')
        out_action = open(direc + str(i) + '/action', 'w')
        out_y_offset = open(direc + str(i) + '/y_offset', 'w')
        out_yaws = open(direc + str(i) + '/yaw', 'w')
        out_height = open(direc + str(i) + '/height', 'w')
        for feature, classif, action, y_offset, yaw in zip(features[i],mode_classifs[i],actions[i],y_offsets[i],yaws[i]):
            out_feature.write(str(feature)[1:-1] + '\n')
            out_classif.write(str(classif) + '\n')
            out_action.write(str(action) + '\n')
            out_y_offset.write(str(y_offset) + '\n')
            out_yaws.write(str(yaw) + '\n')

        out_feature.close()
        out_classif.close()
        out_action.close()
        out_y_offset.close()
        out_yaws.close()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
