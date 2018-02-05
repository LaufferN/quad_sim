from random import shuffle

import tensorflow as tf
import numpy as np

from PIL import Image

def pca(A, dim):

    M = (A-np.mean(A.T,axis=1)).T # subtract the mean (along columns)

    # computing eigenvalues and eigenvectors of covariance matrix
    cov = np.cov(M)
    [latent,coeff] = np.linalg.eig(cov) 
    coeff = coeff.astype(float) # discard complex part that results from numerical error

    idx = np.argsort(latent) # sorting the eigenvalues
    idx = idx[::-1] # in ascending order

    # sorting eigenvectors according to the sorted eigenvalues
    coeff = coeff[:,idx]
    latent = latent[idx] # sorting eigenvalues

    p = np.size(coeff,axis=1)
    if dim < p and dim >= 0: # check if reduction makes sense
        coeff = coeff[:,range(dim)] # cutting dimensionality
    return coeff


def normalize(arr):
    """
    Linear normalization
    """
    arr = arr.astype('float')
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
            return arr

def main():

    # hyperparameters
    learning_rate = 0.5
    epochs = 10
    batch_size = 10
    reduced_dim = 9*9

    # grab training data
    folders = ["middle_left/", "middle_middle/", "middle_right/"]
    label_tags = [np.array([1.,0.,0.]), np.array([0.,1.,0.]), np.array([0.,0.,1.])]
    images = []
    labels = [] 
    for folder, label_tag in zip(folders, label_tags):
        for i in range(1, 1850):
            img = Image.open("../recording/images/" + folder + str(1) + ".png")
            img = img.resize((9,9)) #,Image.ANTIALIAS)
            arr = np.array(img)
            # norm_arr = normalize(arr)
            data = []
            for pixel in arr.flatten():
                data.append(float(pixel)/255.0)
            images.append(np.asarray(data))
            labels.append(label_tag)

    # calculate PCA
    # print("starting PCA")
    # rotation_reduced = pca(train_images, reduced_dim)

    # randomize order of data
    mix = zip(images, labels)
    shuffle(mix)
    images, labels = zip(*mix)

    # assign test and train sets
    train_images = images[:1750]
    train_labels = labels[:1750]
    test_images = images[1750:]
    test_labels = labels[1750:]
    # train_images = train_images[0:2] * 150
    # train_labels = train_labels[0:2] * 150

    # convert to numpy arrays
    # train_images = np.asarray(train_images)
    # train_labels = np.asarray(train_labels)
    # test_images = np.asarray(test_images)
    # test_labels = np.asarray(test_labels)

    # img = Image.new('L', (28,24))
    # img.putdata(np.asarray(test_images[20]))
    # print(test_labels[20])
    # img.show()

    # convert training data to reduced dimension
    # train_pca_images = []
    # for image in train_images:
    #     small_transformed_image = np.dot(rotation_reduced.T, image)
    #     train_pca_images.append(small_transformed_image)

    # # same for testing
    # test_pca_images = []
    # for image in test_images:
    #     small_transformed_image = np.dot(rotation_reduced.T, image)
    #     test_pca_images.append(small_transformed_image)

    train_pca_images = train_images
    test_pca_images = test_images



    # declare the training data placeholders
    x = tf.placeholder(tf.float32, [None, reduced_dim])
    # now declare the output data placeholder - 3 classes
    y = tf.placeholder(tf.float32, [None, 3])

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
    # hidden_out_2 = tf.add(tf.matmul(hidden_out_1, w2), b2)
    # hidden_out_2 = tf.nn.relu(hidden_out_2)

    # calculate the hidden layer output - in this case, let's use a softmax activated
    # output layer
    y_ = tf.nn.softmax(tf.add(tf.matmul(hidden_out_1, w2), b2))

    # define the cost function which we are going to train the model on
    y_clipped = tf.clip_by_value(y_, 1e-10, 0.9999999)
    cross_entropy = -tf.reduce_mean(tf.reduce_sum(y * tf.log(y_clipped)
                                                  + (1 - y) * tf.log(1 - y_clipped), axis=1))
    # cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_clipped))

    # add an optimizer
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

    # finally setup the initialisation operator
    init_op = tf.global_variables_initializer()

    # define an accuracy assessment operation
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    saver = tf.train.Saver()

    # start the session
    with tf.Session() as sess:
        # initialize the variables
        sess.run(init_op)
        # grab a batch
        total_batch = int(len(train_pca_images) / batch_size)
        for epoch in range(epochs):
            avg_cost = 0
            flag = True
            for i in range(total_batch):
                batch_x = train_pca_images[i*batch_size : (i+1)*batch_size]
                batch_y = train_labels[i*batch_size : (i+1)*batch_size]

                if flag:

                    # img = Image.new('L', (28,24))
                    # img.putdata(np.asarray(batch_x[0]))
                    # print(batch_y[0])
                    # img.show()
                    flag = False

                # feed batches
                _, c = sess.run([optimizer, cross_entropy], feed_dict={x: batch_x, y: batch_y})
                avg_cost += c / total_batch
            print("Epoch:", (epoch + 1), "cost =", "{:.3f}".format(avg_cost))

        print("\nTraining complete!")
        print("Accuracy", sess.run(accuracy, feed_dict={x: test_pca_images, y: test_labels}))
        saver.save(sess, "model.ckpt")

        # guess = y_.eval(feed_dict={x: [test_pca_images[0]]}, session=sess)


if __name__ == '__main__':
    main()
