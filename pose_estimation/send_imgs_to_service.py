#!/usr/bin/env python
import rospy
import sys
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image


def import_img(rgb_path=None):
    depth_path = str(rgb_path).replace("rgb", "depth", 1)
    print(rgb_path)
    print(depth_path)
    img_rgb = cv2.imread(rgb_path)
    img_depth = cv2.imread(depth_path)

    # cv2.imshow("image", img)
    # cv2.waitKey(2000)
    bridge = CvBridge()
    img_rgb_msg = bridge.cv2_to_imgmsg(img_rgb, "bgr8")
    img_depth_msg = bridge.cv2_to_imgmsg(img_depth, "passtrough")
    pub_rgb = rospy.Publisher('rgb_image', Image, queue_size=10)
    pub_depth = rospy.Publisher('depth_image', Image, queue_size=10)

    while not rospy.is_shutdown():
        pub_rgb.publish(img_rgb_msg)
        pub_depth.publish(img_depth_msg)
        rospy.Rate(1.0).sleep()  # 1 Hz





def start_node():
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')
    



if __name__ == '__main__':
    try:
        start_node()
        import_img(rospy.myargv(argv=sys.argv)[1])
    except rospy.ROSInterruptException:
        pass



#/home/julius/Documents/Julius_03_x_auswertung/Julius_03_10/scenes/001_standing_coated/rgb/000016.png
