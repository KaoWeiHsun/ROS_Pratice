import rospy
from visualization_msgs.msg import Marker

rospy.init_node(name="mark")
# rospy.Rate(1)

pub = rospy.Publisher(name="visualization_markeraaaa", data_class=Marker, queue_size=1)

while not rospy.is_shutdown():
    cube = Marker()
    cube.header.frame_id = "panda_link0"
    cube.header.stamp = rospy.rostime.get_rostime()
    cube.ns = "test"
    cube.id = 1
    cube.type = Marker.ARROW
    cube.action = Marker.ADD
    cube.pose.position.x = 0.5
    cube.pose.position.y = 0.0
    cube.pose.position.z = 0.0
    cube.pose.orientation.x = 0.0
    cube.pose.orientation.y = 0.0
    cube.pose.orientation.z = 0.0
    cube.pose.orientation.w = 1.0
    cube.scale.x = 1.0
    cube.scale.y = 1.0
    cube.scale.z = 1.0
    cube.color.r = 0.0
    cube.color.g = 1.0
    cube.color.b = 0.0
    cube.color.a = 1.0
    # 該物件存活時間
    cube.lifetime = rospy.Duration(100)
    pub.publish(cube)




