import rospy
from geometry_msgs.msg import PoseStamped
import tf
import sys

# /cmd_vel geometry_msgs/Twist

PI =  3.1415


def main():
    pub = rospy.Publisher('/command/pose', PoseStamped, queue_size=10)
    rospy.init_node('pos_controller', anonymous=True)

    pos = PoseStamped()
    pos.pose.position.x = 70
    pos.pose.position.y = 0
    pos.pose.position.z = 0
    quaternion = tf.transformations.quaternion_from_euler(0, 0, 0)
    pos.pose.orientation.x = quaternion[0]
    pos.pose.orientation.y = quaternion[1]
    pos.pose.orientation.z = quaternion[2]
    pos.pose.orientation.w = quaternion[3]

    rospy.sleep(.5)

    for i in range(5):
        pub.publish(pos)
        rospy.sleep(.1)


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
