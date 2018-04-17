import sys

import rospy
from geometry_msgs.msg import Twist
from controller_manager_msgs.srv import SwitchController

# /cmd_vel geometry_msgs/Twist


def rise(controller):
    servs = []
    for i in range(9):
        s = rospy.ServiceProxy('quad' + str(i) + '/controller_manager/switch_controller', SwitchController)
        # s = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
        servs.append(s)
    pubs = []
    for i in range(9):
        pub = rospy.Publisher('quad' + str(i) + '/cmd_vel', Twist, queue_size=10)
        pubs.append(pub)

    rospy.init_node('spawn', anonymous=True)

    rospy.sleep(.5)

    still = Twist()

    for i in range(9):
        if controller == "twist":
            servs[i]([], ["controller/pose"], 2)
            pubs[i].publish(still)
        elif controller == "pose":
            servs[i](["controller/pose"], [], 2)
        else:
            print("Error: Unknown controller")

if __name__=='__main__':
    try:
        rise(sys.argv[1])
    except rospy.ROSInterruptException:
        pass
