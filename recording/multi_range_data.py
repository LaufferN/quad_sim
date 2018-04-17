import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
import tf
import sys

# /cmd_vel geometry_msgs/Twist

feature = [0] * 940

def range_callback0(data):
    global feature
    feature[0] = data.ranges[60:-81]

def range_callback1(data):
    global feature
    feature[1] = data.ranges[60:-81]

def range_callback2(data):
    global feature
    feature[2] = data.ranges[60:-81]

def range_callback3(data):
    global feature
    feature[3] = data.ranges[60:-81]

def range_callback4(data):
    global feature
    feature[4] = data.ranges[60:-81]

def range_callback5(data):
    global feature
    feature[5] = data.ranges[60:-81]

def range_callback6(data):
    global feature
    feature[6] = data.ranges[60:-81]

def range_callback7(data):
    global feature
    feature[7] = data.ranges[60:-81]

def range_callback8(data):
    global feature
    feature[8] = data.ranges[60:-81]


def forward():

    range_callbacks = [range_callback0,range_callback1,range_callback2,range_callback3,range_callback4,range_callback5,range_callback6,range_callback7,range_callback8]

    for i, range_callback in zip(range(9), range_callbacks):
        rospy.Subscriber('quad' + str(i) + '/scan', LaserScan, range_callback)

    rospy.init_node('range_recording', anonymous=True)

    rospy.sleep(.5)

    f_names = ["middle_right", "left_right", "right_right", "middle_middle", "left_middle", "right_middle", "middle_left", "left_left", "right_left"]

    fs = []
    for i in f_names:
        fs.append(open("training_data2/" + str(i), "w"))

    while not rospy.is_shutdown():
        for i in range(9): 
            current_feature = feature[i]
            fs[i].write(str(current_feature)[1:-1] + "\n")
        rospy.sleep(.03)

    for f in fs:
        f.close()


if __name__=='__main__':
    try:
        forward()
    except rospy.ROSInterruptException:
        pass

