#!/usr/bin/env python3

# Imports
import rospy
from sam_slam_utils.sam_slam_ros_classes import sam_slam_listener
from sam_slam_utils.sam_slam_proc_classes import process_2d_data


def main():
    rospy.init_node('slam_listener', anonymous=True)
    rate = rospy.Rate(5)

    # Topic parameters
    ground_truth_topic = '/sam/sim/odom'
    dead_reckon_topic = '/sam/dr/odom'
    detection_topic = '/sam/payload/sidescan/detection_hypothesis'
    buoy_topic = '/sam/sim/marked_positions'
    frame = 'map'

    # Output parameters
    output_level = 3
    data_processed = False

    print('initializing listener')
    listener = sam_slam_listener(ground_truth_topic, dead_reckon_topic, detection_topic, buoy_topic, frame)

    while not rospy.is_shutdown():
        # Add the end of the run the listener will save its data, at this point we perform the offline slam
        if listener.data_written and not data_processed:
            print("Processing data")
            processing = process_2d_data(listener)
            processing.perform_offline_slam()
            processing.output_results(verbose_level=output_level)
            data_processed = True
        rate.sleep()


if __name__ == '__main__':
    main()
