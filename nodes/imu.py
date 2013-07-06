#!/usr/bin/python

import roslib; roslib.load_manifest('kingfisher_nmea')
import rospy

from nmea_helpers import TxHelper
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped
from math import degrees, pi

from tf.transformations import euler_from_quaternion


class RawIMU(TxHelper):
  SENTENCE = "IMU" 

  def __init__(self):
    rospy.Subscriber("imu/data", Imu, self._cb)

  def _cb(self, msg):
    self.tx(self.gps_time(msg.header.stamp),
        degrees(msg.angular_velocity.x),
        degrees(msg.angular_velocity.y),
        degrees(msg.angular_velocity.z),
        msg.linear_acceleration.x,
        msg.linear_acceleration.y,
        msg.linear_acceleration.z)


class RawCompass(TxHelper):
  SENTENCE = "RCM" 

  def __init__(self):
    rospy.Subscriber("imu/data", Imu, self._cb)
    self.compass_id = 0

  def _cb(self, msg):
    q = msg.orientation
    x, y, z = euler_from_quaternion([ getattr(q, f) for f in q.__slots__ ])
    z_ned = (pi/2) - z
    if z_ned < 0: z_ned += 2*pi

    self.tx(self.gps_time(),
        self.compass_id,
        degrees(z_ned),
        degrees(y),
        degrees(x),
        self.gps_time(msg.header.stamp))


if __name__ == "__main__":
  rospy.init_node('nmea_imu')
  RawCompass()
  RawIMU()
  rospy.spin()
