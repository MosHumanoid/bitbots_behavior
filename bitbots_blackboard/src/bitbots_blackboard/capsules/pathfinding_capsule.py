import rospy
import math

import tf2_ros
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class PathfindingCapsule:
    def __init__(self):
        # Thresholds to determine whether the transmitted goal is a new one
        self.tf_buffer = tf2_ros.Buffer(cache_time=rospy.Duration(2))
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.position_threshold = 0.3
        self.orientation_threshold = 10
        self.pathfinding_pub = None  # type: rospy.Publisher
        self.goal = None  # type: PoseStamped

    def publish(self, msg):
        # type: (PoseStamped) -> None
        map_goal = self.transform_goal_to_map(msg)
        if map_goal and self.is_new_goal_far_from_old_goal(map_goal):
            self.goal = map_goal
            self.pathfinding_pub.publish(self.fix_rotation(map_goal))

    def is_new_goal_far_from_old_goal(self, new_goal_msg):
        # type: (PoseStamped) -> bool
        if not self.goal:
            return True
        old_goal = self.goal
        old_position = old_goal.pose.position
        old_orientation = old_goal.pose.orientation
        old_orientation = euler_from_quaternion([old_orientation.x, old_orientation.y, old_orientation.z, old_orientation.w])
        new_position = new_goal_msg.pose.position
        new_orientation = new_goal_msg.pose.orientation
        new_orientation = euler_from_quaternion([new_orientation.x, new_orientation.y, new_orientation.z, new_orientation.w])

        # Calculate distance between the position
        position_distance = math.sqrt((old_position.x - new_position.x) ** 2 + (old_position.y - new_position.y) ** 2)
        orientation_distance = math.degrees(abs(old_orientation[2] - new_orientation[2]))
        return position_distance > self.position_threshold or orientation_distance > self.orientation_threshold

    def transform_goal_to_map(self, msg):
        # type: (PoseStamped) -> PoseStamped
        # transform local goal to goal in map frame
        if msg.header.frame_id == 'map':
            return msg
        else:
            try:
                msg.header.stamp = rospy.Time(0)
                map_goal = self.tf_buffer.transform(msg, 'map', timeout=rospy.Duration(0.5))
                e = euler_from_quaternion((map_goal.pose.orientation.x, map_goal.pose.orientation.y,
                                           map_goal.pose.orientation.z, map_goal.pose.orientation.w))
                q = quaternion_from_euler(0, 0, e[2])
                map_goal.pose.orientation.x = q[0]
                map_goal.pose.orientation.y = q[1]
                map_goal.pose.orientation.z = q[2]
                map_goal.pose.orientation.w = q[3]
                map_goal.pose.position.z = 0
                return map_goal
            except Exception as e:
                rospy.logwarn(e)
                return

    def fix_rotation(self, msg):
        # type: (PoseStamped) -> PoseStamped
        # this adds translatory movement to a rotation to fix a pathfinding issue
        if (msg.pose.position.x == 0 and msg.pose.position.y == 0 and
                not (msg.pose.orientation.x == 0 and msg.pose.orientation.y == 0 and msg.pose.orientation.z == 0)):
            msg.pose.position.x = 0.01
            msg.pose.position.y = 0.01
        return msg
