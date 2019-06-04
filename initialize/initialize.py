from pymongo import MongoClient
import uuid
import datetime

def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection


def initializedata(collection):
    data_dict = [{'Doctor_name':'Jiachen.Li',
                  'Doctor_specialization':'Paediatric Doctorry',
                  'Doctor_location':'Kensington',
                  'Doctor_room':'302',
                  'Doctor_Uni':'University of New South Wales'},
                 {'Doctor_name': 'Xiaohan.Wang',
                  'Doctor_specialization': 'Orthodontics',
                  'Doctor_location': 'Randwick',
                  'Doctor_room': '101',
                  'Doctor_Uni': 'University of Sydney'
                  },
                 {'Doctor_name': 'David.Zhang',
                  'Doctor_specialization': 'Oral Surgery',
                  'Doctor_location': 'CBD',
                  'Doctor_room': '105',
                  'Doctor_Uni': 'University of Wollogong'
                  },
                 {'Doctor_name': 'Xiaotong.Wu',
                  'Doctor_specialization': 'Dental Care',
                  'Doctor_location': 'Burwood',
                  'Doctor_room': '106',
                  'Doctor_Uni': 'Shanghai JiaoTong University'
                  }
                 ]
    collectiondata = collection.find()
    for item in collectiondata:
        collection.delete_one({'_id':item['_id']})
    for item in data_dict:
        item['_id'] = str(uuid.uuid4())
        collection.insert_one(item)
    print('successful')



def initializetimeslot(collection):
    collection_Doctor = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicDoctor')
    collectionDoctordata = collection_Doctor.find()
    collectiondata  = collection.find()
    for item in collectiondata:
        collection.delete_one({'_id':item['_id']})
    for item in collectionDoctordata:
        for i in range(1,4):
            insert_Day = (datetime.date.today() + datetime.timedelta(days=+i)).strftime('%Y-%m-%d')
            for j in range(9,17):
                dict = {}
                dict['Doctor_name'] = item['Doctor_name']
                dict['Doctor_id'] = item['_id']
                dict['_id']=str(uuid.uuid4())
                dict['Date'] = insert_Day
                if j >= 12:
                    dict['Time'] = str(j) + ':00PM-' + str(j + 1) + ':00PM'
                elif j == 11:
                    dict['Time'] = str(j) + ':00AM-' + str(j + 1) + ':00PM'
                else:
                    dict['Time'] = str(j) + ':00AM-' + str(j + 1) + ':00AM'
                dict['Status'] = 'N'
                dict['Patient_name'] = ''
                collection.insert_one(dict)
    print('success')

if __name__ == '__main__':
    initializedata(connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicDoctor'))
    initializetimeslot(connectcloud('ds263089.mlab.com',63089,
                           'dentalclinic','admin','LIjiachen0717','DentalClinicTimetable'))