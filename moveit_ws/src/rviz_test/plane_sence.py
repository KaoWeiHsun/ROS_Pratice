
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

from moveit_msgs.msg import Grasp

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)
scene = moveit_commander.PlanningSceneInterface()
robot = moveit_commander.RobotCommander()
group_name = "panda_arm"
group = moveit_commander.MoveGroupCommander(group_name)
try:
    pos = geometry_msgs.msg.PoseStamped()
    pos.header.frame_id = "panda_link0"

    scene.add_mesh(name="tttt", pose=pos,
                   filename="C:\Users\koa\Desktop\obj\eyeball.obj", size=(1, 1, 1))
except:
    moveit_commander.roscpp_shutdown()
moveit_commander.roscpp_shutdown()
