import rospy
from visualization_msgs.msg import Marker
import math
from geometry_msgs.msg import Point

rospy.init_node(name="marker_line_point")
pub = rospy.Publisher(name="test_topic", data_class=Marker, queue_size=10)
rate = rospy.Rate(30)
test = Marker()


while not rospy.is_shutdown():
    points = Marker()
    line_strip = Marker()
    line_list = Marker()
    points.header.frame_id = line_strip.header.frame_id = line_list.header.frame_id = "panda_link0"
    points.header.stamp = line_strip.header.stamp = line_list.header.stamp = rospy.rostime.get_rostime()
    points.action = line_strip.action = line_list.action = Marker.ADD
    points.pose.orientation.w = line_strip.pose.orientation.w = line_list.pose.orientation.w = 1.0
    points.ns = line_strip.ns = line_list.ns = "test_ns"

    points.type = Marker.POINTS
    line_strip.type = Marker.LINE_STRIP
    line_list.type = Marker.LINE_LIST

    points.scale.x = 0.2
    points.scale.y = 0.2
    line_strip.scale.x = 0.1
    line_list.scale.x = 0.1

    points.color.g = 1.0
    points.color.a = 1.0

    line_strip.color.b = 1.0
    line_strip.color.a = 1.0

    line_list.color.r = 1.0
    line_list.color.a = 1.0
    f = 0.0
    for i in range(100):
        y = 5 * math.sin(f + i / 100.0 * 2 * math.pi)
        z = 5 * math.cos(f + i / 100.0 * 2 * math.pi)
        p = Point()
        p.x = i-50
        p.y = y
        p.z = z
        points.points.append(p)
        line_strip.points.append(p)
        line_list.points.append(p)

        p.z = p.z + 1.0
        line_list.points.append(p)
    pub.publish(points)
    pub.publish(line_list)
    pub.publish(line_strip)
    f = f + 0.4
    rate.sleep()









