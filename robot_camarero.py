# -*- coding: utf-8 -*-
# from __future__ import print_function

import rospy
from smach_ros import SimpleActionState
import smach_ros
import math
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import Sound
import rospy, cv2, cv_bridge
import numpy as np
from time import sleep
import time

#Definicion de los topics 
TOPIC_TABLE = "/table"
TOPIC_SOUND = "/mobile_base/commands/sound"

class WaitAndSound(State):
    def __init__(self):
        State.__init__(self, outcomes=['finish'])
        

    def execute(self, userdata):
        self.pubSound = rospy.Publisher(TOPIC_SOUND,Sound,queue_size=5)
        
        for i in range(15):
            self.pubSound.publish(1)
            time.sleep(1)

        return 'finish'




class WaitAndDetect(State):
    def __init__(self):
        State.__init__(self, outcomes=['table1','table2','table3','table4','table5'])
        self.table1 = False
        self.table2 = False
        self.table3 = False
        self.table4 = False
        self.table5 = False
    
    def execute(self, userdata):
        self.table1 = False
        self.table2 = False
        self.table3 = False
        self.table4 = False
        self.table5 = False
        self.subTable = rospy.Subscriber(TOPIC_TABLE, String, self.table_callback)
        rate = rospy.Rate(10)

        # Realizar el movimiento de "deambulación" hasta que se detecte un color        
        while not self.table1 and not self.table2 and not self.table3 and not self.table4 and not self.table5:
            rate.sleep()
        
        self.subTable.unregister()

        if self.table1:
            return "table1"
        elif self.table2:
            return "table2"
        elif self.table3:
            return "table3"
        elif self.table4:
            return "table4"
        elif self.table5:
            return "table5"


    def table_callback(self, msg):
        if msg.data == "table1":
            print("Enviando plato a la mesa 1")
            self.table1 = True
        elif msg.data == "table2":
            print("Enviando plato a la mesa 2")
            self.table2 = True
        elif msg.data == "table3":
            print("Enviando plato a la mesa 3")
            self.table3 = True
        elif msg.data == "table4":
            print("Enviando plato a la mesa 4")
            self.table4 = True
        elif msg.data == "table5":
            print("Enviando plato a la mesa 5")
            self.table5 = True


if __name__ == '__main__':
    rospy.init_node("restaurant")
    sm = StateMachine(outcomes=['end'])

    with sm:

        goal_table1 = MoveBaseGoal()
        goal_table1.target_pose.header.frame_id = 'map'
        goal_table1.target_pose.pose.position.x = -3.43
        goal_table1.target_pose.pose.position.y = -7.72
        goal_table1.target_pose.pose.orientation.x = 0
        goal_table1.target_pose.pose.orientation.y = 0
        goal_table1.target_pose.pose.orientation.z = -0.89
        goal_table1.target_pose.pose.orientation.w = 0.45

        goal_table2 = MoveBaseGoal()
        goal_table2.target_pose.header.frame_id = 'map'
        goal_table2.target_pose.pose.position.x = -4.82
        goal_table2.target_pose.pose.position.y = -7.06
        goal_table2.target_pose.pose.orientation.x = 0
        goal_table2.target_pose.pose.orientation.y = 0
        goal_table2.target_pose.pose.orientation.z = 0.68
        goal_table2.target_pose.pose.orientation.w = 0.73

        goal_table3 = MoveBaseGoal()
        goal_table3.target_pose.header.frame_id = 'map'
        goal_table3.target_pose.pose.position.x = -2.03
        goal_table3.target_pose.pose.position.y = -7.02
        goal_table3.target_pose.pose.orientation.x = 0
        goal_table3.target_pose.pose.orientation.y = 0
        goal_table3.target_pose.pose.orientation.z = -0.12
        goal_table3.target_pose.pose.orientation.w = 0.99

        goal_table4 = MoveBaseGoal()
        goal_table4.target_pose.header.frame_id = 'map'
        goal_table4.target_pose.pose.position.x = -2.02
        goal_table4.target_pose.pose.position.y = -5.18
        goal_table4.target_pose.pose.orientation.x = 0
        goal_table4.target_pose.pose.orientation.y = 0
        goal_table4.target_pose.pose.orientation.z = 0.72
        goal_table4.target_pose.pose.orientation.w = 0.69

        goal_table5 = MoveBaseGoal()
        goal_table5.target_pose.header.frame_id = 'map'
        goal_table5.target_pose.pose.position.x = -0.05
        goal_table5.target_pose.pose.position.y = -5.58
        goal_table5.target_pose.pose.orientation.x = 0
        goal_table5.target_pose.pose.orientation.y = 0
        goal_table5.target_pose.pose.orientation.z = -0.21
        goal_table5.target_pose.pose.orientation.w = 0.98

        goal_home = MoveBaseGoal()
        goal_home.target_pose.header.frame_id = 'map'
        goal_home.target_pose.pose.position.x = -6.48
        goal_home.target_pose.pose.position.y = -8.26
        goal_home.target_pose.pose.position.z = 0
        goal_home.target_pose.pose.orientation.x = 0
        goal_home.target_pose.pose.orientation.y = 0
        goal_home.target_pose.pose.orientation.z = -0.63
        goal_home.target_pose.pose.orientation.w = 0.77

        # Agregar los estados al plan de acción
        StateMachine.add('WaitAndDetect', WaitAndDetect(), 
           transitions={
               'table1':'MoveTable1',
               'table2':'MoveTable2',
               'table3':'MoveTable3',
               'table4':'MoveTable4',
               'table5':'MoveTable5'})
               
        StateMachine.add('MoveHome', SimpleActionState('move_base',MoveBaseAction,goal=goal_home),
            transitions={'succeeded':'WaitAndDetect','preempted':'end','aborted':'end'})

        StateMachine.add('WaitAndSound', WaitAndSound(),
            transitions={'finish':'MoveHome'})

        StateMachine.add('MoveTable1', SimpleActionState('move_base',MoveBaseAction,goal=goal_table1),
            transitions={'succeeded':'WaitAndSound','aborted':'MoveHome','preempted':'MoveHome'})  

        StateMachine.add('MoveTable2', SimpleActionState('move_base',MoveBaseAction,goal=goal_table2),
            transitions={'succeeded':'WaitAndSound','aborted':'MoveHome','preempted':'MoveHome'})  

        StateMachine.add('MoveTable3', SimpleActionState('move_base',MoveBaseAction,goal=goal_table3),
            transitions={'succeeded':'WaitAndSound','aborted':'MoveHome','preempted':'MoveHome'})  

        StateMachine.add('MoveTable4', SimpleActionState('move_base',MoveBaseAction,goal=goal_table4),
            transitions={'succeeded':'WaitAndSound','aborted':'MoveHome','preempted':'MoveHome'})  

        StateMachine.add('MoveTable5', SimpleActionState('move_base',MoveBaseAction,goal=goal_table5),
            transitions={'succeeded':'WaitAndSound','aborted':'MoveHome','preempted':'MoveHome'})  

        
        
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()  