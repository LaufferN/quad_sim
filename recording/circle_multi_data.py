import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
import tf
import sys

# /cmd_vel geometry_msgs/Twist

feature = [0] * 940
position = [0] * 9
angle = [0] * 9
time = [0] * 9

def range_callback0(data):
    global feature
    feature[0] = data.ranges[60:-81]

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

def pos_callback8(data):
    global position
    global angle
    global time
    time[8] = data.header.stamp
    position[8] = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle[8] = euler

def forward():

    range_callbacks = [range_callback0,range_callback1,range_callback2,range_callback3,range_callback4,range_callback5,range_callback6,range_callback7,range_callback8]
    pos_callbacks = [pos_callback0,pos_callback1,pos_callback2,pos_callback3,pos_callback4,pos_callback5,pos_callback6,pos_callback7,pos_callback8]

    for i, range_callback, pos_callback in zip(range(9), range_callbacks, pos_callbacks):
        rospy.Subscriber('quad' + str(i) + '/scan', LaserScan, range_callback)
        rospy.Subscriber('quad' + str(i) + '/ground_truth_to_tf/pose', PoseStamped, pos_callback)

    rospy.init_node('range_recording', anonymous=True)

    pubs = []
    for i in range(9):
        pub = rospy.Publisher('quad' + str(i) + '/cmd_vel', Twist, queue_size=10)
        pubs.append(pub)
    
    forward = Twist()
    forward.linear.x = 1.5

    spin_left_forward = Twist()
    spin_left_forward.linear.x = 1.0
    spin_left_forward.angular.z = 0.5

    spin_right_forward = Twist()
    spin_right_forward.linear.x = 1.5
    spin_right_forward.angular.z = -0.4

    still = Twist()

    times = [3.0, 8.0, 5.5, 12.0, 0.0]
    actions = [forward, spin_left_forward, forward, spin_right_forward, still]
    action_strs = ["forward", "left", "forward", "right", "still"]

    rospy.sleep(.5)

    fs = []
    for i in range(9):
        fs.append(open("range_movement_data/new_data_" + str(i), "w"))

    for time, action, action_str in zip(times, actions, action_strs):
        [pub.publish(action) for pub in pubs]
        start_time = rospy.get_time()
        while rospy.get_time() < start_time + time:
            for i in range(9): 
                f = fs[i]
                abs_x = position[i].x
                abs_y = position[i].y
                abs_angle = angle[i][2]
                offset = abs_y  
                angle_offset = abs_angle
                current_feature = feature[i]
                current_time = time

                f.write("{0} {1} {2} {3} {4} {5} {6} {7} \n".format(action_str, current_feature, offset, angle_offset, abs_x, abs_y, abs_angle, current_time))
            rospy.sleep(.03)

    for f in fs:
        f.close()


if __name__=='__main__':
    try:
        forward()
    except rospy.ROSInterruptException:
        pass
