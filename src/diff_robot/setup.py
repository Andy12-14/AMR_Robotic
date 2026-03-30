from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'diff_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # 1. Install Launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        
        # 2. Install Model/Xacro files
        (os.path.join('share', package_name, 'model'), glob('model/*')),
        
        # 3. Install Parameter/Bridge files
        (os.path.join('share', package_name, 'parameters'), glob('parameters/*.yaml')),

        # ADD THIS LINE: Installs your Gazebo worlds
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@todo.todo',
    description='Differential drive robot in Gazzy',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           'obstacle_avoidance = diff_robot.obstacle_avoidance:main',
           'direction = diff_robot.direction:main',
            # If you have python nodes, they go here
        ],
    },
)