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

    xs = [-70, -30, -20, -10, 0, 10, 20, 30, 40]
    # xs = [-40, -30, -20, -10, 0, 10, 20, 30, 40]
    ys = [0, 1, -1, 2, -2, 3, -3, 4, -4]
    for pub, x, y in zip(pubs, xs, ys):
        pos = PoseStamped()
        pos.pose.position.x = x
        pos.pose.position.y = y
        pos.pose.position.z = 0
        quaternion = tf.transformations.quaternion_from_euler(0, 0, -PI/4)
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
