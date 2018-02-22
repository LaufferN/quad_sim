import rospy
from geometry_msgs.msg import Twist

# /cmd_vel geometry_msgs/Twist


def rise():
    pubs = []
    for i in range(9):
        pub = rospy.Publisher('quad' + str(i) + '/cmd_vel', Twist, queue_size=10)
        pubs.append(pub)

    rospy.init_node('rise', anonymous=True)

    rospy.sleep(.5)

    still = Twist()
    [pub.publish(still) for pub in pubs]

if __name__=='__main__':
    try:
        rise()
    except rospy.ROSInterruptException:
        pass
