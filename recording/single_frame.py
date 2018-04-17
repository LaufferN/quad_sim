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

def main():

    range_callbacks = [range_callback0,range_callback1,range_callback2,range_callback3,range_callback4,range_callback5,range_callback6,range_callback7,range_callback8]

    for i, range_callback in zip(range(9), range_callbacks):
        rospy.Subscriber('quad' + str(i) + '/scan', LaserScan, range_callback)

    rospy.init_node('range_recording', anonymous=True)

    rospy.sleep(1)

    with open("/home/niklas/code/hector_quad/recording/temp", "w") as f:
        f.write("(offset, angle): (0, -PI/4) (2, -PI/4) (-2, -PI/4) (0, 0) (2, 0) (-2, 0) (0, PI/4) (2, PI/4) (-2, PI/4) \n")
        for i in range(9):
            f.write(str(feature[i])[1:-1])
            f.write("\n")


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
