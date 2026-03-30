import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class Direction(Node):
    def __init__(self):
        super().__init__('direction')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        
        # 1. A dedicated motor timer running at 30Hz higher than the lidar that got 10Hz
        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)
        
        # 2. Store the "Target" speeds (what the brain wants)
        self.target_linear_x = 0.0
        self.target_angular_z = 0.0
        
        # 3. Store the "Current" speeds (what the wheels are actually doing)
        self.current_linear_x = 0.0
        self.current_angular_z = 0.0
        
        self.get_logger().info('Smooth Proportional Control Node Started!')

    def scan_callback(self, msg):
        # The LiDAR updates the "Target" variables at 10Hz
        front_left = msg.ranges[180:240]
        front_right = msg.ranges[120:180]
        
        valid_left = [r for r in front_left if not math.isinf(r) and not math.isnan(r) and r > 0.0]
        valid_right = [r for r in front_right if not math.isinf(r) and not math.isnan(r) and r > 0.0]
        
        min_left = min(valid_left) if valid_left else 10.0
        min_right = min(valid_right) if valid_right else 10.0
        min_distance = min(min_left, min_right)
        
        # TIER 1: EMERGENCY ESCAPE
        if min_distance < 0.7:
            self.target_linear_x = -0.15 
            self.target_angular_z = 2.0  
            
        # TIER 2: PROPORTIONAL SMOOTH STEERING
        elif min_distance < 2.5:
            self.target_linear_x = max(0.2, min_distance * 0.4) 
            difference = min_left - min_right
            curve_aggressiveness = 1.8 
            self.target_angular_z = difference * curve_aggressiveness
            
        # TIER 3: ALL CLEAR 
        else:
            self.target_linear_x = 1.5   
            self.target_angular_z = 0.0  

    def timer_callback(self):
        # This runs at 30Hz regardless of the LiDAR!
        # It smoothly blends the current speed toward the target speed (Linear Interpolation)
        smoothing_factor = 0.15  # Lower = smoother but slower to react. Higher = jerkier.
        
        self.current_linear_x += (self.target_linear_x - self.current_linear_x) * smoothing_factor
        self.current_angular_z += (self.target_angular_z - self.current_angular_z) * smoothing_factor
        
        twist = Twist()
        twist.linear.x = self.current_linear_x
        twist.angular.z = self.current_angular_z
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Direction()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()