#!/usr/bin/python
from flask import Flask, jsonify, request
app = Flask(__name__)

import MySQLdb, sys, os, json, requests, datetime

# Log file enablement
import inspect
log_file_name = "/usr/local/brimstone.log"
log_file_enable = True

app_name = 'brimstone'
app_version = "1.0"

db = None
db_name = 'job_worksheets'
#db_pass = 'mysql'
db_pass = 'H2xE6h6Bo9cgsnkiUhW076Qf'
db_addr = os.getenv('SQL_SERVER_IPADDR', 'localhost')

sql_ws_all = 'SELECT worksheets.id, jobs.name, worksheets.date_open, worksheets.notes, status.status FROM worksheets JOIN jobs ON jobs.id = worksheets.jobs_id JOIN status ON worksheets.status_id = status.id WHERE status.status IS NOT NULL;'
sql_ws_open = 'SELECT worksheets.id, jobs.name, worksheets.date_open, worksheets.notes, status.status FROM worksheets JOIN jobs ON jobs.id = worksheets.jobs_id JOIN status ON worksheets.status_id = status.id WHERE status.status = "Open";'
sql_jobs_all = 'SELECT jobs.name, customers.name, jobs.notes, status.status FROM jobs JOIN customers ON jobs.customer_id = customers.id JOIN status ON jobs.status_id = status.id;'
sql_jobs_open = 'SELECT jobs.id, jobs.name, customers.name, jobs.notes, status.status FROM jobs JOIN customers ON jobs.customer_id = customers.id JOIN status ON jobs.status_id = status.id WHERE status.status = "Open";'
edit_job_sql_query = 'SELECT jobs.id, jobs.name, customers.name, jobs.notes, status.status FROM jobs JOIN customers ON jobs.customer_id = customers.id JOIN status ON jobs.status_id = status.id WHERE status.status = "Open";'

# This application will run on the following TCP port
app_port = 5000

def write_log(entry):
    if log_file_enable == False:
        return

    try:
        log_file = open(log_file_name, "a")
    except:
        print("BAD  - Unable to open file for append:   {0}\n".format(log_file_name))
        sys.exit()

    try:
        logEntry = "{0} - Calling Function: {1}".format(entry, inspect.stack()[1][3])
        log_file.write(logEntry)
        log_file.close()
    except:
        print "cant do a log"

@app.route('/')
@app.route('/index')
def index():
    html = '''
        <center>
        <BODY style="color:#00FC00" bgcolor=black><H3>You have connected to the {0} application server</H3>
        '''.format(app_name)
    html += '''
        <p>
        Current date and time for this server: 
        '''
    html += datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html += '''
        <H3>(in a breathy voice while waving a hand infront of your face)<br>Go Back. This is not the web page you are looking for.</H3>
        <p>
        </BODY></HTML>
        '''
    return html

@app.route('/api/v1/show_jobs/<status>/')
def apiv1_show_jobs(status):
    myList = []

    if status == 'all':
        sql_query = sql_jobs_all
        write_log("Jobs request - All")
    elif status == 'open':
        sql_query = sql_jobs_open
        write_log("Jobs request - Open")

    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        for row in data:
            myList.append([row[0], row[1], row[2], row[3], row[4]])

        close_db()
        reply = {'status': 'OK', 'results': myList}
    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    reply = {'general': reply}
    return jsonify(reply)

@app.route('/api/v1/show_ws/<status>/')
def apiv1_show_ws(status):
    myList = []

    if status == 'all':
        sql_query = sql_ws_all
        write_log("Worksheets request - All")
    elif status == 'open':
        write_log("Worksheets request - Open")
        sql_query = sql_ws_open

    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        for row in data:
            myList.append([row[0], row[1], row[2], row[3], row[4]])
        close_db()
        reply = {'status': 'OK', 'results': myList}
    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    write_log("{0} - {1}".format(reply['status'], reply['results']))
    reply = {'general': reply}
    return jsonify(reply)

@app.route('/api/v1/add_ws/<project_id>/')
def apiv1_add_ws(project_id):

    date = datetime.date.today().strftime("%Y-%m-%d")
    sql_query_add = 'INSERT INTO worksheets (jobs_id, status_id, date_open) VALUES ({0},1, "{1}");'.format(project_id, date)
    sql_query_get_last = 'SELECT LAST_INSERT_ID();'

    write_log("Adding Worksheet with command: {}".format(sql_query_add))

    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query_add)
        db.commit()

        cursor.execute(sql_query_get_last)
        myData = cursor.fetchall()

        # Maybe check for errors here later
        close_db()
        reply = {'status': 'OK', 'results': myData}

    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    write_log("{0} - {1}".format(reply['status'], reply['results']))
    reply = {'general': reply}
    return jsonify(reply)

@app.route('/api/v1/add_job/')
def apiv1_add_job():

    date_open = datetime.date.today().strftime("%Y-%m-%d")
    sql_query_add = 'INSERT INTO jobs (status_id, date_open) VALUES (1, "{0}");'.format(date_open)
    sql_query_get_last = 'SELECT LAST_INSERT_ID();'

    write_log("Adding Job with command: {}".format(sql_query_add))

    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query_add)
        db.commit()

        cursor.execute(sql_query_get_last)
        myData = cursor.fetchall()

        # Maybe check for errors here later
        close_db()
        reply = {'status': 'OK', 'results': myData}

    except:
        reply = {'status': 'FAIL', 'results': "The Application server is OK, but is unable to show records from database {0}!".format(db_name)}
    
    write_log("{0} - {1}".format(reply['status'], reply['results']))
    reply = {'general': reply}
    return jsonify(reply)

@app.route('/api/v1/edit_job/<this_id>/')
def apiv1_edit_job(this_id):

    # return:
    #     form_data = {"project_name": form_data[0][0], "worksheet_id":worksheet_id, "date":"15/5/2017", "resources":resources, "materials":materials}

    sql_query = 'SELECT customers.id, customers.name, jobs.name, jobs.date_open, jobs.date_close, jobs.notes, status.status FROM jobs JOIN customers ON jobs.customer_id = customers.id JOIN status ON jobs.status_id = status.id WHERE jobs.id = {};'.format(this_id)
    general = get_from_db(sql_query)

    all_info = {'general': general, 'resources': [], 'materials':[]}
    print (all_info)
    return jsonify(all_info)

@app.route('/api/v1/write_job/<this_id>/')
def apiv1_write_job(this_id):
    pass


@app.route('/api/v1/get_ws/<worksheet_id>/')
def apiv1_get_ws(worksheet_id):
    # return:
    #     form_data = {"project_name": form_data[0][0], "worksheet_id":worksheet_id, "date":"15/5/2017", "resources":resources, "materials":materials}

    sql_query = 'SELECT jobs.name, worksheets.date_open, worksheets.notes, status.status FROM worksheets JOIN jobs ON worksheets.jobs_id = jobs.id JOIN status ON worksheets.status_id = status.id WHERE worksheets.id = {};'.format(worksheet_id)
    general = get_from_db(sql_query)
    # print form_data
    sql_query = 'SELECT resource.name, wsheet2resource.hours, wsheet2resource.rate, wsheet2resource.notes FROM wsheet2resource JOIN worksheets ON worksheets.id = wsheet2resource.worksheet_id JOIN resource ON wsheet2resource.resource_id = resource.id WHERE wsheet2resource.worksheet_id = {};'.format(worksheet_id)
    resources = get_from_db(sql_query)
    # print resources
    sql_query = 'SELECT materials.name, materials.cost, materials.notes FROM materials WHERE materials.worksheet_id = {};'.format(worksheet_id)
    materials = get_from_db(sql_query)
    # print materials

    all_info = {'general': general, 'resources': resources, 'materials':materials}
    return jsonify(all_info)

def get_from_db(sql_query):
    myList = []

    try:
        open_db()
        cursor = db.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        for row in data:
            rowList = []
            for a in row:
                rowList.append(a)
            myList.append(rowList)
        close_db()
        reply = {'status': 'OK', 'results': myList}
        # print myList
    except ValueError:
        reply = {'status': 'FAIL', 'results': "E1000: The Application server is OK, but is unable to show records from database {0}!".format(db_name)}

    #write_log("{0} - {1}".format(data['status'], reply['results']))
    return reply

@app.route('/api/v1/worksheet_save')
def apiv1_worksheet_save():
    #functionName = "def apiv1_worksheet_save():"
    request.get_data()

    reply = {'status': 'OK', 'results': myList}   
    reply = {'general': reply} 
    return jsonify(reply)

def open_mysql():
    global db
    ''' Opens a connection to MySQL at the given IP Address '''
	
    try:
        # Open database connection
        db = MySQLdb.connect(db_addr,"root",db_pass)
        return True
    except:
        return False

def create_db():
    ''' Create a new database '''

    try:
        sql_query = "CREATE DATABASE IF NOT EXISTS {0};".format(db_name)
        cursor = db.cursor()
        cursor.execute(sql_query)
    except:
        return False

    return True

def open_db():
    global db
    ''' Opens the database at the given IP Address '''
    	
    try:
        # Open database connection
        db = MySQLdb.connect(db_addr, "root", db_pass, db_name)
    except:
        return False

    return True

def close_db():
    global db
    # disconnect from server
    db.close()

@app.route('/add_row')
def add_row(text, date, name):
	# Use the right database
	sql_query = "INSERT INTO entry (id, entry, entry_date, name) VALUES (NULL, '{0}', '{1}', '{2}');".format(text, date, name)
	open_db()
	cursor = db.cursor()	
	cursor.execute(sql_query)
	db.commit()

	close_db()
	return

@app.route('/add_entry', methods=['POST'])
def add_entry():
    try:
        name = request.args.get("name")
        entry = request.args.get("entry")
        now = datetime.now()
        date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
        add_row(entry, date, name)
    except:
        return jsonify({'status': 'FAIL', 'results': "Not able to post to the database!"})

    return jsonify({'status': 'OK', 'results': "Blog Entry Posted!"})

@app.route('/incomming', methods=['POST'])
def incomming():
    # print ("Incomming message!")
    now = datetime.now()
    date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
    reply = {'status': 'None'}
    request.get_data()
    inbound_message = request.json
    # print (request.data)
    # print (request.form)
    #print (request.json)
    # print ("Message from: {0}".format(request.environ['REMOTE_ADDR']))
    messageurl = "https://api.ciscospark.com/v1/messages/{}".format(inbound_message["data"]["id"])

    headers = {
        'authorization': sparkUser,
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", messageurl, headers=headers)
    messagedata = json.loads(response.text)
    print messagedata
    try:
        message = "You betya!"
        # print("Spark room message is: {0}".format(messagedata["text"]))
        # if for_me(messagedata["text"]):
        # add_row(messagedata["text"], date, 'Steameo')
        # post_message_to_room(post_room_id, message)
        reply = {'status': 'OK'}
    except ValueError:
        print ("We have an error:  {0}".format(response.content))
        reply = {'status': 'Error'}

    return jsonify(reply)

if __name__ == '__main__':
    write_log("Using DB Server at: {0}".format(db_addr))

    app.config.update(DEBUG = True)
    app.run(host='0.0.0.0', port=app_port)