import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import sys

POSITIONS = {
    "1": {"x": 2.52, "y": 2.35},
    "2": {"x": 2.49, "y": -1.34}
}

class GoalSender(Node):
    def __init__(self):
        super().__init__('goal_sender')
        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y):
        self._client.wait_for_server()
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = float(x)
        goal.pose.pose.position.y = float(y)
        goal.pose.pose.orientation.w = 1.0
        future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info(f'Goal sent to ({x}, {y})')

def main():
    rclpy.init()
    node = GoalSender()
    pos = input("Enter position (1 or 2): ").strip()
    if pos in POSITIONS:
        coords = POSITIONS[pos]
        node.send_goal(coords["x"], coords["y"])
    else:
        print("Invalid — enter 1 or 2")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
