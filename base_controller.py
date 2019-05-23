import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import numpy as np
import csv

# /cmd_vel geometry_msgs/Twist



# path = "recording/classifs/OldAndNewClassifiers_16Mar18/new/" #"classif/4" is the best
# path = "recording/classifs/OldAndNewClassifiers_16Mar18/plain/" #"classif/4" is the best
# path = "recording/classifs/old_classifier_20mar/" #"classif/4" is the best
path = "recording/classifs/4/" #"classif/4" is the best
vector_len = 940


control_classif = {'w': [np.empty([1, vector_len]), np.empty([1, vector_len]), np.empty([1, vector_len])], 'b': []}

with open(path + 'class1w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][0][0][i] = float(value[0])

with open(path + 'class2w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][1][0][i] = float(value[0])

with open(path + 'class3w.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['w'][2][0][i] = float(value[0])

with open(path + 'class1b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))

with open(path + 'class2b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))

with open(path + 'class3b.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for value, i in zip(reader, range(vector_len)):
        control_classif['b'].append(float(value[0]))


def classifier(xData, classifs, mode):

    # margvec(i) = classifs{i}.w'*xData'+classifs{i}.b;
    # classvec(i) = sign(classifs{i}.w'*xData'+classifs{i}.b);

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
    if mode == 1:
        if (classvec[0] > 0 and classvec[2] > 0): # minind[0] == 1
            labB = 1
        elif (classvec[0] < 0 and classvec[1] > 0): # minind[0] == 2
            labB = 2
        elif (classvec[1] < 0 and classvec[2] < 0): # minind[0] == 3
            labB = 3
    elif mode == 2:
        if classvec[2] < 0:
            labB = 3
        else:
            if classvec[0] < 0:
                labB = 2
            else:
                labB = 1
    else:
        print("invalid mode!")

    return labB

forward = Twist()
forward.linear.x = 3.0

left = Twist()
left.linear.x = 1.5
left.angular.z = 0.4

right = Twist()
right.linear.x = 1.5
right.angular.z = -.4

actions = [forward, right, left]
# actions = [left, forward, right]
movements = ["forward", "right", "left"]

feature = LaserScan().ranges[60:-81]

def feature_callback(data):
    global feature
    feature = data.ranges[60:-81]

def main():
    pub = rospy.Publisher('quad0/cmd_vel', Twist, queue_size=10)
    rospy.init_node('base_controller', anonymous=True)
    rospy.Subscriber('quad0/scan', LaserScan, feature_callback)

    rospy.sleep(.5) # let ros finish connecting

    done = False
    while not done and not rospy.is_shutdown():


        classification = classifier(feature, control_classif, mode=1)

        # print(mode_classification)

        if classification == -1:
            print("classification is -1")

        action = actions[classification-1]
        print("Going " + movements[classification-1])

        pub.publish(action)

        rospy.sleep(.05)

        # rospy.spin()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
