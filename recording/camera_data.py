import rospy
from sensor_msgs.msg import Image
import cv2
import cv_bridge


def camera_callback(data):
    global camera_feature
    camera_feature = data

def main():
    rospy.Subscriber('/front_cam/camera/image', Image, camera_callback)
    rospy.init_node('camera_recording', anonymous=True)

    # let ros connect
    rospy.sleep(.5)

    camera_data = []

    bridge = cv_bridge.CvBridge()
    num = 1
    while not rospy.is_shutdown():
        cv_image = bridge.imgmsg_to_cv2(camera_feature, desired_encoding=camera_feature.encoding)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('images/middle_middle/' + str(num) + '.png', gray_image)
        num += 1
        rospy.sleep(.01)

if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
