# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.BookAppointment import Bookappointment
from .api.CancelAppointment import Cancelappointment
from .api.CheckAppointment import Checkappointment
from .api.GetDoctorTimetable import Getdoctortimetable


routes = [
    dict(resource=Bookappointment, urls=['/BookAppointment'], endpoint='BookAppointment'),
    dict(resource=Cancelappointment, urls=['/CancelAppointment'], endpoint='CancelAppointment'),
    dict(resource=Checkappointment, urls=['/CheckAppointment'], endpoint='CheckAppointment'),
    dict(resource=Getdoctortimetable, urls=['/GetDoctorTimetable'], endpoint='GetDoctorTimetable'),
]