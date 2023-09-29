# iso3166-2-api 🌎

<!-- ![Vercel](https://vercelbadge.vercel.app/api/amckenna41/iso3166-2-api) -->
![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2-api)
[![pytest](https://github.com/amckenna41/iso3166-2-api/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2-api/actions?query=workflowBuilding%20and%20Testing)
[![iso3166_updates](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2-api)](https://github.com/amckenna41/iso3166-2-api/issues)

<div alt="images" style="justify-content: center; display:flex; margin-left=50px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="200" width="500"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/ISO_Logo_%28Red_square%29.svg" alt="iso" height="200" width="300"/>
</div>

> Frontend API for the iso3166-2 repo that returns a plethora of data fields for all countries in the ISO 3166-1 and ISO 3166-2 standards. Utilising the restcountries API (https://restcountries.com/) as well as the custom-built [`iso3166-2`](https://github.com/amckenna41/iso3166-2) software that incorporates additional subdivision/regional data from the ISO 3166-2. Built using the Python [Flask][flask] framework and hosted on the [Vercel][vercel] platform. A demo of the API and the Python package are available [here][demo].

The main API homepage and documentation is available via the URL:

> https://iso3166-2-api.vercel.app/api

Table of Contents
-----------------
  * [Introduction](#introduction)
  * [API](#api)
  * [Staying up to date](#staying-up-to-date)
  * [Requirements](#requirements)
  * [Issues](#Issues)
  * [Contact](#contact)
  * [References](#references)

Introduction
------------
This repo contains the front and backend of the API created for the [`iso3166-2`](https://github.com/amckenna41/iso3166-2) repository. The API returns a plethora of data fields for all countries in the ISO 3166-1 and ISO 3166-2 standards. Utilising the [RestCountries API](https://restcountries.com/) as well as the custom-built [`iso3166-2`](https://github.com/amckenna41/iso3166-2) software that incorporates data from the ISO 3166-2. Built using the Python [Flask][flask] framework and hosted on the [Vercel][vercel] platform.

[`iso3166-2`](https://github.com/amckenna41/iso3166-2) is a lightweight custom-built Python wrapper for RestCountries API (https://restcountries.com/) which includes an abundance of information about all ISO 3166 countries. But this package also includes information about all countrys' ISO 3166-2 subdivision codes & names, which is absent from RestCountries. Here, subdivision can be used interchangably with regions/states/provinces etc. The full list of additional subdivision data attributes supported are:
* Name
* Code
* Parent Code
* Type
* Latitude/Longitude
* Flag (from [iso3166-flag-icons](flag_icons_repo) repo)

The ISO 3166 standard by the ISO defines codes for the names of countries, dependent territories, special areas of geographical interest, consolidated into the ISO 3166-1 standard [[1]](#references), and their principal subdivisions (e.g., provinces, states, departments, regions), which comprise the ISO 3166-2 standard [[2]](#references). The ISO 3166-1 was first published in 1974 and currently comprises 249 countries, 193 of which are sovereign states that are members of the United Nations [[1]](#references). The ISO 3166-2 was first published in 1998 and as of 29 November 2022 there are 5,043 codes defined in it [[2]](#references).

API
---
The main API endpoint is:

> https://iso3166-2-api.vercel.app/api

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Three paths/endpoints are available in the API - `/api/all`, `/api/alpha2` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 country data for all countries (due to the size of the object this can take some time to load). 

* The 2 letter alpha-2 country code can be appended to the **alpha2** path/endpoint e.g <i>/api/alpha2/JP</i>. A single alpha-2 or list of them can be passed to the endpoint e.g <i>/api/alpha2/FR,DE,HU,ID,MA</i>. For redundancy, the 3 letter alpha-3 counterpart for each country's alpha-2 code can also be appended to the path e.g <i>/api/alpha2/FRA,DEU,HUN,IDN,MAR</i>. If an invalid alpha-2 code is input then an error will be returned.

* The name parameter can be a country name as it is most commonly known in english, according to the ISO 3166-1. The name can similarly be appended to the **name** path/endpoint e.g <i>/api/name/Denmark</i>. A single country name or list of them can be passed into the endpoint e.g <i>/api/name/France,Moldova,Benin</i>. A closeness function is utilised so that the most approximate name from the input will be used e.g Sweden will be used if the input is <i>/api/name/Swede</i>. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

The `filter` query string parameter can be appended to any of the endpoints. It accepts a string of one or more attributes that the user wants to only be returned from their request e.g  <i>/api/alpha2/IE?filter=capital,currencies,languages,region</i>. This example means that only the capital city, currencies, languages and region data for Ireland will be returned. If an invalid attribute name is input then it will be removed from the request.

The full list of attributes available for each country are available in the [ATTRIBUTES.md][attributes] file.

The API documentation and usage with all useful commands and examples to the API is available on the [API.md][api_md] file. A demo of the software and API is also available [here][demo].

Staying up to date
------------------
The ISO is a very dynamic organisation and regularly change/update/remove entries within its library of standards, including the ISO 3166. Additions/changes/deletions to country/territorial codes and attributes vary and update occassioanlly. On the main [`iso3166-2`](https://github.com/amckenna41/iso3166-2) repo a Cloud Function is periodically called periodically that pulls all the latest data and attributes for all ISO 3166 countries, ultimately updating the backend JSON file that the iso3166-2-api uses. This ensures that the object and its data stay up-to-date and accurate.  

Additionally, as the software and API include data from the ISO 3166-2 which includes country subdivison codes and data, a custom-built software [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) was created. Compared to the ISO 3166-1, changes are more frequent for the ISO 3166-2 codes due to there being thousands more entries, thus it can be difficult to keep up with any changes to these codes. These changes can occur for a variety of geopolitical and bureaucratic reasons and are usually communicated via Newsletters on the ISO platform, their Online Browsing Platform (OBP) or via a database, which usually costs money to subscribe to [[3]](#references). Usually these updates are conveyed at the end of the year, with amendments and updates occasionally published at various times throughout the year [[4]](#references). The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software tracks and maintain these changes/updates that are made. The software and accompanying API (https://iso3166-updates.com) makes it extremely easy to check for any new or historic updates to a country or set of country's ISO 3166-2 codes for free, with an easy-to-use interface and Python package and API, ensuring that you get the most up-to-date and accurate ISO 3166-2 codes and naming conventions. A custom script is run periodically (every 3-6 months) that uses the [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) software to check for any updates. If updates are found then a GitHub Issue is automatically raised on the `iso3166-2` repository, communicating all updates/changes that need to be implemented into the `iso3166-2` repo's software and JSONs.

Requirements
------------
* [python][python] >= 3.7
* [flask][flask] >= 2.3.2
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [google-auth][google-auth] >= 2.17.3
* [google-cloud-storage][google-cloud-storage] >= 2.8.0
* [google-api-python-client][google-api-python-client] >= 2.86.0

Issues
------
Any issues, errors or enhancements can be raised via the [Issues](Issues) tab in the repository.

Contact
-------
If you have any questions or comments, please contact amckenna41@qub.ac.uk or raise an issue on the [Issues][Issues] tab. <br><br>

References
----------
\[1\]: ISO3166-1: https://en.wikipedia.org/wiki/ISO_3166-1 <br>
\[2\]: ISO3166-2: https://en.wikipedia.org/wiki/ISO_3166-2 <br>
\[3\]: ISO Country Codes Collection: https://www.iso.org/publication/PUB500001 <br>
\[4\]: ISO Country Codes: https://www.iso.org/iso-3166-country-codes.html <br>
\[5\]: ISO3166-1 flag-icons repo: https://github.com/lipis/flag-icons <br>
\[6\]: ISO3166-2 flag-icons repo: https://github.com/amckenna41/iso3166-flag-icons <br>

Support
-------
<a href="https://www.buymeacoffee.com/amckenna41" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

[Back to top](#TOP)

[demo]: https://colab.research.google.com/drive/1btfEx23bgWdkUPiwdwlDqKkmUp1S-_7U?usp=sharing
[flask]: https://flask.palletsprojects.com/en/2.3.x/
[python]: https://www.python.org/downloads/release/python-360/
[requests]: https://requests.readthedocs.io/
[iso3166]: https://github.com/deactivated/python-iso3166
[google-auth]: https://cloud.google.com/python/docs/reference
[google-cloud-storage]: https://cloud.google.com/python/docs/reference
[google-api-python-client]: https://cloud.google.com/python/docs/reference
[Issues]: https://github.com/amckenna41/iso3166-2-api/issues
[vercel]: https://vercel.com/
[attributes]: https://github.com/amckenna41/iso3166-2-api/ATTRIBUTES.md 
[api_md]: https://github.com/amckenna41/iso3166-2-api/API.md 