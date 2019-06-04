# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from pymongo import MongoClient
from flask import make_response
from flask import jsonify


def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection


class Doctorinformation(Resource):
    def get(self):
        print(g.args)
        try:
            dbconnection = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicDoctor')
            data = dbconnection.find_one({'Doctor_name':g.args['Doctor']})
            print(data)
            if data is None:
                return make_response(jsonify(message="Doctor {} doesn't exist.".format(g.args['Doctor'])), 404)
            doctor_dict = {}
            doctor_dict['Doctor_name'] = data['Doctor_name']
            doctor_dict['Doctor_specialization'] = data['Doctor_specialization']
            doctor_dict['Doctor_location'] = data['Doctor_location']
            doctor_dict['Doctor_room'] = data['Doctor_room']
            doctor_dict['Doctor_Uni'] = data['Doctor_Uni']
            return make_response(jsonify(message = "OK",entities=doctor_dict),200)
        except:
            return make_response(jsonify(message="Interval Error")), 500

