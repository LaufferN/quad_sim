import rospy
from geometry_msgs.msg import PoseStamped
import tf
import sys

# /cmd_vel geometry_msgs/Twist

PI =  3.1415


def main():
    pubs = []
    for i in range(9):
        pub = rospy.Publisher('quad' + str(i) + '/command/pose', PoseStamped, queue_size=10)
        pubs.append(pub)

    rospy.init_node('pos_controller', anonymous=True)

    rospy.sleep(.5)

    # single frame
    # xs = [-23, -20, -17, -13, -10, -7, -3, 0, 3]
    # ys = [0, 3, -3, 0, 3, -3, 0, 3, -3]
    # thetas = [-PI/4, -PI/4, -PI/4, 0, 0, 0, PI/4, PI/4, PI/4,]

    # runs
    xs_init = [-60, -55, -50, -45, -40, -35, -30, -25, -20]
    xs_final = [44, 46, 48, 50, 52, 54, 56, 58, 60]
    xs = xs_init
    ys = [0, 4, -4, 0, 4, -4, 2, 4, 6]
    thetas = [.2, -PI/4, -PI/4, 0, 0, 0, PI/3, PI/4, PI/5,]


    # single quad
    # xs = [-9]
    # ys = [-70]
    # thetas = [2*PI/3]

    for pub, x, y, theta in zip(pubs, xs, ys, thetas):
        pos = PoseStamped()
        pos.pose.position.x = x
        pos.pose.position.y = y
        pos.pose.position.z = 5
        quaternion = tf.transformations.quaternion_from_euler(0, 0, theta)
        pos.pose.orientation.x = quaternion[0]
        pos.pose.orientation.y = quaternion[1]
        pos.pose.orientation.z = quaternion[2]
        pos.pose.orientation.w = quaternion[3]

        pub.publish(pos)


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
