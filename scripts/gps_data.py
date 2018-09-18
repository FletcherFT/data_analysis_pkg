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
    gpsDF = pd.DataFrame(columns=('timestamp','Latitude','Longitude','Altitude'))
    filterDF = pd.DataFrame(columns=('timestamp','Latitude','Longitude','Altitude'))
    with rosbag.Bag(args.inbag,'r') as inbagobj:
        for topic,msg,t in inbagobj.read_messages():
            if topic == "/ublox_gps/fix":
                tmp = pd.DataFrame({    'timestamp' : pd.Timestamp(msg.header.stamp.to_sec(),unit="s"),
                                        'Latitude' : msg.latitude,
                                        'Longitude' : msg.longitude,
                                        'Altitude' : msg.altitude},index=[0])
                gpsDF=gpsDF.append(tmp,sort=False,ignore_index=True)
            if topic == "/ublox_gps/filtered":
                tmp = pd.DataFrame({    'timestamp' : pd.Timestamp(msg.header.stamp.to_sec(),unit="s"),
                                        'Latitude' : msg.latitude,
                                        'Longitude' : msg.longitude,
                                        'Altitude' : msg.altitude},index=[0])
                filterDF=filterDF.append(tmp,sort=False,ignore_index=True)

    gpsDF.to_csv("raw_"+args.outcsv,index_label="seq")
    filterDF.to_csv("filtered_"+args.outcsv,index_label="seq")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Converts IMU readout to a csv form, also calculates the std deviation.')
    parser.add_argument('inbag', metavar='inbag', type=str, nargs='?',
        help='path to the input bag file')
    parser.add_argument('outcsv', metavar='outcsv', type=str, nargs='?',
        help='path for the output csv file')
    args = parser.parse_args()
    process(args)