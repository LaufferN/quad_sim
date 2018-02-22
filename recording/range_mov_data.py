import rospy
import tf

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan

def range_callback(data):
    global feature
    feature = data.ranges[60:-81]

def pos_callback(data):
    global position
    global angle
    global time
    time = data.header.stamp
    position = data.pose.position
    quaternion = data.pose.orientation 
    euler = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
    angle = euler

def main():
    rospy.Subscriber('scan', LaserScan, range_callback)
    rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, pos_callback)
    rospy.init_node('range_recording', anonymous=True)

    # let ros connect
    rospy.sleep(.5)

    camera_data = []

    action = "forward"
    file_name = "right_forward"
    file_append = 3
    with open("range_movement_data/" + file_name + "_" + str(file_append), "w") as f:
        # f.write("action, feature, offset, angle_offset, abs_x, abs_y, abs_angle, time")
        while not rospy.is_shutdown():
            abs_x = position.x
            abs_y = position.y
            abs_angle = angle[2]
            offset = abs_y
            angle_offset = abs_angle

            f.write("{0} {1} {2} {3} {4} {5} {6} {7} \n".format(action, feature, offset, angle_offset, abs_x, abs_y, abs_angle, time))
            rospy.sleep(.03)

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
