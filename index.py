from flask import Flask, request, render_template, jsonify, redirect, url_for
from google.cloud import storage
from google.oauth2 import service_account
import requests
import json 
import iso3166
import os
import re
import logging
import getpass

#initialise Flask app
app = Flask(__name__)

#initialise logging library 
__version__ = "0.0.1"
log = logging.getLogger(__name__)

#initalise User-agent header for requests library 
USER_AGENT_HEADER = {'User-Agent': 'iso3166-2/{} ({}; {})'.format(__version__,
                                       'https://github.com/amckenna41/iso3166-2', getpass.getuser())}

#get Cloud Storage specific env vars
sa_json_str = os.environ["SA_JSON"]
project_id = os.environ["PROJECT_ID"]
bucket_name = os.environ["BUCKET_NAME"]
blob_name = os.environ["BLOB_NAME"]

##### Import ISO 3166-2 JSON from GCP Storage bucket #####
#convert str of service account from env var into json 
sa_json = json.loads(sa_json_str)
#pass service account json into credentials object
credentials = service_account.Credentials.from_service_account_info(sa_json)
#create GCP Storage client using credentials
storage_client = storage.Client(project=project_id, credentials=credentials)
#initialise bucket object
bucket = storage_client.bucket(bucket_name)
#get blob from bucket
blob = bucket.blob(os.environ["BLOB_NAME"])      
#get path to json blob in bucket
blob_path = "gs://" + bucket_name + "/" + blob_name
#bool to track if blob exists
blob_exists = True
#return error if object not found in bucket
if (blob.exists()):    
    #load json from blob on bucket
    all_iso3166_2 = json.loads(storage.Blob.from_string(blob_path, client=storage_client).download_as_text())
else:
    blob_exists = False

#error message returned if issue retrieving updates json
blob_not_found_error_message = {}
blob_not_found_error_message["status_code"] = 400
blob_not_found_error_message["message"] = "Error finding ISO 3166-2 object in GCP Storage Bucket."

#json object storing the error message and status code 
error_message = {}
error_message["status"] = 400

@app.route('/')
@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
def home():
    """
    Default route for https://iso3166-2-api.vercel.app/. Main homepage for API displaying the 
    purpose of API and its documentation. 

    Parameters
    ----------
    None

    Returns
    -------
    :render_template : html
      Flask html template for index.html page.
    :status_code : int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    :Flask.redirect : app.route
        Flask route redirected using the redirect function, specific route and URL
        used is determined by input parameters. 
    """  
    alpha2_code = []
    names = []
    
    #return error if blob not found in bucket 
    if not (blob_exists):
        return jsonify(blob_not_found_error_message), 400
    
    #parse alpha-2 code parameter
    if not (request.args.get('alpha2') is None):
        alpha2_code = ','.join(sorted([request.args.get('alpha2').upper()]))
    
    #parse name parameter
    if not (request.args.get('name') is None):
        names = ','.join(sorted([request.args.get('name').upper()]))

    #redirect to api_alpha2 route if alpha2 query string parameter set 
    if (alpha2_code != []):
        return redirect(url_for('api_alpha2', input_alpha2=alpha2_code))
    
    #redirect to api_name route if name query string parameter set 
    if (names != []):
        return redirect(url_for('api_name', input_name=names))

    return render_template('index.html', string=""), 200

@app.route('/all', methods=['GET'])
@app.route('/all/', methods=['GET'])
def all():
    """
    Flask route for all path. Return all ISO3166-2 data
    for all countries. This path is not reccommended as
    the file with all ISO 3166-2 data is quite large and
    can take some time to load. Route can accept path with 
    or without trailing slash.

    Parameters
    ----------
    None

    Returns
    -------
    :jsonify(all_iso3166_2) : json
      jsonified ISO 3166-2 data.
    :status_code : int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    """  
    #return error if blob not found in bucket 
    if not (blob_exists):
        return jsonify(blob_not_found_error_message), 400
    return jsonify(all_iso3166_2), 200

@app.route('/api/name/<name>', methods=['GET'])
@app.route('/api/name/<name>/', methods=['GET'])
def api_name(name):
    """
    Flask route for name path. Return all ISO 3166-2 data
    for input country name/names. A closeness function is used
    on the input countries, the closest match, to a high degree,
    for the input country from the list of available countries 
    will be used. Return error if invalid country name input. 
    Route can accept path with or without trailing slash.

    Parameters
    ----------
    :name : str/list
        one or more names for countries as they are commonly known in
        english. 

    Returns
    -------
    :iso3166_2 : json
      jsonified response of iso3166-2 data per input country name.
    :status_code : int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    """
    #initialise vars
    iso3166_2 = {}
    alpha2_code = []
    names = []

    #return error if blob not found in bucket 
    if not (blob_exists):
        return jsonify(blob_not_found_error_message), 400

    #if no input parameters set then return error message
    if (name == ""):
        error_message["message"] = "The name input parameter cannot be empty."
        error_message['path'] = request.base_url
        return jsonify(error_message), 400

    #sort country names, uppercase
    names = sorted([name])

    for name_ in names:
        #return error if country name not found
        if not (name_.upper() in list(iso3166.countries_by_name.keys())):
            error_message["message"] = "Country name not found {} in ISO3166.".format(name_)
            error_message['path'] = request.base_url
            return jsonify(error_message), 400
        else:
            #use iso3166 package to find corresponding alpha-2 code from its name
            alpha2_code.append(iso3166.countries_by_name[name.upper()].alpha2)
    
    #create iso3166-2 object from alpha-2 codes
    for code in alpha2_code:
        #get country data from ISO3166-2 object
        iso3166_2[code] = all_iso3166_2[code]

    return jsonify(iso3166_2), 200

@app.route('/api/alpha2/<alpha2>', methods=['GET'])
@app.route('/api/alpha2/<alpha2>/', methods=['GET'])
def api_alpha2(alpha2):
    """
    Flask route for alpha-2 path. Return all ISO3166-2 data
    for the inputted alpha-2 code/codes. If invalid alpha-2
    code or no value input then return error. The endpoint
    can also accept a country in its 3 letter alpha-3 code
    form, which will then be converted into its 2 letter
    alpha-2 counterpart. Route can accept path with or 
    without trailing slash.

    Parameters
    ----------
    :alpha2 : str
        2 letter alpha-2 country code or list of codes. Function 
        can also accept 3 letter alpha-3 code.

    Returns
    -------
    :iso3166_2 : json
      jsonified response of iso3166-2 data per input alpha-2 code.
    :blob_not_found_error_message : dict 
        error message if issue finding iso3166-2 object json.  
    :status_code : int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input.
    """
    #initialise vars
    iso3166_2 = {}
    alpha2_code = []

    #return error if blob not found in bucket 
    if not (blob_exists):
        return jsonify(blob_not_found_error_message), 400

    #sort and uppercase all alpha-2 codes
    alpha2_code = sorted([alpha2.upper()])

    #if no input parameters set then return all country update iso3166_updates
    if (alpha2_code == []):
        error_message["message"] = "The alpha-2 input parameter cannot be empty."
        error_message['path'] = request.base_url
        return jsonify(error_message), 400
    
    def convert_to_alpha2(alpha3_code):
        """ 
        Convert an ISO3166 country's 3 letter alpha-3 code into its 2 letter
        alpha-2 counterpart. 

        Parameters 
        ----------
        :alpha3_code: str
            3 letter ISO3166 country code.
        
        Returns
        -------
        :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
            2 letter ISO3166 country code. 
        """
        #return error if 3 letter alpha-3 code not found
        if not (alpha3_code in list(iso3166.countries_by_alpha3.keys())):
            return None
        else:
            #use iso3166 package to find corresponding alpha-2 code from its alpha-3
            return iso3166.countries_by_alpha3[alpha3_code].alpha2

    #validate multiple alpha-2 codes input, remove any invalid ones
    if (alpha2_code != []):
        if (',' in alpha2_code[0]):
            alpha2_code = alpha2_code[0].split(',')
            alpha2_code = [code.strip() for code in alpha2_code]
            for code in range(0, len(alpha2_code)):
                #api can accept 3 letter alpha-3 code for country, this has to be converted into its alpha-2 counterpart
                if (len(alpha2_code[code]) == 3):
                    temp_code = convert_to_alpha2(alpha2_code[code])
                    #return error message if invalid alpha-3 code input
                    if (temp_code is None):
                        error_message["message"] = f"Invalid 3 letter alpha-3 code input: {''.join(alpha2_code[code])}."
                        error_message['path'] = request.base_url
                        return jsonify(error_message), 400
                    alpha2_code[code] = temp_code
                #use regex to validate format of alpha-2 codes
                if not (bool(re.match(r"^[A-Z]{2}$", alpha2_code[code]))) or (alpha2_code[code] not in list(iso3166.countries_by_alpha2.keys())):
                    alpha2_code.remove(alpha2_code[code])
        else:
            #api can accept 3 letter alpha-3 code for country, this has to be converted into its alpha-2 counterpart
            if (len(alpha2_code[0]) == 3):
                temp_code = convert_to_alpha2(alpha2_code[0])
                #return error message if invalid alpha-3 code input
                if (temp_code is None):
                    error_message["message"] = f"Invalid 3 letter alpha-3 code input: {''.join(alpha2_code[0])}."
                    error_message['path'] = request.base_url
                    return jsonify(error_message), 400
                alpha2_code[0] = temp_code
            #if single alpha-2 code passed in, validate its correctness
            if not (bool(re.match(r"^[A-Z]{2}$", alpha2_code[0]))) or \
                (alpha2_code[0] not in list(iso3166.countries_by_alpha2.keys()) and \
                alpha2_code[0] not in list(iso3166.countries_by_alpha3.keys())):
                error_message["message"] = f"Invalid 2 letter alpha-2 code input: {''.join(alpha2_code)}."
                error_message['path'] = request.base_url
                return jsonify(error_message), 400

    # #get updates from iso3166_updates object per country using alpha-2 code
    for code in alpha2_code:
        iso3166_2[code] = all_iso3166_2[code]

    return jsonify(iso3166_2), 200

@app.errorhandler(404)
def not_found(e):
    """
    Return html template for 404.html when page/path not found in 
    Flask app.

    Parameters
    ----------
    :e : int
        error code.

    Returns
    -------
    :render_template : html
      Flask html template for error.html page.
    :status_code : int
        response status code. 404 code implies page not found.
    """
    error_message_ = ""
    if (request.path.endswith("/") and request.path[:-1] in all_endpoints):
        return redirect(request.path[:-1]), 302
    if not ("api" in request.path):
        error_message_ = "Path " + request.path + " should have the /api path prefix in it." 
    else:
        error_message_ = "ISO 3166-2: Page not found: " + request.path

    return render_template("404.html", path=error_message_), 404

if __name__ == '__main__':
    #run Flask app 
    app.run(debug=True)