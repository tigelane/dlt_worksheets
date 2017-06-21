#!/usr/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)

app_name = 'steameo'


# This application will run on TCP port
app_port = 5000

@app.route('/')
@app.route('/index')
def index():
    html = '''
        <center>
        <BODY style="color:#00FC00" bgcolor=black><H3>You have connected to the test server, not the real one.</H3>
        '''.format(app_name)
    html += '''
        <p>
        Current date and time for this server: 
        '''
    html += datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html += '''
        <H3>(in a breathy voice while waving a hand infront of your face)<br>Go Back. This is not the web page you are looking for.</H3>
        <p>
        </BODY></HTML>
        '''
    return html

@app.route('/api/v1/show_jobs/<jobs>/')
def show_jobs(jobs):

    if jobs == 'all':
        # sql_query = all_sql_query
        print ("All Jobs request.")
    elif jobs == 'open':
        # sql_query = open_sql_query
        print ("Open Jobs request.")

    ''' Get all of the records and return them as a list'''
    myList = [
        [0, "I5 paving", "city of Portland"],
        [1, "road build", "bobs lawns"],
        [2, "projects howdy", "I'm howdy"],
        ]

    reply = {'status': 'OK', 'results': myList}    
    return jsonify(reply)


@app.route('/incomming', methods=['POST'])
def incomming():
    print ("Incomming message!")
    reply = {'status': 'None'}
    request.get_data()
    inbound_message = request.json
    print ("Message from: {0}".format(request.environ['REMOTE_ADDR']))
    print ("Message ID: {0}".format(inbound_message["data"]["id"]))

    return jsonify(reply)

if __name__ == '__main__':
    app.config.update(
        DEBUG = True)
    app.run(host='0.0.0.0', port=app_port)
