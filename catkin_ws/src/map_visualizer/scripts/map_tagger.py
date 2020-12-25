#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import json
from geometry_msgs.msg import Point
from std_msgs.msg import Int16
from map_visualizer.msg import MapDisplayState
from map_visualizer.msg import MapContext
from map_visualizer.msg import Room
from map_visualizer.msg import ObjInt
from map import Map

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Pose given %s", data.pose.position)
    global map
    global map_publisher
    global obj_name
    if(state.state not in [0,-1]):
        if state.state == 1:
            print(len(map.rooms))
            for index in range(len(map.rooms)):
                if map.rooms[index].name == state.room:
                    map.rooms[index].area.append(data.pose.position)
        elif state.state == 2:
            for index, obj in map.rooms[state.room].obj_int:
                if obj.name == obj_name:
                    map.rooms[state.room].obj_int[index].obj_area.append(data.pose.position)
        map_publisher.publish(map)
    
state = MapDisplayState()
map = MapContext()
map_publisher = None
state_publisher = None
obj_name = None

if __name__ == '__main__':
    global map_publisher
    global state_publisher
    rospy.init_node('map_tagger')
    topic = 'tagged_map'
    map_publisher = rospy.Publisher("tagged_map", MapContext)
    state_publisher = rospy.Publisher("map_tagger_state", MapDisplayState)
    rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback)

    rospy.loginfo("Map tagger v1")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    global map
    global state
    x = 1
    while not rospy.is_shutdown():
        if x == 1:
            x = raw_input("Give me the name of the map: ")
            map.name = x
            while True:
                print("What do you want to do?")
                print("1. Add a room")
                print("2. Edit a room")
                print("0. Exit")
                x = input()
                if x == 0:
                    break
                if x == 1:
                    # x = raw_input('Give me the name of the room: ')
                    room_name = str(raw_input('Give me the name of the room: '))
                    state.state = 1
                    state.room = room_name
                    state_publisher.publish(state)
                    new_room = Room()
                    new_room.name = room_name
                    map.rooms.append(new_room)
                    # map.create_room(room_name)
                    print("Please choose the enclosing perimeter area of the room with the goal publisher")
                    print("Insert any key to stop")
                    x = raw_input()
                    print("Area saved.")
                    x = input("Save object of interest? (0 = no, 1 = Yes): ")
                    while(x):
                        global obj_name
                        obj_name = str(raw_input('Give me the name of the object: '))
                        state.state = 2
                        state_publisher.publish(state)
                        obj = ObjInt()
                        obj.name = obj_name
                        map.rooms[state.room_name].obj_int.append(obj)
                        print("Please choose the enclosing perimeter area of the object")
                        print("Insert any key to stop")
                        x = raw_input()
                        x = input("Save another object of interest? (0 = no, 1 = Yes): ")
                    state.state = 0
                    state_publisher.publish(state)
        break
    state.state = -1
    state_publisher.publish(state)
    map_obj = Map(map.name, map.rooms)
    print(map_obj.toJSON())
    with open(str(map.name) + '.json', "w") as f:
        f.write(map_obj.toJSON())
