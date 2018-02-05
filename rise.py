import rospy
from geometry_msgs.msg import Twist

# /cmd_vel geometry_msgs/Twist


def rise():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('rise', anonymous=True)

    up_vel = Twist()
    up_vel.linear.z = 2.0

    rospy.sleep(.5)

    still = Twist()
    pub.publish(up_vel)

    rospy.sleep(7.0)
    pub.publish(still)


if __name__=='__main__':
    try:
        rise()
    except rospy.ROSInterruptException:
        pass
