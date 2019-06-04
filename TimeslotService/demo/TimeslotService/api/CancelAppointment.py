# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from flask import make_response
from flask import jsonify
from pymongo import MongoClient

def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection

class Cancelappointment(Resource):
    def post(self):
        try:
            dbconnection = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicTimetable')
            data = dbconnection.find_one({'_id':g.args["Appointmentid"],'Patient_name':g.args["Patient_name"]})
            if data is None:
                return make_response(jsonify(message="Cancel not successful"),404)
            else:
                data['Status'] = 'N'
                data['Patient_name'] = ''
                dbconnection.update({'_id': data['_id']}, data)
                return make_response(jsonify(message="Cancel successful"),200)
        except:
            return make_response(jsonify(message="Interbval Error"),500)