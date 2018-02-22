import rospy
from sensor_msgs.msg import LaserScan


def range_callback(data):
    global feature
    feature = data.ranges[60:-81]

def main():
    rospy.Subscriber('quad0/scan', LaserScan, range_callback)
    rospy.init_node('laser_scan_recording', anonymous=True)

    # let ros connect
    rospy.sleep(.5)

    file_name = "middle_left"
    with open("laser_scan_data/" + file_name, "w") as f:
        while not rospy.is_shutdown():
            f.write(str(feature)[1:-1] + "\n")
            rospy.sleep(.03)

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
