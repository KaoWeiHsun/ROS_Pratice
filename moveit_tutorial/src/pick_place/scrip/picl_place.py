import rospy, sys
import moveit_commander
from geometry_msgs.msg import PoseStamped, Pose
from moveit_commander import MoveGroupCommander, PlanningSceneInterface
from moveit_msgs.msg import PlanningScene, ObjectColor
from moveit_msgs.msg import Grasp, GripperTranslation, MoveItErrorCodes
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from tf.transformations import quaternion_from_euler
from copy import deepcopy

import numpy as np
import define.unit as un

GRIPPER_OPEN = [0.04, 0.4]
GRIPPER_CLOSED = [0.0, 0.0]

class PickAndPlace:
    def __init__(self,robot_name="panda_arm",frame="panda_link0"):
        try:
            moveit_commander.roscpp_initialize(sys.argv)
            rospy.init_node(name="pick_place_test")
            self.scene = PlanningSceneInterface()
            self.scene_pub = rospy.Publisher('planning_scene', PlanningScene, queue_size=10)
            # region Robot initial
            self.robot = MoveGroupCommander(robot_name)
            self.robot.set_goal_joint_tolerance(0.00001)
            self.robot.set_goal_position_tolerance(0.00001)
            self.robot.set_goal_orientation_tolerance(0.01)
            self.robot.set_goal_tolerance(0.00001)
            self.robot.allow_replanning(True)
            self.robot.set_pose_reference_frame(frame)
            self.robot.set_planning_time(3)
            # endregion
            self.gripper = MoveGroupCommander("hand")
            self.gripper.set_joint_value_target(GRIPPER_CLOSED)
            self.gripper.go()
            self.gripper.set_joint_value_target(GRIPPER_OPEN)
            self.gripper.go()
            self.gripper.set_joint_value_target(GRIPPER_CLOSED)
            self.gripper.go()

            # Robot go home
            self.robot.set_named_target("home")
            self.robot.go()
            # clear all object in world
            self.clear_all_object()

            table_pose = un.Pose(0, 0, -10, 0, 0, 0)
            table_color = un.Color(255, 255, 0, 100)
            self.add_object_box("table", table_pose, table_color, frame, (2000, 2000, 10))

            bearing_pose = un.Pose(250, 250, 500, -90, 45, -90)
            bearing_color = un.Color(255, 0, 255, 255)
            bearing_file_name = "../stl/bearing.stl"
            self.add_object_mesh("bearing", bearing_pose, bearing_color, frame, bearing_file_name)
            obpose = self.scene.get_object_poses(["bearing"])
            # self.robot.set_support_surface_name("table")
            g = Grasp()
            # Create gripper position open or close
            g.pre_grasp_posture = self.open_gripper()
            g.grasp_posture = self.close_gripper()
            g.pre_grasp_approach = self.make_gripper_translation(0.01, 0.1, [0, 1.0, 0])
            g.post_grasp_retreat = self.make_gripper_translation(0.01, 0.9, [0, 1.0,0])
            p = PoseStamped()
            p.header.frame_id = "panda_link0"
            p.pose.orientation =obpose["bearing"].orientation
            p.pose.position = obpose["bearing"].position
            g.grasp_pose = p
            g.allowed_touch_objects = ["bearing"]
            a=[]
            a.append(g)
            result = self.robot.pick(object_name="bearing", grasp=a)
            print(result)



        except Exception as ex:
            print(ex)
            moveit_commander.roscpp_shutdown()

        moveit_commander.roscpp_shutdown()


    def make_gripper_translation(self,min_dist, desired, vector):
        g = GripperTranslation()
        g.direction.vector.x = vector[0]
        g.direction.vector.y = vector[1]
        g.direction.vector.z = vector[2]
        g.direction.header.frame_id = "panda_link0"
        g.min_distance = min_dist
        g.desired_distance = desired
        return g

    def open_gripper(self):
        t = JointTrajectory()
        t.joint_names = ['panda_finger_joint1', 'panda_finger_joint2']
        tp = JointTrajectoryPoint()
        tp.positions = [0.04, 0.04]
        tp.time_from_start = rospy.Duration(secs=1)
        t.points.append(tp)
        return t

    def close_gripper(self):
        t = JointTrajectory()
        t.joint_names = ['panda_finger_joint1', 'panda_finger_joint2']
        tp = JointTrajectoryPoint()
        tp.positions = [0.0, 0.0]
        tp.time_from_start = rospy.Duration(secs=1)
        t.points.append(tp)
        return t


    def clear_all_object(self):
        for world_object in (self.scene.get_known_object_names()):
            self.scene.remove_world_object(world_object)
        for attached_object in (self.scene.get_attached_objects()):
            self.scene.remove_attached_object(attached_object)

    def add_object_box(self, object_name, pose, color, frame, size):
        """
        add object in rviz
        :param object_name: name of object
        :param pose:  pose of object. (xyz) in mm,(abc) in degree
        :param color: color of object.(RGBA)
        :param frame: reference_frame
        :param size: size of object(mm)
        :return: None
        """
        # Add object
        object_pose = PoseStamped()
        object_pose.header.frame_id = frame
        object_pose.pose.position.x = pose.X / 1000.0
        object_pose.pose.position.y = pose.Y / 1000.0
        object_pose.pose.position.z = pose.Z / 1000.0
        quaternion = quaternion_from_euler(np.deg2rad(pose.A), np.deg2rad(pose.B), np.deg2rad(pose.C))
        object_pose.pose.orientation.x = quaternion[0]
        object_pose.pose.orientation.y = quaternion[1]
        object_pose.pose.orientation.z = quaternion[2]
        object_pose.pose.orientation.w = quaternion[3]
        self.scene.add_box(name=object_name, pose=object_pose, size=(size[0]/1000.0, size[1]/1000.0, size[2]/1000.0))
        # Add object color
        object_color = ObjectColor()
        object_color.id = object_name
        object_color.color.r = color.R / 255.00
        object_color.color.g = color.G / 255.00
        object_color.color.b = color.B / 255.00
        object_color.color.a = color.A / 255.00

        p = PlanningScene()
        p.is_diff = True
        p.object_colors.append(object_color)
        self.scene_pub.publish(p)

    def add_object_mesh(self, object_name, pose, color, frame, file_name):
        """
        add object in rviz
        :param object_name: name of object
        :param pose:  pose of object. (xyz) in mm,(abc) in degree
        :param color: color of object.(RGBA)
        :param frame: reference_frame
        :param file_name: mesh file name
        :return: None
        """
        # Add object
        object_pose = PoseStamped()
        object_pose.header.frame_id = frame
        object_pose.pose.position.x = pose.X / 1000.0
        object_pose.pose.position.y = pose.Y / 1000.0
        object_pose.pose.position.z = pose.Z / 1000.0
        quaternion = quaternion_from_euler(np.deg2rad(pose.A), np.deg2rad(pose.B), np.deg2rad(pose.C))
        object_pose.pose.orientation.x = quaternion[0]
        object_pose.pose.orientation.y = quaternion[1]
        object_pose.pose.orientation.z = quaternion[2]
        object_pose.pose.orientation.w = quaternion[3]
        self.scene.add_mesh(name=object_name, pose=object_pose, filename=file_name, size=(0.001, 0.001, 0.001))
        # Add object color
        object_color = ObjectColor()
        object_color.id = object_name
        object_color.color.r = color.R / 255.00
        object_color.color.g = color.G / 255.00
        object_color.color.b = color.B / 255.00
        object_color.color.a = color.A / 255.00

        p = PlanningScene()
        p.is_diff = True
        p.object_colors.append(object_color)
        self.scene_pub.publish(p)


if __name__ == "__main__":
    PickAndPlace()
