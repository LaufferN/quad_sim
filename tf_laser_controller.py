import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import numpy as np
# import csv

import tensorflow as tf

# /cmd_vel geometry_msgs/Twist


model_path = "tf_laser_classifier/sigmoid_model/model.ckpt" 
tf.reset_default_graph()

reduced_dim = 940

# declare the data placeholders
x = tf.placeholder(tf.float32, [None, reduced_dim])

# declare the weights connecting the input to the hidden layer
w1 = tf.Variable(tf.random_normal([reduced_dim, 2], stddev=0.03), name='w1')
b1 = tf.Variable(tf.random_normal([2]), name='b1')
w2 = tf.Variable(tf.random_normal([2, 3], stddev=0.03), name='w2')
b2 = tf.Variable(tf.random_normal([3]), name='b2')
# and the weights connecting the hidden layer to the output layer
# w3 = tf.Variable(tf.random_normal([10, 3], stddev=0.03), name='w3')
# b3 = tf.Variable(tf.random_normal([3]), name='b3')

# calculate the output of the hidden layer
hidden_out_1 = tf.add(tf.matmul(x, w1), b1)
# hidden_out_1 = tf.nn.sigmoid(hidden_out_1)
alpha = .01
hidden_out_1 = tf.maximum(hidden_out_1, alpha * hidden_out_1)

# calculate the hidden layer output - in this case, let's use a softmax activated
# output layer
y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_out_1, w2), b2))

sess = tf.Session()
saver = tf.train.Saver()
saver.restore(sess, model_path)

# forward = Twist()
# forward.linear.x = 3.0

# left = Twist()
# left.linear.x = 1.5
# left.angular.z = 0.4

# right = Twist()
# right.linear.x = 1.5
# right.angular.z = -.4

forward = Twist()
forward.linear.x = 5.0

left = Twist()
left.linear.x = 2.0
left.angular.z = 0.4

right = Twist()
right.linear.x = 2.0
right.angular.z = -.4

actions = [right, forward, left]
movements = ["right", "forward", "left"]


def classifier(data):
    guess = y_.eval(feed_dict={x: [data]}, session=sess)
    classif = guess[0].argmax()

    return classif

def range_callback(data):
    global feature
    feature = data.ranges[60:-81]

def main():
    pub = rospy.Publisher('quad0/cmd_vel', Twist, queue_size=10)
    rospy.init_node('tf_laser_controller', anonymous=True)
    rospy.Subscriber('quad0/scan', LaserScan, range_callback)

    rospy.sleep(.5) # let ros finish connecting

    done = False
    while not done and not rospy.is_shutdown():

        classif = classifier(feature)

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
