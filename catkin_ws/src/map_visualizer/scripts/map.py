#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import json

class Room:
    def __init__(self, name):
        self.area = []
        self.obj_int = []
        self.path = []
        self.name = name

    def set_area(self, point):
        self.area.append(point)

class Map:
    def __init__(self, name):
        self.rooms = {}
        self.name = name

    def create_room(self, room_name):
        self.rooms[room_name] = Room(room_name)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        