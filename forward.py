import rospy
from geometry_msgs.msg import Twist
import sys

# /cmd_vel geometry_msgs/Twist


def forward(speed):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('rise', anonymous=True)

    forward = Twist()
    forward.linear.x = speed

    rospy.sleep(.5)

    pub.publish(forward)


if __name__=='__main__':
    try:
        speed = float(sys.argv[1])
        forward(speed)
    except rospy.ROSInterruptException:
        pass
