import rospy
from geometry_msgs.msg import Twist

# /cmd_vel geometry_msgs/Twist


def rise():
    pubs = []
    for i in range(9):
        pub = rospy.Publisher('quad' + str(i) + '/cmd_vel', Twist, queue_size=10)
        pubs.append(pub)

    rospy.init_node('rise', anonymous=True)

    up_vel = Twist()
    up_vel.linear.z = 2.0

    rospy.sleep(.5)

    still = Twist()
    [pub.publish(up_vel) for pub in pubs]

    # rospy.sleep(8.0) height for valley
    rospy.sleep(6.0)
    [pub.publish(still) for pub in pubs]


if __name__=='__main__':
    try:
        rise()
    except rospy.ROSInterruptException:
        pass
