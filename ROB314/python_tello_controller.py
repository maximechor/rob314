import time
import pygame
import pygame.display
import pygame.key
import pygame.locals
import pygame.font
from commands import commands_up,commands_down

import rospy
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

controls = {
    'z': 'forward',
    's': 'backward',
    'q': 'left',
    'd': 'right',
    'space': 'up',
    'left shift': 'down',
    'right shift': 'down',
    'a': 'counter_clockwise',
    'e': 'clockwise',
}

def receiver(data):
    print('test')

def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode((200, 200))
    pygame.font.init()
    
    rospy.init_node('Drone_command', anonymous=True)

    cmd_vel = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=1)
    takeoff = rospy.Publisher('/tello/takeoff', Empty, queue_size=1)
    land = rospy.Publisher('/tello/land', Empty, queue_size=1)
    #flip = rospy.Publisher('tello/flip', UInt8, queue_size=1)
    image = rospy.Subscriber('/tello/image_raw', Image, receiver)

    speed = 1
    turn = 10

    empty_msg = Empty()
    uint8 = UInt8()
    uint8.data = 0

    #Initialisation of the command to 0
    cmd = Twist()
    cmd.linear.x = 0; cmd.linear.y = 0; cmd.linear.z = 0
    cmd.angular.x = 0; cmd.angular.y = 0; cmd.angular.z = 0

    try:
        while 1:
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


                    if keyname in controls:
                        key_handler = controls[keyname]
                        if key_handler == 'forward':
                            cmd.linear.z = speed
                        elif key_handler == 'backward':
                            cmd.linear.y = -speed
                        elif key_handler == 'left':
                            cmd.linear.x = -speed
                        elif key_handler == 'right':
                            cmd.linear.x = speed
                        elif key_handler == 'up':
                            cmd.linear.z = -speed
                        elif key_handler == 'down':
                            cmd.linear.z = speed
                        elif key_handler == 'counter_clockwise':
                            cmd.angular.z = -turn
                        elif key_handler == 'clockwise':
                            cmd.angular.z = turn

                        

                #Checking which key has been released
                elif e.type == pygame.locals.KEYUP:
                    #print('DEBUG' + '-' + pygame.key.name(e.key))
                    keyname = pygame.key.name(e.key)
                    if keyname in controls:
                        key_handler = controls[keyname]
                        print(key_handler)
                        if key_handler == 'forward':
                            cmd.linear.y = 0
                        elif key_handler == 'backward':
                            cmd.linear.y = 0
                        elif key_handler == 'left':
                            cmd.linear.x = 0
                        elif key_handler == 'right':
                            cmd.linear.x = 0
                        elif key_handler == 'up':
                            cmd.linear.z = 0
                        elif key_handler == 'down':
                            cmd.linear.z = 0
                        elif key_handler == 'counter_clockwise':
                            cmd.angular.z = 0
                        elif key_handler == 'clockwise':
                            cmd.angular.z = 0


            cmd_vel.publish(cmd)
    except e:
        print(str(e))
    finally:
        print('Exiting')
        exit(1)
                    

if __name__ == '__main__':
    main()