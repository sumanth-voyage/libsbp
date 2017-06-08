#!/usr/bin/env python
# Copyright (C) 2015-2018 Swift Navigation Inc.
# Contact: Swift Navigation <dev@swiftnav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.


"""
Geodetic navigation messages reporting GPS time, position, velocity,
and baseline position solutions. For position solutions, these
messages define several different position solutions: single-point
(SPP), RTK, and pseudo-absolute position solutions.

The SPP is the standalone, absolute GPS position solution using only
a single receiver. The RTK solution is the differential GPS
solution, which can use either a fixed/integer or floating carrier
phase ambiguity. The pseudo-absolute position solution uses a
user-provided, well-surveyed base station position (if available)
and the RTK solution in tandem.

When the inertial navigation mode indicates that the IMU is used,
all messages are reported in the vehicle body frame as defined by
device settings.  By default, the vehicle body frame is configured to be
coincident with the antenna phase center.  When there is no inertial
navigation, the solution will be reported at the phase center of the antenna.
There is no inertial navigation capability on Piksi Multi or Duro. 

"""

import construct
import json
from sbp.msg import SBP, SENDER_ID, TYPES_NP, TYPES_KEYS_NP
from sbp.utils import fmt_repr, exclude_fields, walk_json_dict, containerize,\
                      greedy_string
import numpy as np
import traceback

# Automatically generated from piksi/yaml/swiftnav/sbp/navigation.yaml with generate.py.
# Please do not hand edit!


SBP_MSG_GPS_TIME = 0x0102
class MsgGPSTime(SBP):
  """SBP class for message MSG_GPS_TIME (0x0102).

  You can have MSG_GPS_TIME inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the GPS time, representing the time since
the GPS epoch began on midnight January 6, 1980 UTC. GPS time
counts the weeks and seconds of the week. The weeks begin at the
Saturday/Sunday transition. GPS week 0 began at the beginning of
the GPS time scale.

Within each week number, the GPS time of the week is between
between 0 and 604800 seconds (=60*60*24*7). Note that GPS time
does not accumulate leap seconds, and as of now, has a small
offset from UTC. In a message stream, this message precedes a
set of other navigation messages referenced to the same time
(but lacking the ns field) and indicates a more precise time of
these messages.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  wn : int
    GPS week number
  tow : int
    GPS time of week rounded to the nearest millisecond
  ns_residual : int
    Nanosecond residual of millisecond-rounded TOW (ranges
from -500000 to 500000)

  flags : int
    Status flags (reserved)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'wn' / construct.Int16ul,
                   'tow' / construct.Int32ul,
                   'ns_residual' / construct.Int32sl,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'wn',
               'tow',
               'ns_residual',
               'flags',
              ]
  _fields = [
             ( 'u16', 'wn' ),
             ( 'u32', 'tow' ),
             ( 's32', 'ns_residual' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgGPSTime,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgGPSTime, self).__init__()
      self.msg_type = SBP_MSG_GPS_TIME
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.wn = kwargs.pop('wn')
      self.tow = kwargs.pop('tow')
      self.ns_residual = kwargs.pop('ns_residual')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgGPSTime.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgGPSTime(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgGPSTime._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgGPSTime, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_UTC_TIME = 0x0103
class MsgUtcTime(SBP):
  """SBP class for message MSG_UTC_TIME (0x0103).

  You can have MSG_UTC_TIME inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the Universal Coordinated Time (UTC).  Note the flags
which indicate the source of the UTC offset value and source of the time fix.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  flags : int
    Indicates source and time validity
  tow : int
    GPS time of week rounded to the nearest millisecond
  year : int
    Year
  month : int
    Month (range 1 .. 12)
  day : int
    days in the month (range 1-31)
  hours : int
    hours of day (range 0-23)
  minutes : int
    minutes of hour (range 0-59)
  seconds : int
    seconds of minute (range 0-60) rounded down
  ns : int
    nanoseconds of second (range 0-999999999)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'flags' / construct.Int8ul,
                   'tow' / construct.Int32ul,
                   'year' / construct.Int16ul,
                   'month' / construct.Int8ul,
                   'day' / construct.Int8ul,
                   'hours' / construct.Int8ul,
                   'minutes' / construct.Int8ul,
                   'seconds' / construct.Int8ul,
                   'ns' / construct.Int32ul,)
  __slots__ = [
               'flags',
               'tow',
               'year',
               'month',
               'day',
               'hours',
               'minutes',
               'seconds',
               'ns',
              ]
  _fields = [
             ( 'u8', 'flags' ),
             ( 'u32', 'tow' ),
             ( 'u16', 'year' ),
             ( 'u8', 'month' ),
             ( 'u8', 'day' ),
             ( 'u8', 'hours' ),
             ( 'u8', 'minutes' ),
             ( 'u8', 'seconds' ),
             ( 'u32', 'ns' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgUtcTime,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgUtcTime, self).__init__()
      self.msg_type = SBP_MSG_UTC_TIME
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.flags = kwargs.pop('flags')
      self.tow = kwargs.pop('tow')
      self.year = kwargs.pop('year')
      self.month = kwargs.pop('month')
      self.day = kwargs.pop('day')
      self.hours = kwargs.pop('hours')
      self.minutes = kwargs.pop('minutes')
      self.seconds = kwargs.pop('seconds')
      self.ns = kwargs.pop('ns')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgUtcTime.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgUtcTime(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgUtcTime._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgUtcTime, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_DOPS = 0x0208
class MsgDops(SBP):
  """SBP class for message MSG_DOPS (0x0208).

  You can have MSG_DOPS inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This dilution of precision (DOP) message describes the effect of
navigation satellite geometry on positional measurement
precision.  The flags field indicated whether the DOP reported
corresponds to differential or SPP solution.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  gdop : int
    Geometric Dilution of Precision
  pdop : int
    Position Dilution of Precision
  tdop : int
    Time Dilution of Precision
  hdop : int
    Horizontal Dilution of Precision
  vdop : int
    Vertical Dilution of Precision
  flags : int
    Indicates the position solution with which the DOPS message corresponds
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'gdop' / construct.Int16ul,
                   'pdop' / construct.Int16ul,
                   'tdop' / construct.Int16ul,
                   'hdop' / construct.Int16ul,
                   'vdop' / construct.Int16ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'gdop',
               'pdop',
               'tdop',
               'hdop',
               'vdop',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'u16', 'gdop' ),
             ( 'u16', 'pdop' ),
             ( 'u16', 'tdop' ),
             ( 'u16', 'hdop' ),
             ( 'u16', 'vdop' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgDops,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgDops, self).__init__()
      self.msg_type = SBP_MSG_DOPS
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.gdop = kwargs.pop('gdop')
      self.pdop = kwargs.pop('pdop')
      self.tdop = kwargs.pop('tdop')
      self.hdop = kwargs.pop('hdop')
      self.vdop = kwargs.pop('vdop')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgDops.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgDops(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgDops._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgDops, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_ECEF = 0x0209
class MsgPosECEF(SBP):
  """SBP class for message MSG_POS_ECEF (0x0209).

  You can have MSG_POS_ECEF inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  The position solution message reports absolute Earth Centered
Earth Fixed (ECEF) coordinates and the status (single point vs
pseudo-absolute RTK) of the position solution. If the rover
receiver knows the surveyed position of the base station and has
an RTK solution, this reports a pseudo-absolute position
solution using the base station position and the rover's RTK
baseline vector. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : double
    ECEF X coordinate
  y : double
    ECEF Y coordinate
  z : double
    ECEF Z coordinate
  accuracy : int
    Position estimated standard deviation
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Float64l,
                   'y' / construct.Float64l,
                   'z' / construct.Float64l,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'x' ),
             ( 'double', 'y' ),
             ( 'double', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosECEF,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosECEF, self).__init__()
      self.msg_type = SBP_MSG_POS_ECEF
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosECEF.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosECEF(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosECEF._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosECEF, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_ECEF_COV = 0x0214
class MsgPosECEFCov(SBP):
  """SBP class for message MSG_POS_ECEF_COV (0x0214).

  You can have MSG_POS_ECEF_COV inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  The position solution message reports absolute Earth Centered
Earth Fixed (ECEF) coordinates and the status (single point vs
pseudo-absolute RTK) of the position solution. The message also
reports the upper triangular portion of the 3x3 covariance matrix.
If the receiver knows the surveyed position of the base station and has
an RTK solution, this reports a pseudo-absolute position
solution using the base station position and the rover's RTK
baseline vector. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : double
    ECEF X coordinate
  y : double
    ECEF Y coordinate
  z : double
    ECEF Z coordinate
  cov_x_x : float
    Estimated variance of x
  cov_x_y : float
    Estimated covariance of x and y
  cov_x_z : float
    Estimated covariance of x and z
  cov_y_y : float
    Estimated variance of y
  cov_y_z : float
    Estimated covariance of y and z
  cov_z_z : float
    Estimated variance of z
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Float64l,
                   'y' / construct.Float64l,
                   'z' / construct.Float64l,
                   'cov_x_x' / construct.Float32l,
                   'cov_x_y' / construct.Float32l,
                   'cov_x_z' / construct.Float32l,
                   'cov_y_y' / construct.Float32l,
                   'cov_y_z' / construct.Float32l,
                   'cov_z_z' / construct.Float32l,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'cov_x_x',
               'cov_x_y',
               'cov_x_z',
               'cov_y_y',
               'cov_y_z',
               'cov_z_z',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'x' ),
             ( 'double', 'y' ),
             ( 'double', 'z' ),
             ( 'float', 'cov_x_x' ),
             ( 'float', 'cov_x_y' ),
             ( 'float', 'cov_x_z' ),
             ( 'float', 'cov_y_y' ),
             ( 'float', 'cov_y_z' ),
             ( 'float', 'cov_z_z' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosECEFCov,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosECEFCov, self).__init__()
      self.msg_type = SBP_MSG_POS_ECEF_COV
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.cov_x_x = kwargs.pop('cov_x_x')
      self.cov_x_y = kwargs.pop('cov_x_y')
      self.cov_x_z = kwargs.pop('cov_x_z')
      self.cov_y_y = kwargs.pop('cov_y_y')
      self.cov_y_z = kwargs.pop('cov_y_z')
      self.cov_z_z = kwargs.pop('cov_z_z')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosECEFCov.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosECEFCov(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosECEFCov._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosECEFCov, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_LLH = 0x020A
class MsgPosLLH(SBP):
  """SBP class for message MSG_POS_LLH (0x020A).

  You can have MSG_POS_LLH inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This position solution message reports the absolute geodetic
coordinates and the status (single point vs pseudo-absolute RTK)
of the position solution. If the rover receiver knows the
surveyed position of the base station and has an RTK solution,
this reports a pseudo-absolute position solution using the base
station position and the rover's RTK baseline vector. The full
GPS time is given by the preceding MSG_GPS_TIME with the
matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  lat : double
    Latitude
  lon : double
    Longitude
  height : double
    Height above WGS84 ellipsoid
  h_accuracy : int
    Horizontal position estimated standard deviation
  v_accuracy : int
    Vertical position estimated standard deviation
  n_sats : int
    Number of satellites used in solution.
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'lat' / construct.Float64l,
                   'lon' / construct.Float64l,
                   'height' / construct.Float64l,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'lat',
               'lon',
               'height',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'lat' ),
             ( 'double', 'lon' ),
             ( 'double', 'height' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosLLH,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosLLH, self).__init__()
      self.msg_type = SBP_MSG_POS_LLH
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.lat = kwargs.pop('lat')
      self.lon = kwargs.pop('lon')
      self.height = kwargs.pop('height')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosLLH.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosLLH(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosLLH._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosLLH, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_LLH_COV = 0x0211
class MsgPosLLHCov(SBP):
  """SBP class for message MSG_POS_LLH_COV (0x0211).

  You can have MSG_POS_LLH_COV inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This position solution message reports the absolute geodetic
coordinates and the status (single point vs pseudo-absolute RTK)
of the position solution as well as the upper triangle of the 3x3
covariance matrix.  The position information and Fix Mode flags should
follow the MSG_POS_LLH message.  Since the covariance matrix is computed
in the local-level North, East, Down frame, the covariance terms follow
with that convention. Thus, covariances are reported against the "downward"
measurement and care should be taken with the sign convention.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  lat : double
    Latitude
  lon : double
    Longitude
  height : double
    Height above WGS84 ellipsoid
  cov_n_n : float
    Estimated variance of northing
  cov_n_e : float
    Covariance of northing and easting
  cov_n_d : float
    Covariance of northing and downward measurement
  cov_e_e : float
    Estimated variance of easting
  cov_e_d : float
    Covariance of easting and downward measurement
  cov_d_d : float
    Estimated variance of downward measurement
  n_sats : int
    Number of satellites used in solution.
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'lat' / construct.Float64l,
                   'lon' / construct.Float64l,
                   'height' / construct.Float64l,
                   'cov_n_n' / construct.Float32l,
                   'cov_n_e' / construct.Float32l,
                   'cov_n_d' / construct.Float32l,
                   'cov_e_e' / construct.Float32l,
                   'cov_e_d' / construct.Float32l,
                   'cov_d_d' / construct.Float32l,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'lat',
               'lon',
               'height',
               'cov_n_n',
               'cov_n_e',
               'cov_n_d',
               'cov_e_e',
               'cov_e_d',
               'cov_d_d',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'lat' ),
             ( 'double', 'lon' ),
             ( 'double', 'height' ),
             ( 'float', 'cov_n_n' ),
             ( 'float', 'cov_n_e' ),
             ( 'float', 'cov_n_d' ),
             ( 'float', 'cov_e_e' ),
             ( 'float', 'cov_e_d' ),
             ( 'float', 'cov_d_d' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosLLHCov,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosLLHCov, self).__init__()
      self.msg_type = SBP_MSG_POS_LLH_COV
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.lat = kwargs.pop('lat')
      self.lon = kwargs.pop('lon')
      self.height = kwargs.pop('height')
      self.cov_n_n = kwargs.pop('cov_n_n')
      self.cov_n_e = kwargs.pop('cov_n_e')
      self.cov_n_d = kwargs.pop('cov_n_d')
      self.cov_e_e = kwargs.pop('cov_e_e')
      self.cov_e_d = kwargs.pop('cov_e_d')
      self.cov_d_d = kwargs.pop('cov_d_d')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosLLHCov.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosLLHCov(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosLLHCov._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosLLHCov, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_BASELINE_ECEF = 0x020B
class MsgBaselineECEF(SBP):
  """SBP class for message MSG_BASELINE_ECEF (0x020B).

  You can have MSG_BASELINE_ECEF inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the baseline solution in Earth Centered
Earth Fixed (ECEF) coordinates. This baseline is the relative
vector distance from the base station to the rover receiver. The
full GPS time is given by the preceding MSG_GPS_TIME with the
matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Baseline ECEF X coordinate
  y : int
    Baseline ECEF Y coordinate
  z : int
    Baseline ECEF Z coordinate
  accuracy : int
    Position estimated standard deviation
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgBaselineECEF,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgBaselineECEF, self).__init__()
      self.msg_type = SBP_MSG_BASELINE_ECEF
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgBaselineECEF.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgBaselineECEF(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgBaselineECEF._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgBaselineECEF, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_BASELINE_NED = 0x020C
class MsgBaselineNED(SBP):
  """SBP class for message MSG_BASELINE_NED (0x020C).

  You can have MSG_BASELINE_NED inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the baseline solution in North East Down
(NED) coordinates. This baseline is the relative vector distance
from the base station to the rover receiver, and NED coordinate
system is defined at the local WGS84 tangent plane centered at the
base station position.  The full GPS time is given by the
preceding MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  n : int
    Baseline North coordinate
  e : int
    Baseline East coordinate
  d : int
    Baseline Down coordinate
  h_accuracy : int
    Horizontal position estimated standard deviation
  v_accuracy : int
    Vertical position estimated standard deviation
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'n' / construct.Int32sl,
                   'e' / construct.Int32sl,
                   'd' / construct.Int32sl,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'n',
               'e',
               'd',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'n' ),
             ( 's32', 'e' ),
             ( 's32', 'd' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgBaselineNED,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgBaselineNED, self).__init__()
      self.msg_type = SBP_MSG_BASELINE_NED
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.n = kwargs.pop('n')
      self.e = kwargs.pop('e')
      self.d = kwargs.pop('d')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgBaselineNED.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgBaselineNED(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgBaselineNED._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgBaselineNED, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_ECEF = 0x020D
class MsgVelECEF(SBP):
  """SBP class for message MSG_VEL_ECEF (0x020D).

  You can have MSG_VEL_ECEF inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in Earth Centered Earth Fixed
(ECEF) coordinates. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Velocity ECEF X coordinate
  y : int
    Velocity ECEF Y coordinate
  z : int
    Velocity ECEF Z coordinate
  accuracy : int
    Velocity estimated standard deviation

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelECEF,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelECEF, self).__init__()
      self.msg_type = SBP_MSG_VEL_ECEF
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelECEF.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelECEF(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelECEF._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelECEF, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_ECEF_COV = 0x0215
class MsgVelECEFCov(SBP):
  """SBP class for message MSG_VEL_ECEF_COV (0x0215).

  You can have MSG_VEL_ECEF_COV inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in Earth Centered Earth Fixed
(ECEF) coordinates. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Velocity ECEF X coordinate
  y : int
    Velocity ECEF Y coordinate
  z : int
    Velocity ECEF Z coordinate
  cov_x_x : float
    Estimated variance of x
  cov_x_y : float
    Estimated covariance of x and y
  cov_x_z : float
    Estimated covariance of x and z
  cov_y_y : float
    Estimated variance of y
  cov_y_z : float
    Estimated covariance of y and z
  cov_z_z : float
    Estimated variance of z
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'cov_x_x' / construct.Float32l,
                   'cov_x_y' / construct.Float32l,
                   'cov_x_z' / construct.Float32l,
                   'cov_y_y' / construct.Float32l,
                   'cov_y_z' / construct.Float32l,
                   'cov_z_z' / construct.Float32l,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'cov_x_x',
               'cov_x_y',
               'cov_x_z',
               'cov_y_y',
               'cov_y_z',
               'cov_z_z',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'float', 'cov_x_x' ),
             ( 'float', 'cov_x_y' ),
             ( 'float', 'cov_x_z' ),
             ( 'float', 'cov_y_y' ),
             ( 'float', 'cov_y_z' ),
             ( 'float', 'cov_z_z' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelECEFCov,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelECEFCov, self).__init__()
      self.msg_type = SBP_MSG_VEL_ECEF_COV
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.cov_x_x = kwargs.pop('cov_x_x')
      self.cov_x_y = kwargs.pop('cov_x_y')
      self.cov_x_z = kwargs.pop('cov_x_z')
      self.cov_y_y = kwargs.pop('cov_y_y')
      self.cov_y_z = kwargs.pop('cov_y_z')
      self.cov_z_z = kwargs.pop('cov_z_z')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelECEFCov.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelECEFCov(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelECEFCov._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelECEFCov, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_NED = 0x020E
class MsgVelNED(SBP):
  """SBP class for message MSG_VEL_NED (0x020E).

  You can have MSG_VEL_NED inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in local North East Down (NED)
coordinates. The NED coordinate system is defined as the local WGS84
tangent plane centered at the current position. The full GPS time is
given by the preceding MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  n : int
    Velocity North coordinate
  e : int
    Velocity East coordinate
  d : int
    Velocity Down coordinate
  h_accuracy : int
    Horizontal velocity estimated standard deviation

  v_accuracy : int
    Vertical velocity estimated standard deviation

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'n' / construct.Int32sl,
                   'e' / construct.Int32sl,
                   'd' / construct.Int32sl,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'n',
               'e',
               'd',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'n' ),
             ( 's32', 'e' ),
             ( 's32', 'd' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelNED,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelNED, self).__init__()
      self.msg_type = SBP_MSG_VEL_NED
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.n = kwargs.pop('n')
      self.e = kwargs.pop('e')
      self.d = kwargs.pop('d')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelNED.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelNED(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelNED._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelNED, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_NED_COV = 0x0212
class MsgVelNEDCov(SBP):
  """SBP class for message MSG_VEL_NED_COV (0x0212).

  You can have MSG_VEL_NED_COV inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in local North East Down (NED)
coordinates. The NED coordinate system is defined as the local WGS84
tangent plane centered at the current position. The full GPS time is
given by the preceding MSG_GPS_TIME with the matching time-of-week (tow).
This message is similar to the MSG_VEL_NED, but it includes the upper triangular
portion of the 3x3 covariance matrix.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  n : int
    Velocity North coordinate
  e : int
    Velocity East coordinate
  d : int
    Velocity Down coordinate
  cov_n_n : float
    Estimated variance of northward measurement
  cov_n_e : float
    Covariance of northward and eastward measurement
  cov_n_d : float
    Covariance of northward and downward measurement
  cov_e_e : float
    Estimated variance of eastward measurement
  cov_e_d : float
    Covariance of eastward and downward measurement
  cov_d_d : float
    Estimated variance of downward measurement
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'n' / construct.Int32sl,
                   'e' / construct.Int32sl,
                   'd' / construct.Int32sl,
                   'cov_n_n' / construct.Float32l,
                   'cov_n_e' / construct.Float32l,
                   'cov_n_d' / construct.Float32l,
                   'cov_e_e' / construct.Float32l,
                   'cov_e_d' / construct.Float32l,
                   'cov_d_d' / construct.Float32l,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'n',
               'e',
               'd',
               'cov_n_n',
               'cov_n_e',
               'cov_n_d',
               'cov_e_e',
               'cov_e_d',
               'cov_d_d',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'n' ),
             ( 's32', 'e' ),
             ( 's32', 'd' ),
             ( 'float', 'cov_n_n' ),
             ( 'float', 'cov_n_e' ),
             ( 'float', 'cov_n_d' ),
             ( 'float', 'cov_e_e' ),
             ( 'float', 'cov_e_d' ),
             ( 'float', 'cov_d_d' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelNEDCov,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelNEDCov, self).__init__()
      self.msg_type = SBP_MSG_VEL_NED_COV
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.n = kwargs.pop('n')
      self.e = kwargs.pop('e')
      self.d = kwargs.pop('d')
      self.cov_n_n = kwargs.pop('cov_n_n')
      self.cov_n_e = kwargs.pop('cov_n_e')
      self.cov_n_d = kwargs.pop('cov_n_d')
      self.cov_e_e = kwargs.pop('cov_e_e')
      self.cov_e_d = kwargs.pop('cov_e_d')
      self.cov_d_d = kwargs.pop('cov_d_d')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelNEDCov.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelNEDCov(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelNEDCov._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelNEDCov, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_BODY = 0x0213
class MsgVelBody(SBP):
  """SBP class for message MSG_VEL_BODY (0x0213).

  You can have MSG_VEL_BODY inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in the Vehicle Body Frame. By convention,
the x-axis should point out the nose of the vehicle and represent the forward
direction, while as the y-axis should point out the right hand side of the vehicle.
Since this is a right handed system, z should point out the bottom of the vehicle.
The orientation and origin of the Vehicle Body Frame are specified via the device settings.
The full GPS time is given by the preceding MSG_GPS_TIME with the
matching time-of-week (tow). This message is only produced by inertial versions of Swift
products and is not available from Piksi Multi or Duro.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Velocity in x direction
  y : int
    Velocity in y direction
  z : int
    Velocity in z direction
  cov_x_x : float
    Estimated variance of x
  cov_x_y : float
    Covariance of x and y
  cov_x_z : float
    Covariance of x and z
  cov_y_y : float
    Estimated variance of y
  cov_y_z : float
    Covariance of y and z
  cov_z_z : float
    Estimated variance of z
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'cov_x_x' / construct.Float32l,
                   'cov_x_y' / construct.Float32l,
                   'cov_x_z' / construct.Float32l,
                   'cov_y_y' / construct.Float32l,
                   'cov_y_z' / construct.Float32l,
                   'cov_z_z' / construct.Float32l,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'cov_x_x',
               'cov_x_y',
               'cov_x_z',
               'cov_y_y',
               'cov_y_z',
               'cov_z_z',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'float', 'cov_x_x' ),
             ( 'float', 'cov_x_y' ),
             ( 'float', 'cov_x_z' ),
             ( 'float', 'cov_y_y' ),
             ( 'float', 'cov_y_z' ),
             ( 'float', 'cov_z_z' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelBody,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelBody, self).__init__()
      self.msg_type = SBP_MSG_VEL_BODY
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.cov_x_x = kwargs.pop('cov_x_x')
      self.cov_x_y = kwargs.pop('cov_x_y')
      self.cov_x_z = kwargs.pop('cov_x_z')
      self.cov_y_y = kwargs.pop('cov_y_y')
      self.cov_y_z = kwargs.pop('cov_y_z')
      self.cov_z_z = kwargs.pop('cov_z_z')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelBody.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelBody(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelBody._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelBody, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_AGE_CORRECTIONS = 0x0210
class MsgAgeCorrections(SBP):
  """SBP class for message MSG_AGE_CORRECTIONS (0x0210).

  You can have MSG_AGE_CORRECTIONS inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the Age of the corrections used for the current
Differential solution


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  age : int
    Age of the corrections (0xFFFF indicates invalid)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'age' / construct.Int16ul,)
  __slots__ = [
               'tow',
               'age',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'u16', 'age' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgAgeCorrections,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgAgeCorrections, self).__init__()
      self.msg_type = SBP_MSG_AGE_CORRECTIONS
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.age = kwargs.pop('age')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgAgeCorrections.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgAgeCorrections(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgAgeCorrections._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgAgeCorrections, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_GPS_TIME_DEP_A = 0x0100
class MsgGPSTimeDepA(SBP):
  """SBP class for message MSG_GPS_TIME_DEP_A (0x0100).

  You can have MSG_GPS_TIME_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the GPS time, representing the time since
the GPS epoch began on midnight January 6, 1980 UTC. GPS time
counts the weeks and seconds of the week. The weeks begin at the
Saturday/Sunday transition. GPS week 0 began at the beginning of
the GPS time scale.

Within each week number, the GPS time of the week is between
between 0 and 604800 seconds (=60*60*24*7). Note that GPS time
does not accumulate leap seconds, and as of now, has a small
offset from UTC. In a message stream, this message precedes a
set of other navigation messages referenced to the same time
(but lacking the ns field) and indicates a more precise time of
these messages.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  wn : int
    GPS week number
  tow : int
    GPS time of week rounded to the nearest millisecond
  ns_residual : int
    Nanosecond residual of millisecond-rounded TOW (ranges
from -500000 to 500000)

  flags : int
    Status flags (reserved)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'wn' / construct.Int16ul,
                   'tow' / construct.Int32ul,
                   'ns_residual' / construct.Int32sl,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'wn',
               'tow',
               'ns_residual',
               'flags',
              ]
  _fields = [
             ( 'u16', 'wn' ),
             ( 'u32', 'tow' ),
             ( 's32', 'ns_residual' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgGPSTimeDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgGPSTimeDepA, self).__init__()
      self.msg_type = SBP_MSG_GPS_TIME_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.wn = kwargs.pop('wn')
      self.tow = kwargs.pop('tow')
      self.ns_residual = kwargs.pop('ns_residual')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgGPSTimeDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgGPSTimeDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgGPSTimeDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgGPSTimeDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_DOPS_DEP_A = 0x0206
class MsgDopsDepA(SBP):
  """SBP class for message MSG_DOPS_DEP_A (0x0206).

  You can have MSG_DOPS_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This dilution of precision (DOP) message describes the effect of
navigation satellite geometry on positional measurement
precision.


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  gdop : int
    Geometric Dilution of Precision
  pdop : int
    Position Dilution of Precision
  tdop : int
    Time Dilution of Precision
  hdop : int
    Horizontal Dilution of Precision
  vdop : int
    Vertical Dilution of Precision
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'gdop' / construct.Int16ul,
                   'pdop' / construct.Int16ul,
                   'tdop' / construct.Int16ul,
                   'hdop' / construct.Int16ul,
                   'vdop' / construct.Int16ul,)
  __slots__ = [
               'tow',
               'gdop',
               'pdop',
               'tdop',
               'hdop',
               'vdop',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'u16', 'gdop' ),
             ( 'u16', 'pdop' ),
             ( 'u16', 'tdop' ),
             ( 'u16', 'hdop' ),
             ( 'u16', 'vdop' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgDopsDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgDopsDepA, self).__init__()
      self.msg_type = SBP_MSG_DOPS_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.gdop = kwargs.pop('gdop')
      self.pdop = kwargs.pop('pdop')
      self.tdop = kwargs.pop('tdop')
      self.hdop = kwargs.pop('hdop')
      self.vdop = kwargs.pop('vdop')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgDopsDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgDopsDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgDopsDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgDopsDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_ECEF_DEP_A = 0x0200
class MsgPosECEFDepA(SBP):
  """SBP class for message MSG_POS_ECEF_DEP_A (0x0200).

  You can have MSG_POS_ECEF_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  The position solution message reports absolute Earth Centered
Earth Fixed (ECEF) coordinates and the status (single point vs
pseudo-absolute RTK) of the position solution. If the rover
receiver knows the surveyed position of the base station and has
an RTK solution, this reports a pseudo-absolute position
solution using the base station position and the rover's RTK
baseline vector. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : double
    ECEF X coordinate
  y : double
    ECEF Y coordinate
  z : double
    ECEF Z coordinate
  accuracy : int
    Position accuracy estimate (not implemented). Defaults
to 0.

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Float64l,
                   'y' / construct.Float64l,
                   'z' / construct.Float64l,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'x' ),
             ( 'double', 'y' ),
             ( 'double', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosECEFDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosECEFDepA, self).__init__()
      self.msg_type = SBP_MSG_POS_ECEF_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosECEFDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosECEFDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosECEFDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosECEFDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_POS_LLH_DEP_A = 0x0201
class MsgPosLLHDepA(SBP):
  """SBP class for message MSG_POS_LLH_DEP_A (0x0201).

  You can have MSG_POS_LLH_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This position solution message reports the absolute geodetic
coordinates and the status (single point vs pseudo-absolute RTK)
of the position solution. If the rover receiver knows the
surveyed position of the base station and has an RTK solution,
this reports a pseudo-absolute position solution using the base
station position and the rover's RTK baseline vector. The full
GPS time is given by the preceding MSG_GPS_TIME with the
matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  lat : double
    Latitude
  lon : double
    Longitude
  height : double
    Height
  h_accuracy : int
    Horizontal position accuracy estimate (not
implemented). Defaults to 0.

  v_accuracy : int
    Vertical position accuracy estimate (not
implemented). Defaults to 0.

  n_sats : int
    Number of satellites used in solution.
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'lat' / construct.Float64l,
                   'lon' / construct.Float64l,
                   'height' / construct.Float64l,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'lat',
               'lon',
               'height',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'double', 'lat' ),
             ( 'double', 'lon' ),
             ( 'double', 'height' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgPosLLHDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgPosLLHDepA, self).__init__()
      self.msg_type = SBP_MSG_POS_LLH_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.lat = kwargs.pop('lat')
      self.lon = kwargs.pop('lon')
      self.height = kwargs.pop('height')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgPosLLHDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgPosLLHDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgPosLLHDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgPosLLHDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_BASELINE_ECEF_DEP_A = 0x0202
class MsgBaselineECEFDepA(SBP):
  """SBP class for message MSG_BASELINE_ECEF_DEP_A (0x0202).

  You can have MSG_BASELINE_ECEF_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the baseline solution in Earth Centered
Earth Fixed (ECEF) coordinates. This baseline is the relative
vector distance from the base station to the rover receiver. The
full GPS time is given by the preceding MSG_GPS_TIME with the
matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Baseline ECEF X coordinate
  y : int
    Baseline ECEF Y coordinate
  z : int
    Baseline ECEF Z coordinate
  accuracy : int
    Position accuracy estimate

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgBaselineECEFDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgBaselineECEFDepA, self).__init__()
      self.msg_type = SBP_MSG_BASELINE_ECEF_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgBaselineECEFDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgBaselineECEFDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgBaselineECEFDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgBaselineECEFDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_BASELINE_NED_DEP_A = 0x0203
class MsgBaselineNEDDepA(SBP):
  """SBP class for message MSG_BASELINE_NED_DEP_A (0x0203).

  You can have MSG_BASELINE_NED_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the baseline solution in North East Down
(NED) coordinates. This baseline is the relative vector distance
from the base station to the rover receiver, and NED coordinate
system is defined at the local WGS84 tangent plane centered at the
base station position.  The full GPS time is given by the
preceding MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  n : int
    Baseline North coordinate
  e : int
    Baseline East coordinate
  d : int
    Baseline Down coordinate
  h_accuracy : int
    Horizontal position accuracy estimate (not
implemented). Defaults to 0.

  v_accuracy : int
    Vertical position accuracy estimate (not
implemented). Defaults to 0.

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'n' / construct.Int32sl,
                   'e' / construct.Int32sl,
                   'd' / construct.Int32sl,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'n',
               'e',
               'd',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'n' ),
             ( 's32', 'e' ),
             ( 's32', 'd' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgBaselineNEDDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgBaselineNEDDepA, self).__init__()
      self.msg_type = SBP_MSG_BASELINE_NED_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.n = kwargs.pop('n')
      self.e = kwargs.pop('e')
      self.d = kwargs.pop('d')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgBaselineNEDDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgBaselineNEDDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgBaselineNEDDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgBaselineNEDDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_ECEF_DEP_A = 0x0204
class MsgVelECEFDepA(SBP):
  """SBP class for message MSG_VEL_ECEF_DEP_A (0x0204).

  You can have MSG_VEL_ECEF_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in Earth Centered Earth Fixed
(ECEF) coordinates. The full GPS time is given by the preceding
MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  x : int
    Velocity ECEF X coordinate
  y : int
    Velocity ECEF Y coordinate
  z : int
    Velocity ECEF Z coordinate
  accuracy : int
    Velocity accuracy estimate (not implemented). Defaults
to 0.

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags (reserved)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'x' / construct.Int32sl,
                   'y' / construct.Int32sl,
                   'z' / construct.Int32sl,
                   'accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'x',
               'y',
               'z',
               'accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'x' ),
             ( 's32', 'y' ),
             ( 's32', 'z' ),
             ( 'u16', 'accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelECEFDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelECEFDepA, self).__init__()
      self.msg_type = SBP_MSG_VEL_ECEF_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.x = kwargs.pop('x')
      self.y = kwargs.pop('y')
      self.z = kwargs.pop('z')
      self.accuracy = kwargs.pop('accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelECEFDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelECEFDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelECEFDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelECEFDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_VEL_NED_DEP_A = 0x0205
class MsgVelNEDDepA(SBP):
  """SBP class for message MSG_VEL_NED_DEP_A (0x0205).

  You can have MSG_VEL_NED_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the velocity in local North East Down (NED)
coordinates. The NED coordinate system is defined as the local WGS84
tangent plane centered at the current position. The full GPS time is
given by the preceding MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  n : int
    Velocity North coordinate
  e : int
    Velocity East coordinate
  d : int
    Velocity Down coordinate
  h_accuracy : int
    Horizontal velocity accuracy estimate (not
implemented). Defaults to 0.

  v_accuracy : int
    Vertical velocity accuracy estimate (not
implemented). Defaults to 0.

  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags (reserved)
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'n' / construct.Int32sl,
                   'e' / construct.Int32sl,
                   'd' / construct.Int32sl,
                   'h_accuracy' / construct.Int16ul,
                   'v_accuracy' / construct.Int16ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'n',
               'e',
               'd',
               'h_accuracy',
               'v_accuracy',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 's32', 'n' ),
             ( 's32', 'e' ),
             ( 's32', 'd' ),
             ( 'u16', 'h_accuracy' ),
             ( 'u16', 'v_accuracy' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgVelNEDDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgVelNEDDepA, self).__init__()
      self.msg_type = SBP_MSG_VEL_NED_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.n = kwargs.pop('n')
      self.e = kwargs.pop('e')
      self.d = kwargs.pop('d')
      self.h_accuracy = kwargs.pop('h_accuracy')
      self.v_accuracy = kwargs.pop('v_accuracy')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgVelNEDDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgVelNEDDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgVelNEDDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgVelNEDDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    
SBP_MSG_BASELINE_HEADING_DEP_A = 0x0207
class MsgBaselineHeadingDepA(SBP):
  """SBP class for message MSG_BASELINE_HEADING_DEP_A (0x0207).

  You can have MSG_BASELINE_HEADING_DEP_A inherit its fields directly
  from an inherited SBP object, or construct it inline using a dict
  of its fields.

  
  This message reports the baseline heading pointing from the base station
to the rover relative to True North. The full GPS time is given by the
preceding MSG_GPS_TIME with the matching time-of-week (tow).


  Parameters
  ----------
  sbp : SBP
    SBP parent object to inherit from.
  tow : int
    GPS Time of Week
  heading : int
    Heading
  n_sats : int
    Number of satellites used in solution
  flags : int
    Status flags
  sender : int
    Optional sender ID, defaults to SENDER_ID (see sbp/msg.py).

  """
  _parser = construct.Struct(
                   'tow' / construct.Int32ul,
                   'heading' / construct.Int32ul,
                   'n_sats' / construct.Int8ul,
                   'flags' / construct.Int8ul,)
  __slots__ = [
               'tow',
               'heading',
               'n_sats',
               'flags',
              ]
  _fields = [
             ( 'u32', 'tow' ),
             ( 'u32', 'heading' ),
             ( 'u8', 'n_sats' ),
             ( 'u8', 'flags' ),
            ]

  def __init__(self, sbp=None, **kwargs):
    if sbp:
      super( MsgBaselineHeadingDepA,
             self).__init__(sbp.msg_type, sbp.sender, sbp.length,
                            sbp.payload, sbp.crc)
      self.from_binary(sbp.payload)
    else:
      super( MsgBaselineHeadingDepA, self).__init__()
      self.msg_type = SBP_MSG_BASELINE_HEADING_DEP_A
      self.sender = kwargs.pop('sender', SENDER_ID)
      self.tow = kwargs.pop('tow')
      self.heading = kwargs.pop('heading')
      self.n_sats = kwargs.pop('n_sats')
      self.flags = kwargs.pop('flags')

  def __repr__(self):
    return fmt_repr(self)

  @staticmethod
  def from_json(s):
    """Given a JSON-encoded string s, build a message object.

    """
    d = json.loads(s)
    return MsgBaselineHeadingDepA.from_json_dict(d)

  @staticmethod
  def from_json_dict(d):
    sbp = SBP.from_json_dict(d)
    return MsgBaselineHeadingDepA(sbp, **d)

 
  def from_binary(self, d):
    """Given a binary payload d, update the appropriate payload fields of
    the message.

    """
    try:
      self._from_binary(d)
    except:
      print traceback.print_exc()

  def __getitem__(self, item):
    return getattr(self, item)

  def _get_embedded_type(self, t):
    return globals()[t]

  def to_binary(self):
    """Produce a framed/packed SBP message.

    """
    c = containerize(exclude_fields(self))
    self.payload = MsgBaselineHeadingDepA._parser.build(c)
    return self.pack()

  def to_json_dict(self):
    self.to_binary()
    d = super( MsgBaselineHeadingDepA, self).to_json_dict()
    j = walk_json_dict(exclude_fields(self))
    d.update(j)
    return d
    

msg_classes = {
  0x0102: MsgGPSTime,
  0x0103: MsgUtcTime,
  0x0208: MsgDops,
  0x0209: MsgPosECEF,
  0x0214: MsgPosECEFCov,
  0x020A: MsgPosLLH,
  0x0211: MsgPosLLHCov,
  0x020B: MsgBaselineECEF,
  0x020C: MsgBaselineNED,
  0x020D: MsgVelECEF,
  0x0215: MsgVelECEFCov,
  0x020E: MsgVelNED,
  0x0212: MsgVelNEDCov,
  0x0213: MsgVelBody,
  0x0210: MsgAgeCorrections,
  0x0100: MsgGPSTimeDepA,
  0x0206: MsgDopsDepA,
  0x0200: MsgPosECEFDepA,
  0x0201: MsgPosLLHDepA,
  0x0202: MsgBaselineECEFDepA,
  0x0203: MsgBaselineNEDDepA,
  0x0204: MsgVelECEFDepA,
  0x0205: MsgVelNEDDepA,
  0x0207: MsgBaselineHeadingDepA,
}