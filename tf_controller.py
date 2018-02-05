import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

import numpy as np
# import csv
import cv_bridge
import cv2

import tensorflow as tf

# /cmd_vel geometry_msgs/Twist



model_path = "tf_classifier/model.ckpt" 
tf.reset_default_graph()

reduced_dim = 9*9

# declare the data placeholders
x = tf.placeholder(tf.float32, [None, reduced_dim])

# declare the weights connecting the input to the hidden layer
w1 = tf.Variable(tf.random_normal([reduced_dim, 10], stddev=0.03), name='w1')
b1 = tf.Variable(tf.random_normal([10]), name='b1')
w2 = tf.Variable(tf.random_normal([10, 3], stddev=0.03), name='w2')
b2 = tf.Variable(tf.random_normal([3]), name='b2')
# and the weights connecting the hidden layer to the output layer
# w3 = tf.Variable(tf.random_normal([10, 3], stddev=0.03), name='w3')
# b3 = tf.Variable(tf.random_normal([3]), name='b3')

# calculate the output of the hidden layer
hidden_out_1 = tf.add(tf.matmul(x, w1), b1)
hidden_out_1 = tf.nn.sigmoid(hidden_out_1)

# calculate the hidden layer output - in this case, let's use a softmax activated
# output layer
y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_out_1, w2), b2))

sess = tf.Session()
saver = tf.train.Saver()
saver.restore(sess, model_path)

forward = Twist()
forward.linear.x = 3.0

left = Twist()
left.linear.x = 1.5
left.angular.z = 0.4

right = Twist()
right.linear.x = 1.5
right.angular.z = -.4

actions = [right, forward, left]
movements = ["right", "forward", "left"]

camera_feature = np.array(0)

bridge = cv_bridge.CvBridge()

def classifier(image):
    guess = y_.eval(feed_dict={x: [image]}, session=sess)
    classif = guess[0].argmax()

    return classif

def camera_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding=data.encoding)
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(gray_image, (9,9))

    global camera_feature
    camera_feature = np.asarray(img).flatten()

def main():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('rise', anonymous=True)
    rospy.Subscriber('/front_cam/camera/image', Image, camera_callback)

    rospy.sleep(.5) # let ros finish connecting

    done = False
    while not done and not rospy.is_shutdown():

        # create laser scanner subscriber

        # print(feature)


        # print(mode_class)


        classif = classifier(camera_feature)

        action = actions[classif]
        print("Going " + movements[classif]) 

        pub.publish(action)

        rospy.sleep(.05)

        # rospy.spin()


if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
