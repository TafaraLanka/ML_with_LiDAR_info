#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import csv

def distance_finder(ranges, i, j):
    ranges = [x for x in ranges if x != 0]
    array_slice = ranges[i: j+1]
    return (sum(array_slice)/float(len(array_slice)))

def drive(drive_data):
    global drive_speed, turn_speed
    drive_speed = drive_data.linear.x
    turn_speed = drive_data.angular.z
    drive_speed = round(drive_speed, 2)
    turn_speed = round(turn_speed, 2)

def append_list(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as tafara:
        csv_writer = csv.writer(tafara)
        csv_writer.writerow(list_of_elem)

def obstacle(data):
    rospy.Subscriber("cmd_vel", Twist, drive)

    d1 = distance_finder(data.ranges, 0, 5)
    d2 = distance_finder(data.ranges, 40, 45)
    d3 = distance_finder(data.ranges, 85, 95)
    d4 = distance_finder(data.ranges, 130, 135)
    d5 = distance_finder(data.ranges, 175, 180)

    d1 = round(d1, 3)
    d2 = round(d2, 3)
    d3 = round(d3, 3)
    d4 = round(d4, 3)
    d5 = round(d5, 3)

    item = [d1, d2, d3, d4, d5,  drive_speed, turn_speed]
    append_list('data_two.csv', item)

    print(f"d1 {d1}, d3 {d3}, d5 {d5}, spd {drive_speed}, trn {turn_speed}")


if __name__ == "__main__":
    rospy.init_node('laser_data', anonymous=True)
    rospy.Subscriber("scan", LaserScan, obstacle)
    rospy.spin()
