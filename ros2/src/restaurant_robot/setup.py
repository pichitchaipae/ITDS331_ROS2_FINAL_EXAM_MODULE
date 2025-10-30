from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'restaurant_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        ('share/' + package_name, ['package.xml']),
        # Install only canonical launch files (exclude deprecated rviz_scan.launch.py)
        (
            'share/' + package_name + '/launch',
            [
                f for f in glob('launch/*.launch.py')
                if not f.endswith('rviz_scan.launch.py')
            ],
        ),
        # Install only canonical config files
        (
            'share/' + package_name + '/config',
            [
                f for f in glob('config/*')
                if os.path.basename(f) in (
                    'slam_mapping.rviz',
                    'nav2.rviz',
                )
            ],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jao',
    maintainer_email='pichitchai.pae@student.mahidol.ac.th',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'order_server = restaurant_robot.order_server:main',
        ],
    },
)
