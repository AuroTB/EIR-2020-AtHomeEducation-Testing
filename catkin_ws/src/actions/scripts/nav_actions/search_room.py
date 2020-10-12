#! /usr/bin/env python
from __future__ import print_function

import actionlib
import rospy

from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_actions.move_base import MoveBase

class searchRoom(object):
    _goalPoints = {}

    def getGoalPoints(self, location):
        ## TODO 
        ## Implement get_room_path
        ## self._goalPoints = get_room_path.getPoints(location)
        ## return get_room_path.generatePath(self._goalPoints)
        rospy.loginfo('Search Room Action Class Called')

if __name__ == "__main__":
    searchRoom = searchRoom()