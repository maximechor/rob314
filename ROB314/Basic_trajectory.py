import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose2D
from time import sleep
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

import math

import time
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font

class BoundingBox:
    def __init__ (self):
        self.margin = 0.85
        self.min_x = -1.90*self.margin
        self.min_y = -2.10*self.margin
        self.min_z = 0.0 # to take off
        self.max_x = 1.90*self.margin
        self.max_y = 1.80*self.margin
        self.max_z = 2.5*self.margin

class Position:
    def __init__ (self,x=1,y=1,z=1):
        self.x = x
        self.y = y
        self.z = z

def isInBoundingBox(position,boundingBox):
    if (position.x < boundingBox.max_x):
        if (position.y < boundingBox.max_y):
            if (position.z < boundingBox.max_z):
                if (position.x > boundingBox.min_x):
                    if (position.y > boundingBox.min_y):
                        if (position.z > boundingBox.min_z):
                            return True
    return False

myposition = Position()


def receiver(data):
    global myposition
    myposition.x = data.pose.position.x
    myposition.y = data.pose.position.y
    myposition.z = data.pose.position.z

def receiver_or(data):
    global theta
    theta = data.theta

def correcteur_p(desired_pos, position_cur, Kp):
    return np.array([desired_pos.x - myposition.x,desired_pos.y - myposition.y, desired_pos.z - myposition.z])*Kp

def correcteur_i(desired_pos, position_cur, Ki, sum_err):
    sum_err.x = sum_err.x - myposition.x + desired_pos.x
    sum_err.y = sum_err.y - myposition.y + desired_pos.y
    sum_err.z = sum_err.z - myposition.z + desired_pos.z

    correction_i = np.array([sum_err.x, sum_err.x, sum_err.x]) * Ki
    return [correction_i, sum_err]

def correcteur_d():
    pass

def correction(desired_pos, position_cur,sum_err,Kp,Ki):
    cor_p = correcteur_p(desired_pos,position_cur,Kp)
    [cor_i,sum_err] = correcteur_i(desired_pos, position_cur, Ki, sum_err)

    cor_pi = cor_p + cor_i
    return [cor_pi,sum_err]
    


    


def main():
    global myposition
    global theta
    theta = 0
    Kp = 0.8
    Ki = 0.0004
    Kd = 0

    speed = 1
    
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((200, 200))
    pygame.font.init()

    flight = 0
    
    myboundingBox = BoundingBox()
    rospy.init_node('Basic_trajectory', anonymous=True)
    drone_pos = rospy.Subscriber('/mocap_node/Drone/pose', PoseStamped, receiver ,queue_size=1)
    drone_or = rospy.Subscriber('/mocap_node/Drone/ground_pose', Pose2D, receiver_or ,queue_size=1)
    land = rospy.Publisher('/tello/land', Empty, queue_size=1)
    cmd_vel = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=1)
    takeoff = rospy.Publisher('/tello/takeoff', Empty, queue_size=1)

    empty_msg = Empty()

    desired_pos = Position(0,0,1.5)

    cmd = Twist()

    while(1):

        time.sleep(0.01)
        for e in pygame.event.get():
            #Checking which key has been pressed down
            if e.type == pygame.locals.KEYDOWN:
                #print('DEBUG' + '+' + pygame.key.name(e.key))
                keyname = pygame.key.name(e.key)
                if keyname == 'escape':
                    land.publish(empty_msg)
                    exit(0)
                if keyname == 'return':
                    takeoff.publish(empty_msg)
                    flight = 1

                    sum_err = Position(0,0,0)


        valid = isInBoundingBox(myposition, myboundingBox)
        if (not valid):
            land.publish(empty_msg)
            flight = 0
            #exit(0)

        if (flight == 1):
            
            [cor_pi,sum_err] = correction(desired_pos, myposition,sum_err,Kp,Ki)

            cmd.linear.x = cor_pi[0]*speed*(math.sin(theta))
            cmd.linear.y = cor_pi[1]*speed*(-math.cos(theta))
            cmd.linear.z = cor_pi[2]*speed

            print("DEBUG : Commande :  x = " + str(cmd.linear.x) + "|y = " + str(cmd.linear.y) + "|z = " + str(cmd.linear.z))

            cmd.angular.x = 0; cmd.angular.y = 0; cmd.angular.z = 0
            cmd_vel.publish(cmd)

        

if __name__ == '__main__':
    main()