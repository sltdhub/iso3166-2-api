from flask import Flask, request, render_template, jsonify
import iso3166
import iso3166_2 as iso3166_2
import re
from difflib import get_close_matches

#initialise Flask app
app = Flask(__name__)

#register routes/endpoints with or without trailing slash
app.url_map.strict_slashes = False

#json object storing the error message, route and status code 
error_message = {}
error_message["status"] = 400

#get all subdivision data from the ISO 3166-2 package
all_iso3166_2 = iso3166_2.country.all

@app.route('/')
@app.route('/api')
@app.route('/api/')
def home():
    """
    Default route for https://iso3166-2-api.vercel.app/. Main homepage for API displaying the 
    purpose of API and its documentation. Route can accept path with or without trailing slash.

    Parameters
    ==========
    None

    Returns
    =======
    :flask.render_template: html
      Flask html template for index.html page.
    """
    return render_template('index.html')

@app.route('/api/all', methods=['GET'])
@app.route('/api/all/', methods=['GET'])
def all():
    """
    Flask route for '/api/all' path/endpoint. Return all ISO 3166-2 subdivision data 
    attributes and values for all countries. Route can accept path with or without 
    trailing slash.

    Parameters
    ==========
    None

    Returns
    =======
    :jsonify(all_iso3166_2): json
        jsonified ISO 3166-2 subdivision data.
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    """  
    return jsonify(all_iso3166_2), 200

@app.route('/api/subd/<subd>', methods=['GET'])
@app.route('/api/subd/<subd>/', methods=['GET'])
@app.route('/subd/<subd>', methods=['GET'])
@app.route('/subd/<subd>/', methods=['GET'])
def api_iso3166_2(subd):    
    """
    Flask route for '/api/subd' path/endpoint. Return all ISO 3166-2 subdivision data for the
    inputted subdivision, according to its ISO 3166-2 code. If invalid subdivision code or no 
    value input then return error. Route can accept path with or without trailing slash.

    Parameters
    ==========
    :subd: str/list
        ISO 3166-2 subdivision code or list of codes.

    Returns
    =======
    :iso3166_2: json
        jsonified response of iso3166-2 data per input subdivision code.
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input.
    """
    #initialise vars
    iso3166_2 = {}
    subd_code = []
    country_subd_code = {}

    #set path url for error message object
    error_message['path'] = request.base_url

    #get list of all available subdivision codes
    all_iso3166_2_codes = []
    for country in all_iso3166_2:
        for subd_code in all_iso3166_2[country]:
            all_iso3166_2_codes.append(subd_code)
            
    #sort and uppercase all subdivision codes, remove any unicode spaces (%20)
    subd_code = sorted([subd.upper().replace(' ','').replace('%20', '')])

    #if no input parameters set then raise and return error
    if (subd_code == []):
        error_message["message"] = "The subdivision input parameter cannot be empty."
        return jsonify(error_message), 400
    else:
        #iterate over each subd code, validate each subdivision is in correct format
        for code in subd_code:
            if not ('-' in code):
                error_message["message"] = "All subdivision codes must be in the format XX-Y, XX-YY or XX-YYY: {}.".format(code)
                error_message['path'] = request.base_url
                return jsonify(error_message), 400
            
    #if first element in subdivision list is comma seperated list of codes, split into actual array of comma seperated codes
    if (',' in subd_code[0]):
        subd_code = subd_code[0].split(',')
        subd_code = [code.strip() for code in subd_code]
        for code in range(0, len(subd_code)):
            #use regex to validate format of subdivision codes - raise error if format is invalid
            if not (bool(re.match(r"^[A-Z]{2}-[A-Z0-9]{1,3}$", subd_code[code]))) or (subd_code[code] not in all_iso3166_2_codes):
                error_message["message"] = "All subdivision codes must be in the format XX-Y, XX-YY or XX-YYY: {}.".format(subd_code[code])
                return jsonify(error_message), 400
            #split subdivision code into country code and subdivision code e.g GB-ABD will be split into {"GB": "GB-ABD"}
            country_subd_code[subd_code[code].split('-')[0]] = subd_code[code]
    else:
        #if single subdivision code passed in, validate its correctness - raise error if invalid
        if not (bool(re.match(r"^[A-Z]{2}-[A-Z0-9]{1,3}$", subd_code[0]))): 
            error_message["message"] = f"All subdivision codes must be in the format XX-Y, XX-YY or XX-YYY: {''.join(subd_code)}."
            return jsonify(error_message), 400            
        if (subd_code[0] not in all_iso3166_2_codes):
            error_message["message"] = f"Subdivision code {subd_code[0]} not found in list of available subdivisions for {subd_code[0].split('-')[0]}."
            return jsonify(error_message), 400  

        #split subdivision code into country code and subdivision code e.g GB-ABD will be split into {"GB": "GB-ABD"}
        country_subd_code[subd_code[0].split('-')[0]] = subd_code[0]

    #get subdivision data from iso3166_2 object per country using ISO 3166-2 code
    for country, code in country_subd_code.items():
        iso3166_2[code] = all_iso3166_2[country][code]

    return jsonify(iso3166_2), 200

@app.route('/api/alpha2/<alpha2>', methods=['GET'])
@app.route('/api/alpha2/<alpha2>/', methods=['GET'])
@app.route('/alpha2/<alpha2>', methods=['GET'])
@app.route('/alpha2/<alpha2>/', methods=['GET'])
def api_alpha2(alpha2):
    """
    Flask route for '/api/alpha2' path/endpoint. Return all ISO 3166-2 subdivision data for the
    inputted alpha-2 code/codes. If invalid alpha-2 code or no value input then return error. The 
    endpoint can also accept a country in its 3 letter alpha-3 code form, which will then be converted 
    into its 2 letter alpha-2 counterpart. Route can accept path with or without trailing slash.

    Parameters
    ==========
    :alpha2: str/list
        2 letter alpha-2 country code or list of codes. Function can also accept 3 letter alpha-3 code.

    Returns
    =======
    :iso3166_2: json
        jsonified response of iso3166-2 data per input alpha-2 code. 
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input.
    """
    #initialise vars
    iso3166_2 = {}
    alpha2_code = []

    #set path url for error message object
    error_message['path'] = request.base_url

    #sort and uppercase all alpha-2 codes, remove any unicode spaces (%20)
    alpha2_code = sorted([alpha2.upper().replace(' ','').replace('%20', '')])

    #if no input parameters set then raise and return error
    if (alpha2_code == []):
        error_message["message"] = "The alpha-2 input parameter cannot be empty."
        error_message['path'] = request.base_url
        return jsonify(error_message), 400
    
    def convert_to_alpha2(alpha3_code):
        """ 
        Convert an ISO 3166 country's 3 letter alpha-3 code into its 2 letter
        alpha-2 counterpart. 

        Parameters 
        ==========
        :alpha3_code: str
            3 letter ISO 3166 country code.
        
        Returns
        =======
        :iso3166.countries_by_alpha3[alpha3_code].alpha2: str
            2 letter ISO 3166 country code. 
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
                        return jsonify(error_message), 400
                    alpha2_code[code] = temp_code
                #use regex to validate format of alpha-2 codes - if invalid then return error
                if not (bool(re.match(r"^[A-Z]{2}$", alpha2_code[code]))) or (alpha2_code[code] not in list(iso3166.countries_by_alpha2.keys())):
                    error_message["message"] = f"Invalid alpha-2 country code input: {''.join(alpha2_code[code])}."
                    return jsonify(error_message), 400
        else:
            #api can accept 3 letter alpha-3 code for country, this has to be converted into its alpha-2 counterpart
            if (len(alpha2_code[0]) == 3):
                temp_code = convert_to_alpha2(alpha2_code[0])
                #return error message if invalid alpha-3 code input
                if (temp_code is None):
                    error_message["message"] = f"Invalid 3 letter alpha-3 code input: {''.join(alpha2_code[0])}."
                    return jsonify(error_message), 400
                alpha2_code[0] = temp_code
            #if single alpha-2 code passed in, validate its correctness, raise error if invalid
            if not (bool(re.match(r"^[A-Z]{2}$", alpha2_code[0]))) or \
                (alpha2_code[0] not in list(iso3166.countries_by_alpha2.keys()) and \
                alpha2_code[0] not in list(iso3166.countries_by_alpha3.keys())):
                error_message["message"] = f"Invalid 2 letter alpha-2 code input: {''.join(alpha2_code)}."
                return jsonify(error_message), 400

    #get subdivision data from iso3166_2 object per country using alpha-2 code
    for code in alpha2_code:
        iso3166_2[code] = all_iso3166_2[code]

    return jsonify(iso3166_2), 200

@app.route('/api/name/<name>', methods=['GET'])
@app.route('/api/name/<name>/', methods=['GET'])
@app.route('/name/<name>', methods=['GET'])
@app.route('/name/<name>/', methods=['GET'])
def api_name(name):
    """
    Flask route for 'api/name' path/endpoint. Return all ISO 3166-2 subdivision data attributes and 
    values for inputted country name/names. A closeness function is used on the input country name 
    to get the closest match, to a high degree, from the list of available countries, e.g if Swede 
    is input then the data for Sweden will be returned. Return error if invalid country name input. 
    Route can accept path with or without trailing slash.

    Parameters
    ==========
    :name: str/list
        one or more country names as they are commonly known in English. 

    Returns
    =======
    :iso3166_2: json
        jsonified response of iso3166-2 data per input country name.
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    """
    #initialise vars
    iso3166_2 = {}
    alpha2_code = []
    names = []

    #set path url for error message object
    error_message['path'] = request.base_url

    #if no input parameters set then return error message
    if (name == ""):
        error_message["message"] = "The name input parameter cannot be empty."
        error_message['path'] = request.base_url
        return jsonify(error_message), 400

    #remove unicode space (%20) from input parameter
    name = name.replace('%20', ' ').title()

    #path can accept multiple country names, seperated by a comma but several
    #countries contain a comma already in their name. Seperate multiple country names
    #by comma, cast to a sorted list, unless any of the names are in the below list
    name_comma_exceptions = ["BOLIVIA, PLURINATIONAL STATE OF",
                    "BONAIRE, SINT EUSTATIUS AND SABA",
                    "CONGO, DEMOCRATIC REPUBLIC OF THE",
                    "IRAN, ISLAMIC REPUBLIC OF",
                    "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
                    "KOREA, REPUBLIC OF",
                    "MICRONESIA, FEDERATED STATES OF",
                    "MOLDOVA, REPUBLIC OF",
                    "PALESTINE, STATE OF",
                    "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA",
                    "TAIWAN, PROVINCE OF CHINA",
                    "TANZANIA, UNITED REPUBLIC OF",
                    "VIRGIN ISLANDS, BRITISH",
                    "VIRGIN ISLANDS, U.S.",
                    "VENEZUELA, BOLIVARIAN REPUBLIC OF"]
    
    #check if input country is in above list, if not add to sorted comma seperated list    
    if (name.upper() in name_comma_exceptions):
        names = [name]
    else:
        names = sorted(name.split(','))
    
    #list of country name exceptions that are converted into their more common name
    name_converted = {"UAE": "United Arab Emirates", "Brunei": "Brunei Darussalam", "Bolivia": "Bolivia, Plurinational State of", 
                      "Bosnia": "Bosnia and Herzegovina", "Bonaire": "Bonaire, Sint Eustatius and Saba", "DR Congo": 
                      "Congo, the Democratic Republic of the", "Ivory Coast": "Côte d'Ivoire", "Cape Verde": "Cabo Verde", 
                      "Cocos Islands": "Cocos (Keeling) Islands", "Falkland Islands": "Falkland Islands (Malvinas)", 
                      "Micronesia": "Micronesia, Federated States of", "United Kingdom": "United Kingdom of Great Britain and Northern Ireland",
                      "South Georgia": "South Georgia and the South Sandwich Islands", "Iran": "Iran, Islamic Republic of",
                      "North Korea": "Korea, Democratic People's Republic of", "South Korea": "Korea, Republic of", 
                      "Laos": "Lao People's Democratic Republic", "Moldova": "Moldova, Republic of", "Saint Martin": "Saint Martin (French part)",
                      "Macau": "Macao", "Pitcairn Islands": "Pitcairn", "South Georgia": "South Georgia and the South Sandwich Islands",
                      "Heard Island": "Heard Island and McDonald Islands", "Palestine": "Palestine, State of", 
                      "Saint Helena": "Saint Helena, Ascension and Tristan da Cunha", "St Helena": "Saint Helena, Ascension and Tristan da Cunha",              
                      "Saint Kitts": "Saint Kitts and Nevis", "St Kitts": "Saint Kitts and Nevis", "St Vincent": "Saint Vincent and the Grenadines", 
                      "St Lucia": "Saint Lucia", "Saint Vincent": "Saint Vincent and the Grenadines", "Russia": "Russian Federation", 
                      "Sao Tome and Principe":" São Tomé and Príncipe", "Sint Maarten": "Sint Maarten (Dutch part)", "Syria": "Syrian Arab Republic", 
                      "Svalbard": "Svalbard and Jan Mayen", "French Southern and Antarctic Lands": "French Southern Territories", "Turkey": "Türkiye", 
                      "Taiwan": "Taiwan, Province of China", "Tanzania": "Tanzania, United Republic of", "USA": "United States of America", 
                      "United States": "United States of America", "Vatican City": "Holy See", "Vatican": "Holy See", "Venezuela": 
                      "Venezuela, Bolivarian Republic of", "Virgin Islands, British": "British Virgin Islands"}
    
    #iterate over list of names, convert country names from name_converted dict, if applicable
    for name_ in range(0, len(names)):
        if (names[name_].title() in list(name_converted.keys())):
            names[name_] = name_converted[names[name_]]

    #remove all whitespace in any of the country names
    names = [name_.strip(' ') for name_ in names]

    #get list of available country names from iso3166 library, remove whitespace
    all_names_no_space = [name_.strip(' ') for name_ in list(iso3166.countries_by_name.keys())]
    
    #iterate over all input country names, get corresponding 2 letter alpha-2 code
    for name_ in names:

        #get list of country name matches from input name using closeness function, using default cutoff parameter value
        name_matches = get_close_matches(name_.upper(), all_names_no_space)
        matching_name = ""

        #get highest matching country name from one input (manually set British Virgin Islands vs US Virgin Islands)
        if (name_matches != []):
            if (name_ == "British Virgin Islands"):
                matching_name = name_matches[1]
            else:
                matching_name = name_matches[0]
        else:
            #return error if country name not found
            error_message["message"] = "Country name {} not found in the ISO 3166.".format(name_)
            return jsonify(error_message), 400

        #use iso3166 package to find corresponding alpha-2 code from its name
        alpha2_code.append(iso3166.countries_by_name[matching_name.upper()].alpha2)
    
    #get country data from ISO 3166-2 object, using alpha-2 code
    for code in alpha2_code:
        iso3166_2[code] = all_iso3166_2[code]

    return jsonify(iso3166_2), 200

@app.errorhandler(404)
def not_found(e):
    """
    Return html template for 404.html when page/path not found in Flask app.

    Parameters
    ==========
    :e: int
        error code.

    Returns
    =======
    :flask.render_template: html
      Flask html template for 404.html page.
    :status_code: int
        response status code. 404 code implies page not found.
    """
    return render_template("404.html", path=request.url), 404

if __name__ == '__main__':
    #run Flask app 
    app.run(debug=True)