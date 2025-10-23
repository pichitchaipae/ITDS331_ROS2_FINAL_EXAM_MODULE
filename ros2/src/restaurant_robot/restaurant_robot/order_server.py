import rclpy
from rclpy.node import Node
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer
import time

class RestaurantServer(Node):
    def __init__(self):
        super().__init__('restaurant_server')
        self._action_server = ActionServer(
            self, Fibonacci, 'serve_order', self.execute_callback)

    async def execute_callback(self, goal_handle):
        table_id = goal_handle.request.order
        feedback_msg = Fibonacci.Feedback()
        self.get_logger().info(f'รับออเดอร์จากโต๊ะ {table_id}')
        
        # ไปครัว
        feedback_msg.sequence = [1]
        self.get_logger().info('กำลังไปที่ครัว...')
        goal_handle.publish_feedback(feedback_msg)
        time.sleep(5)

        # ส่งอาหาร
        feedback_msg.sequence.append(2)
        self.get_logger().info(f'กำลังนำอาหารไปที่โต๊ะ {table_id}...')
        goal_handle.publish_feedback(feedback_msg)
        time.sleep(5)

        self.get_logger().info(f'เสิร์ฟอาหารที่โต๊ะ {table_id} เรียบร้อยแล้ว!')
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = [1, 2, 3]
        return result

def main(args=None):
    rclpy.init(args=args)
    node = RestaurantServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
