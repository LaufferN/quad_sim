import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import numpy as np
import csv
from sklearn import svm

# /cmd_vel geometry_msgs/Twist



vector_len = 940
path = "recording/laser_scan_data_forest/"

class_str_map = {'middle_left': 0, 'middle_middle': 1, 'middle_right': 2}

training_data = []
training_labels = []
file_names = ['middle_left', 'middle_middle', 'middle_right']
for file_name in file_names:
    with open(path + file_name) as f:
        for line in f:
            data = map(float, line.split(', '))
            training_data.append(data)
            training_labels.append(class_str_map[file_name])

# "one-vs-all" multi-class strategy
clf = svm.LinearSVC(verbose=True) 
print(clf.fit(training_data, training_labels))


def classifier(xData):
    prediction = clf.predict([xData])
    return prediction[0] # because predict returns a 2D array

forward = Twist()
forward.linear.x = 3.0

left = Twist()
left.linear.x = 1.5
left.angular.z = 0.4

right = Twist()
right.linear.x = 1.5
right.angular.z = -.4

actions = [right, forward, left]
movements = ["right", "forward", "left"]

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


        classification = classifier(feature)

        # print(mode_classification)

        if classification == -1:
            print("classification is -1")

        action = actions[classification]
        print("Going " + movements[classification])

        pub.publish(action)

        rospy.sleep(.05)

        # rospy.spin()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
