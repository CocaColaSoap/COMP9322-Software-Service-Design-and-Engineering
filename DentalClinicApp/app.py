from flask import *
import requests
from flask import render_template
from rivescript import RiveScript
import os
app = Flask(__name__)

app.secret_key = 'please-generate-a-random-secret_key'
rs = RiveScript()
rs.load_directory(os.getcwd()+'/brain')
rs.sort_replies()
@app.route('/')
def index():
    return render_template('index.html')

reminder_flag = False
@app.route('/message',methods = ['POST'])
def message():
    global reminder_flag
    try:
        session["username"]
    except:
        if reminder_flag is True:
            req_msg = request.form['msg']
            session['username'] = req_msg
            reply = f'Hello {session["username"]},Welcome to use this Dental Clinic Chatbot.<br>' \
                f'You can talk with me or get the dental service.<br>' \
                f'To get Doctor Information, please type eg:list all Doctors in Clinic etc.<br>' \
                f'To book an appointment, please type eg:get timetable of xx on YYYY-MM-DD.<br>'
            return reply
        elif reminder_flag is False:
            reply = "please type your name first to get services"
            reminder_flag = True
            return reply


    req_msg = request.form['msg']
    result = requests.get('https://api.wit.ai/message?v=20190401&q={}'.format(req_msg),
                         headers={'Authorization': 'Bearer XNFTSAJFBGZR6DN6HC6EGIVI7RJDOAFX'}).json()
    try:
        print(result)
        if result['entities']['intent'][0]['value'] == 'ListAllDoctors':
            content = requests.get(f'http://127.0.0.1:5000/DoctorService/AllDoctorInformation').json()
            print(content)
            if content['message'] == 'OK':
                reply = 'Doctors have been listed below<br>'
                reply += '<table>'
                reply += '<tr>'
                reply += '<td>Doctor Name</td>'
                reply += '<td>Doctor Specialization</td>'
                reply += '<td>Location</td>'
                reply += '</tr>'
                for item in content['DoctorInformation']:
                    reply += '<tr>'
                    reply += '<td>'+item['Doctor_name']+'</td>'
                    reply += '<td>' + item['Doctor_specialization'] + '</td>'
                    reply += '<td>' + item['Doctor_location']+'</td>'
                    reply += '</tr>'
                reply += '</table>'
                reply +='To get more information about Doctor, please type eg: Jiachen.Li Information'
            elif content['message'] == 'Interval Error':
                reply = 'Server has problems, please waiting for repairing'
            else:
                reply = 'No Doctor in Clinic.'

        if result['entities']['intent'][0]['value'] == 'Doctor information':
            content = requests.get(f'http://127.0.0.1:5000/DoctorService/DoctorInformation?Doctor={req_msg.split()[0]}').json()
            if content['message'] == 'OK':
                reply = 'Doctor Name:' + content['entities']['Doctor_name'] + '<br>'
                reply += 'Doctor Specialization:' + content['entities']['Doctor_specialization'] + '<br>'
                reply += 'Location:' + content['entities']['Doctor_location'] + '<br>'
                reply += 'Room:' + content['entities']['Doctor_room'] + '<br>'
                reply += 'Uni:' + content['entities']['Doctor_Uni'] + '<br>'
            elif content['message'] == 'Interval Error':
                reply = 'Server has problems, please waiting for repairing'
            else:
                reply = 'Please type correct Doctor Name'

        if result['entities']['intent'][0]['value'] == 'ListAvailableDoctors':
            date = result['entities']['datetime'][0]['values'][0]['value'][0:10]
            content = requests.get(f'http://127.0.0.1:5000/DoctorService/AvailableDoctor?Date={date}').json()
            if content['message'] == 'OK':
                reply = 'Available Doctors on {}'.format(date) + '<br>'
                reply += '<table>'
                reply += '<tr>'
                reply += '<td>Dentist Name</td>'
                reply += '<td>Location</td>'
                reply += '</tr>'
                for item in content['entities']:
                    reply += '<tr>'
                    reply += '<td>' + item['Doctor_name'] + '</td>'
                    reply += '<td>' + item['Doctor_location'] + '</td>'
                    reply += '</tr>'
                reply += '</table>'
                reply += 'To get the timetable of Doctor, please type eg: Get Timetable of Jiachen.Li on YYYY-MM-DD'
            elif content['message'] == 'Interval Error':
                reply = 'Server has problems, please waiting for repairing'
            else:
                reply = 'Please type correct date eg:YYYY-MM-DD and make true that the date is not three days later than today.'

        if result['entities']['intent'][0]['value'] == 'GetDoctorTimetable':
            doctor_name = result['entities']['doctor_name'][0]['value']
            date = result['entities']['datetime'][0]['values'][0]['value'][0:10]
            content = requests.get(
                f'http://127.0.0.1:8888/TimeslotService/GetDoctorTimetable?Doctor={doctor_name}&Date={date}').json()
            if content['message'] == 'OK':
                reply = f'The timetable of {doctor_name} on {date} is<br>'
                reply += '<table>'
                reply += '<tr>'
                reply += '<td>Doctor Name</td>'
                reply += '<td>Date</td>'
                reply += f'<td>Timeslot</td>'
                reply += f'<td>Book Appointment</td>'
                reply += '</td>'
                reply += '</tr>'
                for item in content['entities']:
                    reply += '<tr>'
                    reply += '<td>' + item['Doctor_name'] + '</td>'
                    reply += '<td>' + date + '</td>'
                    reply += f'<td>' + item['Time']+'</td>'
                    reply += f'<td><input type=button data={item["_id"]} onclick = aClick(this) value=Book></input></td>'
                    reply += '</tr>'
            elif content['message'] == 'Interval Error':
                reply = 'Server has problems, please waiting for repairing'
            else:
                reply = 'The doctor may has no available timetable today.'

        if result['entities']['intent'][0]['value'] == 'Check Appointment':
            content = requests.get(
                f'http://127.0.0.1:8888/TimeslotService/CheckAppointment?Patientname={session["username"]}').json()
            if content['message'] == 'OK':
                reply = '<table>'
                reply += '<tr>'
                reply += '<td>Doctor Name</td>'
                reply += '<td>Date</td>'
                reply += f'<td>Timeslot</td>'
                reply += f'<td>Cancel</td>'
                reply += '</td>'
                reply += '</tr>'
                for item in content['entities']:
                    reply += '<tr>'
                    reply += '<td>' + item['Doctor_name'] + '</td>'
                    reply += '<td>' + item['Date'] + '</td>'
                    reply += f'<td>' + item['Time'] + '</td>'
                    reply += f'<td><input type=button data={item["_id"]} onclick = bClick(this) value=cancel></input></td>'
                    reply += '</tr>'
            elif content['message'] == 'Interval Error':
                reply = 'Server has problems, please waiting for repairing'
            else:
                reply = 'No appointment.'
    except:
            reply = rs.reply('localhost', req_msg)
    return reply


@app.route('/bookAppointment',methods = ['POST'])
def makeappointment():
    req_msg = request.form['msg']
    content = requests.post(
        f'http://127.0.0.1:8888/TimeslotService/BookAppointment?Appointmentid={req_msg}&Patientname={session["username"]}').json()
    reply = ''
    if content['message'] == 'Book Successful':
        reply = f'You have booked with {content["Doctor_name"]} on {content["Date"]} {content["Time"]}.<br>' \
                'If you want cancel the appointment, please type: check appointment first.'
    elif content['message'] =='Book not Successful':
        reply = 'The timeslot is not available<br>' \
                'Please book another timeslot.<br>'
        content = requests.get(
            f'http://127.0.0.1:8888/TimeslotService/GetDoctorTimetable?Doctor={content["Doctor_name"]}&Date={content["Date"]}').json()
        reply += '<table>'
        reply += '<tr>'
        reply += '<td>Doctor Name</td>'
        reply += '<td>Date</td>'
        reply += f'<td>Timeslot</td>'
        reply += f'<td>Book Appointment</td>'
        reply += '</td>'
        reply += '</tr>'
        for item in content['entities']:
            reply += '<tr>'
            reply += '<td>' + item['Doctor_name'] + '</td>'
            reply += '<td>' + item["Date"] + '</td>'
            reply += f'<td>' + item['Time'] + '</td>'
            reply += f'<td><input type=button data={item["_id"]} onclick = aClick(this) value=Book></input></td>'
            reply += '</tr>'

    elif content['message'] == 'Interval Error':
        reply = 'Server has problems, please waiting for repairing'
    return reply


@app.route('/cancel',methods=['POST'])
def cancel():
    req_msg = request.form['msg']
    content = requests.post(
        f'http://127.0.0.1:8888/TimeslotService/CancelAppointment?Appointmentid={req_msg}&Patient_name={session["username"]}').json()
    reply = ''
    if content['message'] == 'Cancel successful':
        reply = 'Cancel Successful.'
    elif content['message'] == 'Interval Error':
        reply = 'Server has problems, please waiting for repairing'
    else:
        reply = 'No appointment could be cancelled'
    return reply



if __name__ == '__main__':
    app.run(
        port = 10898,
        debug = True
    )
