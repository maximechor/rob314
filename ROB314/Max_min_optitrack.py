import rospy
from geometry_msgs.msg import PoseStamped


x = 0.
y = 0.
z = 0.

def receiver(data):
    global x
    global y
    global z
    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

def main():
    counter = 0
    max_x = -100
    max_y = -100
    max_z = -100
    min_x = 100
    min_y = 100
    min_z = 100
    global x
    global y
    global z
    rospy.init_node('Basic_trajectory', anonymous=True)
    wand_pos = rospy.Subscriber('/mocap_node/Wand/pose', PoseStamped, receiver)

    while(1):
        counter = counter + 1
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z

        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if z < min_z:
            min_z = z

        if (counter%2000) == 0:
            print(min_x)
            print(min_y)
            print(min_z)

            print(max_x)
            print(max_y)
            print(max_z)

            print("\n\n")


if __name__ == '__main__':
    main()