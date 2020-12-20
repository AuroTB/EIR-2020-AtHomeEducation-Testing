#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import json
from map import Map
from geometry_msgs.msg import Point
from std_msgs.msg import Int16

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Pose given %s", data.pose.position)
    global room_name
    global map
    global point_publisher
    if(state == 0):
        map.rooms[room_name].set_area(data.pose.position)
        point_publisher.publish(data.pose.position)
    
state = -1
room_name = None
map = None
point_publisher = None
state_publisher = None

if __name__ == '__main__':
    global point_publisher
    global state_publisher
    rospy.init_node('map_tagger')
    topic = 'map_tagger_pont'
    point_publisher = rospy.Publisher("map_tagger_pont", Point)
    state_publisher = rospy.Publisher("map_tagger_state", Int16)
    rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback)

    rospy.loginfo("Map tagger v1")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("What do you want to do?")
    print("1. Create map")
    print("2. Edit map")
    x = input()

    global map
    global state
    while not rospy.is_shutdown():
        if x == 1:
            x = raw_input("Give me the name of the map: ")
            map = Map(x)
            while True:
                print("What do you want to do?")
                print("1. Add a room")
                print("0. Exit")
                x = input()
                if x == 0:
                    break
                if x == 1:
                    state = 0
                    state_publisher.publish(state)
                    x = raw_input('Give me the name of the room: ')
                    room_name = str(x)
                    map.create_room(room_name)
                    print("Please choose the enclosing perimeter area of the room with the goal publisher")
                    print("Insert any key to stop")
                    x = raw_input()
                    print("Area saved.")
                    state = -1
                    state_publisher.publish(state)
                    # x = input("Save object of interest? Y/n: ")
                    # while(str(x) == 'Y'):
                    #     state = 1
                    #     state_publisher.publish(state)
                    #     print("Please choose the enclosing perimeter area of the object")
                    #     print("Insert any key to stop")
                    #     x = raw_input()
                    #     x = raw_input("Save another object of interest? Y/n: ")
        break

    mapJsonStr = map.toJSON()
    print(mapJsonStr)
    with open(str(map.name) + '.json', "w") as f:
        f.write(mapJsonStr)
