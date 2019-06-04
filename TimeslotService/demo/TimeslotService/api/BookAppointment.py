# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from flask import make_response
from flask import jsonify

from pymongo import MongoClient
from flask import request, g

from . import Resource
from .. import schemas

def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection

class Bookappointment(Resource):

    def post(self):
        print(g.args)
        try:
            dbconnection = connectcloud('ds263089.mlab.com', 63089,
                                        'dentalclinic', 'admin', 'LIjiachen0717', 'DentalClinicTimetable')
            data = dbconnection.find_one({'_id': g.args["Appointmentid"]})
            if data['Status'] == 'Y':
                return make_response(
                    jsonify(message="Book not Successful", Doctor_name=data['Doctor_name'], Date=data['Date'],
                            Time=data['Time']), 404)
            else:
                data['Status'] = 'Y'
                data['Patient_name'] = g.args["Patientname"]
                dbconnection.update({'_id': g.args["Appointmentid"]}, data)
                return make_response(jsonify(message="Book Successful",Doctor_name=data['Doctor_name'], Date = data['Date'],
                                     Time = data['Time']),200)
        except:
            return make_response(jsonify(message="Interval Error"),500)