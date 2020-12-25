#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import json

class Room:
    def __init__(self, name):
        self.area = []
        self.obj_int = {}
        self.path = []
        self.name = name
        self.entrance = []

    def __init__(self, name, area):
        self.name = name
        self.area = []
        self.obj_int = {}
        self.path = []
        self.entrance = []
        self.set_area(area)

    def set_area(self, points):
        for point in points:
            self.area.append([point.x, point.y, point.z])

    def set_obj_int(self, obj, points):
        if obj in self.obj_int:
            obj_int[obj].append(points)
        else:
            obj_int[obj] = []
            obj_int[obj].append(points)

    def set_entrance(self, point):
        self.entrance = point

    def reset_room(self):
        self.area = []
        self.obj_int = []
        self.path = []
        self.name = name
        self.entrance = None

class Map:
    def __init__(self, name):
        self.rooms = {}
        self.name = name

    def __init__(self, name, rooms):
        self.rooms = {}
        self.name = name
        self.set_rooms(rooms)

    def set_rooms(self, room_list):
        for room in room_list:
            self.rooms[room.name]=Room(room.name, room.area)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        