from visualization_msgs.msg import Marker
import rospy

rospy.init_node(name="mark_text_node")
pub = rospy.Publisher(name="topic_marker_text", data_class=Marker, queue_size=1)
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    text = Marker()
    text.header.frame_id = "panda_link0"
    text.header.stamp = rospy.rostime.get_rostime()
    text.type = Marker.TEXT_VIEW_FACING
    text.text = "text"
    text.scale.z = 1.0
    text.action = Marker.ADD
    text.color.r = 1.0
    text.color.a = 1.0
    text.pose.position.z = -1.0
    pub.publish(text)
    rate.sleep()