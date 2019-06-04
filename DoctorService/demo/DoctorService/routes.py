# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.AllDoctorInformation import Alldoctorinformation
from .api.DoctorInformation import Doctorinformation
from .api.AvailableDoctor import Availabledoctor


routes = [
    dict(resource=Alldoctorinformation, urls=['/AllDoctorInformation'], endpoint='AllDoctorInformation'),
    dict(resource=Doctorinformation, urls=['/DoctorInformation'], endpoint='DoctorInformation'),
    dict(resource=Availabledoctor, urls=['/AvailableDoctor'], endpoint='AvailableDoctor'),
]