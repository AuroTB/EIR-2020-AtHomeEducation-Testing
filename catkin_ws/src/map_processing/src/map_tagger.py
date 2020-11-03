#!/usr/bin/env python
from geometry_msgs.msg import Point
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

class Place:
    def __init__(self, name, p1, p2, p3, p4):
        self.p1 = p1 
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.name = name

marker_array_ = []

def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose)
    # coordinateX = data.pose.pose.position.x
    # coordinateY = data.pose.pose.position.y
    # quaternionX = data.pose.pose.orientation.x
    # quaternionY = data.pose.pose.orientation.y
    # quaternionZ = data.pose.pose.orientation.z
    # quaternionW = data.pose.pose.orientation.w
    # f= open("goals.csv","a+")
    # f.write("%f,%f,%f,%f,%f,%f\r\n" % (coordinateX, coordinateY, quaternionX, quaternionY, quaternionZ, quaternionW))
    # f.close()
    show_marker(data.pose)

def show_marker(pos_, ori_, scale_, color_, lifetime_):
    global marker_array_
    marker_ = Marker()
    marker_.header.frame_id = "/table_top"
    # marker_.header.stamp = rospy.Time.now()
    marker_.type = marker_.CUBE
    marker_.action = marker_.ADD

    marker_.pose.position.x = pos_.position.x
    marker_.pose.position.y = pos_.position.y
    marker_.pose.position.z = pos_.position.z
    marker_.pose.orientation.x = pos_.orientation.x
    marker_.pose.orientation.y = pos_.orientation.y
    marker_.pose.orientation.z = pos_.orientation.z
    marker_.pose.orientation.w = pos_.orientation.w

    marker_.lifetime = rospy.Duration.from_sec(lifetime_)
    marker_.scale.x = scale_[0]
    marker_.scale.y = scale_[1]
    marker_.scale.z = scale_[2]
    marker_.color.a = 0.5
    red_, green_, blue_ = color_
    marker_.color.r = red_
    marker_.color.g = green_
    marker_.color.b = blue_
    marker_array_.markers.append(marker_)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('goal_listener', anonymous=True)

    rospy.Subscriber("/move_base_simple/goal", PoseWithCovarianceStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()