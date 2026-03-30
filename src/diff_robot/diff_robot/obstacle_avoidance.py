import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

class ObstacleAvoidance(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance')
        
        # Create a publisher to drive the robot
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Create a subscriber to read the LiDAR rays  data
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        
        self.get_logger().info('Autonomous Obstacle Avoidance Node Started!')

    def scan_callback(self, msg):
            #Look at the front 80 degrees 
            # so we don't clip corners when driving fast.
            front_rays = msg.ranges[140:220]
            
            # Filter out invalid or infinite values (rays that doesn't reflect anything )
            valid_rays = [r for r in front_rays if not math.isinf(r) and not math.isnan(r) and r > 0.0]
            
            # Default to 10 meters if no obstacle is seen
            min_distance = min(valid_rays) if valid_rays else 10.0
            
            twist = Twist()
            
            # determine an treshold distance for the robot to stop 
            # When the distance is lower than 0.8 the robot stop
            if min_distance < 0.8:  
                twist.linear.x = 0.0  # Stop going forward
                twist.angular.z = 1.0  # turning at 1 radians per second 
                self.get_logger().info(f'Obstacle ahead at {min_distance:.2f}m. Turning ...')

            
            else:
                twist.linear.x = 1.2   
                twist.angular.z = 0.0
                self.get_logger().info('The path is clear')

                
            # Send the command to the robot
            self.publisher_.publish(twist)

        

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidance()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()