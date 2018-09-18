#!/usr/bin/env python
# license removed for brevity
# This script calculates the standard deviation of an IMU recording.
import rosbag
#import rospy
import pandas as pd
import numpy as np
#from sensor_msgs.msg import Imu
import argparse
#import os
from tf_conversions import transformations as T

def process(args):
    ## DON'T ALTER ------------------------------------------------
    inbagobj = rosbag.Bag(args.inbag,'r')
    imuDF = pd.DataFrame(columns=('timestamp','phi','theta','psi','p','q','r','ax','ay','az'))
    with rosbag.Bag(args.inbag,'r') as inbagobj:
        for topic,msg,t in inbagobj.read_messages():
            if topic == "/imu/data":
                quat = (msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w)
                eul = T.euler_from_quaternion(quat,axes='sxyz')
                t = msg.header.stamp
                tmp = pd.DataFrame({    'timestamp' : pd.Timestamp(t.to_sec(),unit="s"),
                                        'phi' : eul[0],
                                        'theta' : eul[1],
                                        'psi' : eul[2],
                                        'p' : msg.angular_velocity.x,
                                        'q' : msg.angular_velocity.y,
                                        'r' : msg.angular_velocity.z,
                                        'ax' : msg.linear_acceleration.x,
                                        'ay' : msg.linear_acceleration.y,
                                        'az' : msg.linear_acceleration.z},index=[0])
                imuDF=imuDF.append(tmp,sort=False,ignore_index=True)
    imuDF.to_csv(args.outcsv)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Converts IMU readout to a csv form, also calculates the std deviation.')
    parser.add_argument('inbag', metavar='inbag', type=str, nargs='?',
        help='path to the input bag file')
    parser.add_argument('outcsv', metavar='outcsv', type=str, nargs='?',
        help='path for the output csv file')
    args = parser.parse_args()
    process(args)