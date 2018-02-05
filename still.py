import rospy
from geometry_msgs.msg import Twist

# /cmd_vel geometry_msgs/Twist


def rise():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('rise', anonymous=True)

    rospy.sleep(.5)

    still = Twist()
    pub.publish(still)

if __name__=='__main__':
    try:
        rise()
    except rospy.ROSInterruptException:
        pass
