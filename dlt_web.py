#!/usr/bin/env python

from flask import Flask, request, render_template, url_for, redirect, session

from datetime import datetime
import sys, requests, re, random, os
import json, time

# Log file enablement
import inspect
log_file_name = "/usr/local/brimstone.log"
log_file_enable = True

applicationTitle = "DLT_WS_Web"
app_addr = os.getenv('APP_SERVER_IPADDR', 'localhost')
app_port = 5000

url_base = 'http://{0}:{1}/api/v1'.format(app_addr, app_port)
data_url = ""
form_data = []
records = []
app_title = "DL Trucking - Daily Worksheets"

#  Theme files and theme to use for the system
theme = "a"
theme_cancel = "b"
theme_file_1 = "themes/dlt_themes.min.css" 
theme_file_2 = "themes/jquery.mobile.icons.min.css" 

app = Flask(__name__)

def write_log(entry):
    if log_file_enable == False:
        return

    try:
        log_file = open(log_file_name, "a")
    except:
        print("BAD  - Unable to open file for append:   {0}\n".format(log_file_name))
        sys.exit()

    logEntry = "{0} - Calling Function: {1}".format(entry, inspect.stack()[1][3])
    log_file.write(logEntry)
    log_file.close()
    print "Log Entry: {}".format(logEntry)

def basic_render(data_url, page_header, rendering_file, form_data):
    if data_url != "":
        data = open_url(data_url)
        if data['result'] == 0:
            return data['data']
        else:
            records = data['data']['general']['results']
    else:
        records = []

    html = document_header()
    html += render_template(rendering_file, url_base = url_base, page_header = page_header, theme = theme, theme_cancel=theme_cancel, records=records, form_data=form_data )
    html += document_footer()

    return html

@app.route('/edit_job/<job_id>/')
def edit_job(job_id):
    
    data_url = '{0}/edit_job/{1}/'.format(url_base, job_id)
    rendering_file = 'edit_job.html'
    page_header = "DLT Edit a Job"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/save_job', methods=['POST'])
def save_job():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """
    if request.form["button"] == "cancel":
        return redirect('/jobs', code=303)

    formValues = {}
    formValues["hco"] = request.form['hco']
    formValues["janme"] = request.form['janme']
    formValues["loc"] = request.form['loc']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    # Add the rest to values that are optional
    formValues["sdate"] = request.form['sdate']
    formValues["epay"] = request.form['epay']
    

    print (formValues)
    # Need to write info to the app server


    return redirect('/server_info', code=303)

@app.route('/index')
def index():
    return default()

@app.route('/')
def default():

    rendering_file = 'index.html'
    page_header = "David Linn Trucking"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/jobs')
def jobs():

    data_url = '{0}/show_jobs/open/'.format(url_base)
    rendering_file = 'jobs.html'
    page_header = "DLT Job Home"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/worksheets')
def worksheets():

    rendering_file = 'worksheets.html'
    page_header = "DLT Daily Worksheets"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/enter_key')
def enter_key():

    rendering_file = 'enter_key.html'
    page_header = "Enter User Key"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/select_jobs_open')
def select_jobs_open():

    data_url = '{0}/show_jobs/open/'.format(url_base)
    rendering_file = 'select_job_add_ws.html'
    page_header = "Select Project"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/select_ws_open')
def select_ws_open():

    data_url = '{0}/show_ws/open/'.format(url_base)
    rendering_file = 'select_ws.html'
    page_header = "Select Worksheet"

    return basic_render(data_url, page_header, rendering_file, form_data)

@app.route('/add_ws/<project_id>/')
def add_ws(project_id):

    data_url = '{0}/add_ws/{1}/'.format(url_base, project_id)

    if data_url != "":
        data = open_url(data_url)

        if data['result'] == 0:
            return data['data']
        else:
            # print data
            new_worksheet = data['data']['general']['results'][0][0]

    return edit_ws(new_worksheet)

@app.route('/edit_ws/<worksheet_id>/')
def edit_ws(worksheet_id):

    data_url = '{0}/get_ws/{1}/'.format(url_base, worksheet_id)
    rendering_file = 'edit_ws.html'
    page_header = "{}".format(worksheet_id)

    try:
        data = open_url(data_url)
        if data['result'] == 0:
            return data['data']
        else:
            all_data = data['data']
    except Exception as e:
        # print e
        return {'result':0, 'data':render_error_screen(e)}
    
    form_data = {"project_name": all_data['general']['results'][0][0], "worksheet_id":worksheet_id, "date":all_data['general']['results'][0][1], "resources":all_data['resources']['results'], "materials":all_data['materials']['results']}

    html = document_header()
    html += render_template(rendering_file, url_base = url_base, page_header = page_header, theme = theme, theme_cancel=theme_cancel, form_data=form_data )
    html += document_footer()

    return html

@app.route('/save_ws', methods=['POST'])
def save_ws():

    worksheet_id = request.form["worksheet_id"]
    if "ws_status" in request.form:
        ws_status= str(request.form['ws_status'])
    else:
        ws_status = "not"
    notes = str(request.form['notes'])
    # print (ws_status, notes, worksheet_id)

    # Need to save the two items above to the DB.
    # Also going to need to put a hidden item in the page called Worksheet_id so I know what record to update.
    # /api/v1/worksheet_save


    if "close" in request.form:
        return redirect('/', code=303)
    else:
        return redirect('/edit_ws/{0}/'.format(worksheet_id), code=303)

@app.route('/add_job')
def add_job():
    """
    Need to make a call to create a new job, then open the dit jobs page with that new job.
    :return: html pages as rendered html
    """

    data_url = '{0}/add_job'.format(url_base)

    if data_url != "":
        data = open_url(data_url)

        if data['result'] == 0:
            return data['data']
        else:
            print data
            id = data['data']['general']['results'][0][0]

    return edit_job(id)

def document_header():
    """
    Import all CSS and javascript files.  Setup page theme.
    :return: html pages as rendered html
    """    
    theme_1 = url_for('static', filename=theme_file_1) 
    theme_2 = url_for('static', filename=theme_file_2) 

    html = render_template('document_header.html', title=app_title, style_1=theme_1, style_2=theme_2)
    return html

def document_footer():
    """
    Close out the page.
    :return: html pages as rendered html
    """    
    html = render_template('document_footer.html')
    return html

def render_error_screen(error):
    """
    Takes the error as a string, returns full html page to display
    :param error: Error code
    :return: html pages as rendered html
    """
    # Render HTML
    html = document_header()
    html += render_template('error.html', error=error)
    html += document_footer()
    return html

def get_header_graphic():
    """
    Should be included on all screens, pics a rangome graphic for the top of the screen
    :return: url_for to the graphic for the header. 
    """
    header_graphic_file = header_graphic_files[random.randint(0, len(header_graphic_files)-1)]
    return url_for('static', filename=header_graphic_file)

def get_style_link():
    return url_for('static', filename=style_file)

def open_url(url):
    try: 
        result = requests.get(url)
        # print ("In open url 1")

    except:
        error = "Application Server Failure: Not able to communicate with Application Server at {0} ".format(app_addr)
        return {'result':0, 'data':render_error_screen(error)}

    decoded_json = json.loads(result.text)
    if (result.status_code == 200):
        # print ("In open url 2")
        if decoded_json['general']['status'] == 'FAIL':
            print (decoded_json)
            error = "Database Failure: Response from Application Server: " + decoded_json['general']['results']
            return {'result':0, 'data':render_error_screen(error)}

        if len(decoded_json['general']['results']) == 0:
            # print ("In open url 4")
            error = "Response from Application Server: No records found."
            return {'result':0, 'data':render_error_screen(error)}

    else:   
        error = "Non 200 HTML response - Some wierd error."
        return {'result':0, 'data':render_error_screen(error)}
    
    return {'result':1, 'data':decoded_json}

@app.route('/login', methods=['GET'])
def login_get():

    html = base_menu()
    html += render_template('login.html')

    return html

@app.route('/login', methods=['POST'])
def login_post():
    session['username'] = str(request.form['username'])
    session['password'] = str(request.form['password'])
    return redirect('/server_info', code=303)

@app.route('/new_gadget', methods=['GET'])
def new_gadget():
    """
    Render entry page for a new job
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('enter_new_gadget.html')
    return html

@app.route('/add_new_gadget', methods=['POST'])
def add_new_gadget():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """
    time_start = time.time()
    if request.form["button"] == "cancel":
        return redirect('/', code=303)

    formValues = {}
    formValues["type"] = request.form['type']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    # Add the rest to values that are optional
    formValues["name"] = request.form['name']
    formValues["wrating"] = request.form['wrating']
    formValues["notes"] = request.form['notes']
    # formValues[""] = request.form['']
    
    print (formValues)

    message = "Gadget added of type: {}".format(formValues["type"])
    if formValues["name"] != "":
        message += " named: {}".format(formValues["name"])

    html = table_header()
    html += render_template('add_record.html', thecolor="green", header="Success", message=message)
    html += table_footer()

    # print 'Time to complete posting of new gadget: ', time.time() - time_start
    return html

@app.route('/new_person', methods=['GET'])
def new_person():
    """
    Render entry page for a new job
    :return: html pages as rendered html
    """

    html = base_menu()
    html += render_template('enter_new_person.html')
    return html

@app.route('/add_new_person', methods=['POST'])
def add_new_person():
    """
    Gather data from form post and post information to database
    :return: html pages as rendered html
    """

    if request.form["button"] == "cancel":
        return redirect('/server_info', code=303)

    formValues = {}
    formValues["fname"] = request.form['fname']
    formValues["lname"] = request.form['lname']
    formValues["phone"] = request.form['phone']

    #  Look for missing items and show an error screen if needed
    for k, v in formValues.iteritems():
        if v == "":
            return render_error_screen("You must specify all of the '*' values.")

    print (request.form)

    # Add the rest to values that are optional
    formValues["contact"] = request.form['contact']
    formValues["email"] = request.form['email']
    formValues["notes"] = request.form['notes']
    # formValues[""] = request.form['']
    
    print (formValues)
    return redirect('/server_info', code=303)


@app.route('/show_jobs/<jobs>/')
def show_jobs(jobs):

    url = 'http://{0}:{1}/show_jobs/{2}/'.format(app_addr, app_port, jobs)
    
    if jobs == 'all':
        title = "All Jobs"
    else:
        title = "Open Jobs"

    data = open_url(url)
    if data['result'] == 0:
        return data['data']

    else:
        records = data['data']
        html = table_header()
        html += render_template('show_jobs.html', title=title, records=records)
        html += table_footer()

    return html

@app.route('/search_host')
def search_host():
    """
    Render Search for an Endpoint Page page
    :return: html pages as rendered html
    """

    # Render HTML
    tenant_list = []
    tenants = get_user_tenants()
    for tenant in tenants:
        tenant_list.append(tenant.name)

    html = base_menu()
    html += render_template('search_host.html', tenants=tenant_list)
    return html

@app.route('/search_host', methods=['POST'])
def search_host_post():
    """
    Gather data from form post and render search results
    :return: html pages as rendered html
    """
    time_start = time.time()
    aciSession = login_to_apic(session)
    if type(aciSession) is list:
        return aciSession[2]
    try:
        tenant_name = request.form['tenant_name']
    except:
        return render_error_screen("You must specify a tenant that you would like to search in")
    text = request.form['text']


    records = []

    tenants = get_user_tenants()
    for tenant in tenants:
        if tenant_name.upper() in tenant.name.upper() or tenant_name == 'all':
            apps = aci.AppProfile.get(aciSession, tenant)
            for app in apps:
                epgs = aci.EPG.get(aciSession, app, tenant)
                for epg in epgs:
                    # endpoints = aci.Endpoint.get_all_by_epg(aciSession, tenant.name, app.name, epg.name, with_interface_attachments=False)
                    endpoints = c1.get_epg_info(aciSession, tenant.name, app.name, epg.name)
                    for ep in endpoints:
                        for match in [ep.ip.upper(), ep.mac.upper(), ep.encap.upper(), ep.if_name.upper(), tenant.name.upper(), app.name.upper(), epg.name.upper()]:
                            if text.upper() in match:
                                records.append((ep.mac, ep.ip, ep.if_name, ep.encap,
                                            tenant.name, app.name, epg.name))
                                break


    html = table_header()
    html += render_template('search_host_post.html', text=text, records=set(records))
    html += table_footer()
    print 'Time to complete: ', time.time() - time_start
    return html

@app.route('/search_contract')
def search_contract():
    """
    Render Contract Details search form.
    :return:
    """
    # Render HTML
    html = base_menu()
    html += render_template('search_contract.html')
    return html

@app.route('/search_contract', methods=['POST'])
def search_contract_post():
    """
    Gather data from form post and render search results
    :return:
    """
    aciSession = login_to_apic(session)
    if type(aciSession) is list:
        return aciSession[2]

    text = request.form['text']


    # Download all of the tenants, app profiles, and EPGs
    # and store the names as tuples in a list
    records = []
    CONTRACTS = c1.ContractMap()

    tenants = aci.Tenant.get_deep(aciSession)
    for tenant in tenants:
        for contract in tenant.get_children():
            if isinstance(contract, aci.Contract):
                if text.upper() in contract.name.upper():
                    CONTRACTS.names.append(contract.name)
                    CONTRACTS.filters[contract.name] = []
                    CONTRACTS.tenant[contract.name] = tenant.name
                    for subject in contract.get_children():
                        url = '/api/node/mo/uni/tn-%s/brc-%s/subj-%s.json?query-target=children' % (tenant.name, contract.name, subject.name)
                        resp = aciSession.get(url)
                        dns = json.loads(resp.text)['imdata']
                        for dn in dns:
                            filter_name = dn['vzRsSubjFiltAtt']['attributes']['tRn'][4:]


                            records.append((tenant.name, contract.name, filter_name))
                            url = '/api/node/mo/uni/tn-%s/flt-%s.json?query-target=children&target-subtree-class=vzEntry' % (tenant.name, filter_name)

                            resp = aciSession.get(url)
                            dns = json.loads(resp.text)['imdata']
                            for dn in dns:
                                dFromPort = dn['vzEntry']['attributes']['dFromPort']
                                dToPort = dn['vzEntry']['attributes']['dFromPort']
                                prot = dn['vzEntry']['attributes']['prot']
                                if dFromPort == dToPort:
                                    dlistPort = prot + ':' + dFromPort
                                else:
                                    dlistPort = prot + ':' + dFromPort + '-' + dToPort
                                CONTRACTS.filters[contract.name].append(filter_name + ' (' + dlistPort + ')')

    # Render HTML
    html = table_header()
    html += render_template('search_contract_post.html', CONTRACTS=CONTRACTS)
    html += table_footer()
    return html


if __name__ == '__main__':
    # app.secret_key = os.urandom(24)
    app.secret_key = "abcde12345"
    app.config.update(
            DEBUG=True)

    app.run(host='0.0.0.0', port=80)
