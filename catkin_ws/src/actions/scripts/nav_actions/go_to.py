#! /usr/bin/env python
from __future__ import print_function

import csv
import json
from math import degrees, radians

import actionlib
import rospy
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

import actions.msg

class goToAction(object):
    targetLocation = ''
    goals = {}

    def __init__(self):
        self.getLocations()
    
    def getLocations(self):
          # declare the coordinates of interest
        a = ['entrance', 'bedroom', 'kitchen', 'restroom', 'dinning_room']
        place = 0
        self.goals = {}
        with open('/home/ricardochapa/Desktop/RoBorregos/Roborregos-Navigation-Testing/catkin_ws/src/actions/data/goals.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                goal = [float(i) for i in row]
                self.goals[a[place]] = goal
                place=(place+1)%len(a)
            rospy.loginfo(self.goals)
    
    def getGoals(self):
        return self.goals

if __name__ == '__main__':
    action = goToAction()