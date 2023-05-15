#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys, select, termios, tty
import time
import threading

settings = termios.tcgetattr(sys.stdin)

class SimpleControl:
    def __init__(self):
        self.velx=0
        self.vely=0
        self.velz=0
        self.rotz=0
        self.rotx=0
        self.roty=0

        self.run_rose=True

        rospy.init_node('husky_teleop')
        self.pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)

        self.t=threading.Thread(target=self.run_ros_node)

        self.t.start()
        
    def run_main(self):
        statu=True
        while statu:
            statu=self.apply_control()


    def apply_control(self):
        key = self.getKey()
        if key=='w':
            self.velx+=0.5
            self.velx=min(self.velx,1.5)
            self.rotz=0
        elif key=='s':
            self.velx-=0.5
            self.velx=max(self.velx,-1.5)
            self.rotz=0
        elif key=='a':
            self.rotz=1
        elif key=='d':
            self.rotz=-1
        elif key=='q':
            self.run_rose=False
            self.t.join()
            return False
        else:
            self.rotz=0
        return True
    
    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def run_ros_node(self):
        while self.run_rose:
            self.sent_ros_node()
    
    def sent_ros_node(self):
        twist=Twist()
        twist.linear.x = self.velx
        twist.linear.y = self.vely
        twist.linear.z = self.velz
        twist.angular.x = self.rotx
        twist.angular.y = self.roty
        twist.angular.z = self.rotz

        self.pub.publish(twist)


#sc=SimpleControl()
#sc.run_main()


