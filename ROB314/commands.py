from geometry_msgs.msg import Twist

def commands(key_handler):
    pass

def commands_down(cmd, key_handler):
    
    cmd.linear.x = 0; cmd.linear.y = 0; cmd.linear.z = 0
    cmd.angular.x = 0; cmd.angular.y = 0; cmd.angular.z = 0
    return cmd

def commands_up(cmd, key_handler):
    
    cmd.linear.x = 0; cmd.linear.y = 0; cmd.linear.z = 0
    cmd.angular.x = 0; cmd.angular.y = 0; cmd.angular.z = 0
    return cmd