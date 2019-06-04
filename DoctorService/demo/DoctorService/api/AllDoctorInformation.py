# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from pymongo import MongoClient
from flask import make_response
from flask import jsonify
from . import Resource

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

class Alldoctorinformation(Resource):

    def get(self):
        try:
            dbconnection = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicDoctor')
            data = dbconnection.find()
            print(data[0])
            DoctorList= []
            for item in data:
                DoctorList.append(DoctorInformationDealing(item))
            if len(DoctorList) == 0:
                return make_response(jsonify(message="No Doctor in Clinic"), 404)
            return make_response(jsonify(message="OK",DoctorInformation=DoctorList), 200)

        except:
            return make_response(jsonify(message="Interbval Error"), 500)