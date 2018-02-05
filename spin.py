import rospy
from geometry_msgs.msg import Twist
import sys

# /cmd_vel geometry_msgs/Twist


def spin(speed):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('rise', anonymous=True)

    spin_vel = Twist()
    spin_vel.angular.z = speed

    rospy.sleep(.5)

    pub.publish(spin_vel)


if __name__=='__main__':
    try:
        speed = float(sys.argv[1])
        spin(speed)
    except rospy.ROSInterruptException:
        pass
