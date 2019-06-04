# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import make_response
from flask import jsonify
from flask import request, g

from . import Resource
from .. import schemas
from pymongo import MongoClient


def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection


def DoctorInformationDealing(data):
    doctor_dict = {}
    doctor_dict['Doctor_name'] = data['Doctor_name']
    doctor_dict['Doctor_specialization'] = data['Doctor_specialization']
    doctor_dict['Doctor_location'] = data['Doctor_location']
    return doctor_dict


class Availabledoctor(Resource):

    def get(self):
        print(g.args['Date'])
        try:
            dbconnection = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicTimetable')
            dbconnection1 = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicDoctor')
            data1 = dbconnection1.find()
            list_doctor = []
            for item in data1:
                data = dbconnection.find_one({'Doctor_name':item['Doctor_name'],'Status':'N','Date':g.args['Date']})
                print(data)
                if data is not None:
                    list_doctor.append(item)
            if len(list_doctor) == 0:
                return make_response(jsonify(message="No available Doctors"), 404)
            else:
                return make_response(jsonify(message="OK",entities=list_doctor), 200)
        except:
            return make_response(jsonify(message="Interval Error"),500)