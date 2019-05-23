import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

# /cmd_vel geometry_msgs/Twist


def rise():
    servs = []
    for i in range(9):
        s = rospy.ServiceProxy('quad' + str(i) + '/engage', Empty)
        servs.append(s)

    rospy.init_node('spawn', anonymous=True)

    rospy.sleep(.5)


    for i in range(9):
        rospy.wait_for_service('quad' + str(i) + '/engage', timeout=None)
        servs[i]()

if __name__=='__main__':
    try:
        rise()
    except rospy.ROSInterruptException:
        pass
