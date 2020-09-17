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

from nav_actions.go_to import goToAction

import actions.msg


""" 
Valid states:
    PENDING
    ACTIVE
    SUCCEEDED
    ABORTED
Valid Actions:
    gt-Place
    so-Object
    ao-toDefine
"""


class navigationServer(object):
    # Create messages that are used to publish feedback/result
    _feedback = actions.msg.navServFeedback()
    _result = actions.msg.navServResult()
    _goToAction = goToAction()
    _moveBaseStatus = ["PENDING","ACTIVE", "SUCCEDED","ABORTED"]


    def __init__(self, name):
        self._action_name = name
        rospy.loginfo(name)
        # Initialize Navigation Action Server
        self._as = actionlib.SimpleActionServer(self._action_name, actions.msg.navServAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
    
    def execute_cb(self, goal):
        # Action Type
        action = goal.target_location[0:2]
 
        if (action == "gt"):
            # Validate target location
            rospy.loginfo("Goal received!")
            rospy.loginfo("Looking for the goal in the map...")
            goal_given = goal.target_location[3:] 
            
            # Valid if the given location is in the known locations.
            if self._goToAction.locationExists(goal_given) == True:
                # Start executing the action
                self.send_goal(self._goToAction.getLocation(goal_given))
            else:
                #Rejected goal
                self._result = False
                rospy.loginfo('%s: Aborted. Location not found' % self._action_name)
                self._as.set_aborted()

        elif (action == "so"):
            rospy.loginfo("Search Object Action")
        elif (action == "ao"):
            rospy.loginfo("Approach Object Action")
        else:
            rospy.loginfo("Invalid Action")
            self._result = False
            self._as.set_aborted()

    def getMoveBaseStatus(self, data):
        self.status = data.status_list[0].status

        if (self.status < 2):
            self._feedback.status = self._moveBaseStatus[self.status]
        elif (self.status == 2 or self.status > 4):
            self._feedback.status = self._moveBaseStatus[3]
        else:
            self._feedback.status = self._moveBaseStatus[self.status - 1]

        self._as.publish_feedback(self._feedback)
        
        rospy.loginfo(rospy.get_caller_id() + " I heard %s", self._feedback.status)

    def send_goal(self, goal_pose_given):
        #define a client for to send goal requests to the move_base server through a SimpleActionClient
        ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        #wait for the action server to come up
        while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
                rospy.loginfo("Waiting for the move_base action server to come up")
        
        goal = MoveBaseGoal()
        #set up the frame parameters
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        # set up goal pose and orientation
        goal.target_pose.pose.position =  Point(goal_pose_given[0],goal_pose_given[1],0)
        goal.target_pose.pose.orientation.x = goal_pose_given[2]
        goal.target_pose.pose.orientation.y = goal_pose_given[3]
        goal.target_pose.pose.orientation.z = goal_pose_given[4]
        goal.target_pose.pose.orientation.w = goal_pose_given[5]

        rospy.loginfo("Sending goal location ...")
        ac.send_goal(goal)

        moveBaseStatusTopic = rospy.Subscriber("move_base/status", GoalStatusArray, self.getMoveBaseStatus)

        ac.wait_for_result(rospy.Duration(120))
       
        if(ac.get_state() ==  GoalStatus.SUCCEEDED):
            moveBaseStatusTopic.unregister()
            rospy.loginfo("You have reached the destination")
            self._result.result = True
            self._as.set_succeeded(self._result)
            return True
        else:
            moveBaseStatusTopic.unregister()
            rospy.loginfo("The robot failed to reach the destination")
            self._result.result = False
            self._as.set_aborted()
            return False


if __name__ == '__main__':
    rospy.init_node('navServer')
    server = navigationServer(rospy.get_name())
    rospy.spin()
