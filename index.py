from flask import Flask, request, render_template, jsonify
import iso3166
from iso3166_2 import *
import re
from unidecode import unidecode
from difflib import get_close_matches

#initialise Flask app
app = Flask(__name__)

#register routes/endpoints with or without trailing slash
app.url_map.strict_slashes = False

############################################### Endpoints #################################################

# /api - main homepage for API, displaying purpose and documentation
# /api/all - return all subdivision data for all countries
# /api/alpha - return all subdivision data for input country using its alpha-2, alpha-3 or numeric codes  
# /api/subdivision - return subdivision data for input subdivision using its subdivision code             
# /api/country_name - return all subdivision data for input country using its country name                        
# /api/name - return all subdivision data for input subdivision using its subdivision name    

###########################################################################################################

#json object storing the error message, route and status code 
error_message = {}
error_message["status"] = 400

#get all subdivision data from the ISO 3166-2 package
iso3166_2_instance = ISO3166_2()
all_iso3166_2 = iso3166_2_instance.all

@app.route('/')
@app.route('/api')
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
@app.route('/all', methods=['GET'])
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

@app.route('/api/subdivision/<subd>', methods=['GET'])
@app.route('/subdivision/<subd>', methods=['GET'])
@app.route('/api/subdivision', methods=['GET'])
@app.route('/subdivision', methods=['GET'])
def api_subdivision(subd=""):    
    """
    Flask route for '/api/subdivision' path/endpoint. Return all ISO 3166-2 subdivision data 
    for the inputted subdivision, according to its ISO 3166-2 code. A comma seperated list of 
    subdivision codes can also be input. If invalid subdivision code or no value input then 
    return error. Route can accept path with or without trailing slash.

    Parameters
    ==========
    :subd: str/list (default="")
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

    #set path url for error message object
    error_message['path'] = request.base_url

    #get list of all available subdivision codes
    all_iso3166_2_codes = []
    for country in all_iso3166_2:
        for subd_code in all_iso3166_2[country]:
            all_iso3166_2_codes.append(subd_code)
            
    #sort and uppercase all subdivision codes, remove any unicode spaces (%20)
    subd_code = sorted([subd.upper().replace(' ','').replace('%20', '')])
    
    #if no input parameters set then return error
    if (subd_code == ['']):
        error_message["message"] = "The subdivision input parameter cannot be empty."
        return jsonify(error_message), 400

    #if first element in subdivision list is comma seperated list of codes, split into actual array of comma seperated codes
    if (',' in subd_code[0]):
        subd_code = subd_code[0].split(',')
        subd_code = [code.strip() for code in subd_code]

    #iterate over each subdivision code and validate its format and check if exists in dataset, if not then return error
    for subd in range(0, len(subd_code)):
        if not (bool(re.match(r"^[A-Z]{2}-[A-Z0-9]{1,3}$", subd_code[subd]))):
            error_message["message"] = "All subdivision codes must be in the format XX-Y, XX-YY or XX-YYY: {}.".format(subd_code[subd])
            return jsonify(error_message), 400
        if (subd_code[subd] not in all_iso3166_2_codes):
            error_message["message"] = f"Subdivision code {subd_code[subd]} not found in list of available subdivisions for {subd_code[subd].split('-')[0]}."
            return jsonify(error_message), 400

        #create empty country object for country subdivision data, if code is valid, using subdivision code as key
        if not (subd_code in all_iso3166_2_codes):
            iso3166_2[subd_code[subd]] = {}

        #add respective subdivision data to object
        iso3166_2[subd_code[subd]]= all_iso3166_2[subd_code[subd].split('-')[0]][subd_code[subd]]

    return jsonify(iso3166_2), 200

@app.route('/api/alpha/<alpha>', methods=['GET'])
@app.route('/alpha/<alpha>', methods=['GET'])
@app.route('/api/alpha', methods=['GET'])
@app.route('/alpha', methods=['GET'])
def api_alpha(alpha=""):
    """
    Flask route for '/api/alpha' path/endpoint. Return all ISO 3166-2 subdivision data for the 
    country with the inputted ISO 3166-1 alpha-2, alpha-3 or numeric code/codes. If invalid alpha 
    code or no value input then return error. Route can accept path with or without trailing slash.

    Parameters
    ==========
    :alpha: str/list (default="")
        2 letter alpha-2, 3 letter alpha-3 or numeric country code or list of codes. If default
        value then return error.

    Returns
    =======
    :iso3166_2: json
        jsonified response of iso3166-2 data per input alpha code. 
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input.
    """
    #initialise vars
    iso3166_2 = {}
    alpha_code = []

    #set path url for error message object
    error_message['path'] = request.base_url

    #sort and uppercase all alpha codes, remove any unicode spaces (%20)
    alpha_code = sorted([alpha.upper().replace(' ','').replace('%20', '')])

    #if no input parameters set then raise and return error
    if (alpha_code == ['']):
        error_message["message"] = "The alpha input parameter cannot be empty."
        return jsonify(error_message), 400
    
    def convert_to_alpha2(alpha_code):
        """ 
        Convert an ISO 3166 country's 3 letter alpha-3 code or numeric code into its 
        2 letter alpha-2 counterpart. 

        Parameters 
        ==========
        :alpha_code: str
            3 letter ISO 3166 alpha-3 country code or numeric code.
        
        Returns
        =======
        :iso3166.countries_by_alpha3[alpha3_code].alpha2/iso3166.countries_by_numeric[alpha_code].alpha2: str
            2 letter alpha-2 ISO 3166 country code. 
        """
        if (alpha_code.isdigit()):
            #return error if numeric code not found
            if not (alpha_code in list(iso3166.countries_by_numeric.keys())):
                return None
            else:
                #use iso3166 package to find corresponding alpha-2 code from its numeric code
                return iso3166.countries_by_numeric[alpha_code].alpha2
    
        #return error if 3 letter alpha-3 code not found
        if not (alpha_code in list(iso3166.countries_by_alpha3.keys())):
            return None
        else:
            #use iso3166 package to find corresponding alpha-2 code from its alpha-3 code
            return iso3166.countries_by_alpha3[alpha_code].alpha2

    #split multiple alpha codes into list of codes, remove whitespace
    if (',' in alpha_code[0]):
        alpha_code = alpha_code[0].split(',')
        alpha_code = [code.strip() for code in alpha_code]

    #iterate over each input alpha codes, convert to equivalent alpha-2 codes if applicable, return error if invalid code
    for code in range(0, len(alpha_code)):
        #api can accept numeric code for country, this has to be converted into its alpha-2 counterpart
        if (alpha_code[0].isdigit()):
            temp_code = convert_to_alpha2(alpha_code[code])
            #return error message if invalid numeric code input
            if (temp_code is None):
                error_message["message"] = f"Invalid ISO 3166-1 numeric country code input: {''.join(alpha_code[code])}."
                return jsonify(error_message), 400
            alpha_code[code] = temp_code
        else:
            #api can accept 3 letter alpha-3 code for country, this has to be converted into its alpha-2 counterpart
            if (len(alpha_code[code]) == 3):
                temp_code = convert_to_alpha2(alpha_code[code])
                #return error message if invalid alpha-3 code input
                if (temp_code is None):
                    error_message["message"] = f"Invalid ISO 3166-2 alpha-3 country code input: {''.join(alpha_code[code])}."
                    return jsonify(error_message), 400
                alpha_code[code] = temp_code

        #use regex to validate format of alpha-2 codes - if invalid then return error
        if not (bool(re.match(r"^[A-Z]{2}$", alpha_code[code]))) or (alpha_code[code] not in list(iso3166.countries_by_alpha2.keys())):
            error_message["message"] = f"Invalid ISO 3166-1 alpha country code input: {''.join(alpha_code[code])}."
            return jsonify(error_message), 400

    #get subdivision data from iso3166_2 object per country using alpha-2 code
    for code in alpha_code:
        iso3166_2[code] = all_iso3166_2[code]
    
    return jsonify(iso3166_2), 200

@app.route('/api/country_name/<country_name>', methods=['GET'])
@app.route('/country_name/<country_name>', methods=['GET'])
@app.route('/api/country_name', methods=['GET'])
@app.route('/country_name', methods=['GET'])
def api_country_name(country_name=""):
    """
    Flask route for '/api/country_name' path/endpoint. Return all ISO 3166-2 subdivision data attributes and 
    values for inputted country name/names. A closeness function is used on the input country name 
    to get the closest match, to a high degree, from the list of available countries, e.g if Swede 
    is input then the data for Sweden will be returned. Return error if invalid country name or no name 
    parameter input. Route can accept path with or without trailing slash.

    Parameters
    ==========
    :country_name: str/list (default="")
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

    #remove unicode space (%20) from input parameter
    name = country_name.replace('%20', ' ').title()

    #set path for current request url 
    error_message['path'] = request.base_url

    #if no input parameters set then return error message
    if (name == ""):
        error_message["message"] = "The country name input parameter cannot be empty."
        return jsonify(error_message), 400

    #path can accept multiple country names, seperated by a comma but several
    #countries contain a comma already in their name. If multiple country names input,  
    #seperate by comma, cast to a sorted list, unless any of the names are in the below list
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

        #get list of exact country name matches from input name using closeness function, using cutoff of 100%
        name_matches = get_close_matches(name_.upper(), all_names_no_space, cutoff=1)
        matching_name = ""

        #if no exact matching country name found, reduce the cutoff to 80%
        if (name_matches == []):
            name_matches = get_close_matches(name_.upper(), all_names_no_space, cutoff=0.8)

        #get highest matching country name from one input (manually set British Virgin Islands vs US Virgin Islands)
        if (name_matches != []):
            if (name_ == "British Virgin Islands"):
                matching_name = name_matches[1]
            else:
                matching_name = name_matches[0]
        else:
            #return error if country name not found
            error_message["message"] = "Invalid country name input: {}.".format(name_)
            return jsonify(error_message), 400

        #use iso3166 package to find corresponding alpha-2 code from its name
        alpha2_code.append(iso3166.countries_by_name[matching_name.upper()].alpha2)
    
    #get country data from ISO 3166-2 object, using alpha-2 code
    for code in alpha2_code:
        iso3166_2[code] = all_iso3166_2[code]

    return jsonify(iso3166_2), 200

@app.route('/api/name/<subdivision_name>', methods=['GET'])
@app.route('/name/<subdivision_name>', methods=['GET'])
@app.route('/api/name', methods=['GET'])
@app.route('/name', methods=['GET'])
def api_subdivision_name(subdivision_name=""):
    """
    Flask route for '/api/name' path/endpoint. Return all ISO 3166-2 subdivision data attributes and 
    values for inputted subdivision name/names. When searching for the sought subdivision name, a 
    closeness function is used to find the exact match within the dataset, if this returns nothing 
    then the dataset is searched for subdivision names that match 90% or more, the first match will
    then be returned. If no matching subdivision name found or input is empty then return an error. 
    Route can accept path with or without trailing slash.

    Parameters
    ==========
    :subdivision_name: str/list (default="")
        one or more subdivision names as they are commonly known in English. 

    Returns
    =======
    :iso3166_2: json
        jsonified response of iso3166-2 data per input subdivision name.
    :status_code: int
        response status code. 200 is a successful response, 400 means there was an 
        invalid parameter input. 
    """
    #if no input parameters set then raise and return error
    if (subdivision_name == ""):
        error_message["message"] = "The subdivision name input parameter cannot be empty."
        error_message['path'] = request.base_url
        return jsonify(error_message), 400
    
    #object to store the subdivision name and its corresponding alpha-2 code and subdivision code (name: alpha_2, code: subd_code)
    all_subdivision_names = {}

    #list to store all subdivision names for all countries
    all_subdivision_names_list = []

    #list of subdivision names with comma in them from dataset, required if multiple subdivison names are input e.g - Murcia, Regiónde, Newry, Mourne and Down
    subdivision_name_expections = []

    #seperate list to keep track if any of input subdivsion names are exceptions (have comma in them)
    subdivision_name_expections_input = []
    
    #iterate over all ISO 3166-2 subdivision data, appending each subdivision's name, country code and 
    #subdivision code to object that will be used to search through, lowercase, remove whitespace and any accents,
    #if a comma is in the official subdivision name then append to the exception list only if comma is in input parameter
    for alpha_2 in all_iso3166_2:
        for subd in all_iso3166_2[alpha_2]:

            #append object of the subdivison's alpha-2 code and subdivision code with its name as the key
            if not (unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', '')) in list(all_subdivision_names.keys())):
                all_subdivision_names[unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', ''))]  = []
                all_subdivision_names[unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', ''))].append({"alpha2": alpha_2, "code": subd})
            else:
                all_subdivision_names[unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', ''))].append({"alpha2": alpha_2, "code": subd})

            #append subdivision name to list of subdivision names for searching
            all_subdivision_names_list.append(unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', '')))

            #if comma in official subdivision name, append to the exception list, which is needed if a comma seperated list of names are input
            if (',' in subdivision_name):
                if (',' in unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', ''))):
                    subdivision_name_expections.append(unidecode(all_iso3166_2[alpha_2][subd]["name"].lower().replace(' ', '')))

    #only execute subdivision name exception code if comma is in input param
    if (',' in subdivision_name):
        #sort exceptions list alphabetically 
        subdivision_name_expections.sort()

        #temp var to track input subdivision name 
        temp_subdivision_name = unidecode(subdivision_name.lower().replace(' ', '').replace('%20', ''))

        #iterate over all subdivision names exceptions (those with a comma in them), append to seperate list if input param is one
        for sub_name in subdivision_name_expections:
            if (sub_name in temp_subdivision_name):
                subdivision_name_expections_input.append(sub_name)
                #remove current subdivision name from temp var, strip of commas
                subdivision_name = temp_subdivision_name.replace(sub_name, '').strip(',')

    #sort and lowercase all subdivision names codes, remove any unicode spaces (%20) and accents
    subdivision_names = sorted([unidecode(subdivision_name.lower().replace(' ','').replace('%20', ''))])
    
    #split multiple subdivision names into list
    subdivision_names = subdivision_names[0].split(',')

    #extend subdivsion names list if any subdivision name exceptions are present in input param
    if (subdivision_name_expections_input != []):
        subdivision_names.extend(subdivision_name_expections_input)

    #object to keep track of matching subdivisions and their data
    output_subdivisions =  {}

    #iterate over all input subdivision names, and find matching subdivision in data object
    for subdiv in subdivision_names: 

        #using difflib library, try getting exact matching subdivision name from list, using cutoff of 100% likeness
        subdivision_name_matches = get_close_matches(subdiv, all_subdivision_names_list, cutoff=1.0)

        #if no exact match found previously, get closest matching subdivision name from list, using cutoff of 90% likeness
        if (subdivision_name_matches == []):
            subdivision_name_matches = get_close_matches(subdiv, all_subdivision_names_list, cutoff=0.9)
        
        #return subdivision data if one match found, get matching subdivision from object
        if (len(subdivision_name_matches) == 1):
            #create temp object for subdivision and its data attributes, with its subdivision code as key
            subdivision = all_iso3166_2[all_subdivision_names[subdivision_name_matches[0]][0]["alpha2"]][all_subdivision_names[subdivision_name_matches[0]][0]["code"]]
            #append subdivision data and its attributes to the output object
            output_subdivisions[all_subdivision_names[subdivision_name_matches[0]][0]["code"]] = subdivision

        #return list of subdivision data objects if multiple matches found
        else:
            for subd in range(0, len(subdivision_name_matches)): 
                for obj in range(0, len(all_subdivision_names[subdivision_name_matches[subd]])):
                    #create temp object for subdivision and its data attributes, with its subdivision code as key
                    subdivision = all_iso3166_2[all_subdivision_names[subdivision_name_matches[subd]][obj]["alpha2"]][all_subdivision_names[subdivision_name_matches[subd]][obj]["code"]]
                    #append subdivision data and its attributes to the output object
                    output_subdivisions[all_subdivision_names[subdivision_name_matches[subd]][obj]["code"]] = subdivision

    #return error if no matching subdivisions found from input name    
    if (output_subdivisions == {}):
        error_message["message"] = "No valid subdivision found for input name: {}.".format(subdivision_name)
        error_message['path'] = request.base_url
        return jsonify(error_message), 400  

    #return object of matching subdivisions and their data
    else:
        return jsonify(output_subdivisions), 200

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
    #validation in the case of user inputting /alpha2, /alpha3 or /numeric endpoint instead of /alpha
    if any(alpha in request.url for alpha in ["alpha2", "alpha3", "numeric"]):
        return render_template("404.html", path=request.url, 
            alpha_endpoint_message="Searching via a country's alpha code (alpha-2, alpha-3 or numeric code) should use the /alpha endpoint."), 404

    return render_template("404.html", path=request.url), 404

if __name__ == '__main__':
    #run Flask app 
    app.run(debug=True)