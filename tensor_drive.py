#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from keras.models import load_model
from sensor_msgs.msg import LaserScan


def dist(ranges, i, j):
    ranges = [x for x in ranges if x != 0]
    array_slice = ranges[i: j+1]
    return sum(array_slice)/float(len(array_slice))


def process(data):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    d1 = dist(data.ranges, 0, 5)
    d2 = dist(data.ranges, 40, 45)
    d3 = dist(data.ranges, 85, 95)
    d4 = dist(data.ranges, 130, 135)
    d5 = dist(data.ranges, 175, 180)

    d1 = round(d1, 3)
    d2 = round(d2, 3)
    d3 = round(d3, 3)
    d4 = round(d4, 3)
    d5 = round(d5, 3)

    # f = h5py.File('/home/tafara/catkin_ws/src/ros_car/src/model.h5', mode='r')
    item = [(d1, d2, d3, d4, d5)]
    model = load_model('/home/tafara/catkin_ws/src/ros_car/src/model_final.h5')
    angle = model.predict(item)
    angle = round(angle[0][0], 1)

    twist = Twist()
    twist.linear.x = 0.15
    twist.linear.y = 0.0
    twist.linear.z = 0.0
    twist.angular.x = 0.0
    twist.angular.y = 0.0
    twist.angular.z = angle

    print(angle)

    pub.publish(twist)

    # print(angle)

if __name__ == "__main__":
    rospy.init_node("controller", anonymous=True)
    rospy.Subscriber('scan', LaserScan, process)
    rospy.spin()
