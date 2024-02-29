# iso3166-2-api 🌎
<!-- ![Vercel](https://vercelbadge.vercel.app/api/amckenna41/iso3166-2-api) -->
![Vercel](https://therealsujitk-vercel-badge.vercel.app/?app=iso3166-2-api)
[![pytest](https://github.com/amckenna41/iso3166-2-api/workflows/Building%20and%20Testing/badge.svg)](https://github.com/amckenna41/iso3166-2-api/actions?query=workflowBuilding%20and%20Testing)
[![iso3166_updates](https://img.shields.io/pypi/v/iso3166-2)](https://pypi.org/project/iso3166-2)
[![Documentation Status](https://readthedocs.org/projects/iso3166-2/badge/?version=latest)](https://iso3166-2.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/github/license/amckenna41/iso3166-2)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/amckenna41/iso3166-2-api)](https://github.com/amckenna41/iso3166-2-api/issues)

<div alt="images" style="justify-content: center; display:flex; margin-left=50px;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/3d/Flag-map_of_the_world_%282017%29.png" alt="globe" height="200" width="500"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/e3/ISO_Logo_%28Red_square%29.svg" alt="iso" height="200" width="300"/>
</div>

> Frontend API for the [`iso3166-2`](https://github.com/amckenna41/iso3166-2) software and repo that returns a plethora of subdivision/regional data for all countries in the ISO 3166-2 standard. Built using the Python Flask framework and hosted on the Vercel platform.

The main API homepage and documentation is available via the URL: <b>[https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)</b>

* A <b>demo</b> of the software and API is available [here][demo].
* A <b>Medium</b> article that dives deeper into `iso3166-2` is available [here][medium].

Table of Contents
-----------------
- [Introduction](#introduction)
- [API](#api)
- [Staying up to date](#staying-up-to-date)
- [Requirements](#requirements)
- [Issues](#issues)
- [Contact](#contact)
- [References](#references)

Introduction
------------
This repo contains the front and backend of the API created for the [`iso3166-2`](https://github.com/amckenna41/iso3166-2) repository. The API returns a plethora of subdivison data for all countries in the ISO 3166-2 standard. Utilising the custom-built [`iso3166-2`](https://github.com/amckenna41/iso3166-2) software that incorporates data from the ISO 3166-2. Built using the Python [Flask][flask] framework and hosted on the [Vercel][vercel] platform.

[`iso3166-2`](https://github.com/amckenna41/iso3166-2) is a lightweight custom-built Python package, and accompanying API, that can be used to access all of the world's ISO 3166-2 subdivision data. Here, subdivision can be used interchangably with regions/states/provinces etc. Currently, the package and API support subdivision data from **250** officially assigned code elements within the ISO 3166-1, with **200** of these countries having recognised subdivisions (50 entires have 0 subdivisions), totalling **5,039** subdivisions across the whole dataset. Transitional reservations are not included and only 4 of the exceptional reservations, that have now been officially assigned, are included: AX (Aland Islands), GG (Guernsey), IM (Isle of Man) and JE (Jersey) [[3]](#references). The ISO 3166-2 was first published in 1998 and as of November 2023 there are 5,039 codes defined in it [[2]](#references).

The full list of additional subdivision data attributes supported are:

* Name (subdivsion name)
* Local name (subdivision name in local language)
* Code (subdivision code)
* Parent Code (subdivision parent code)
* Type (subdivision type, e.g. region, state, canton, parish etc)
* Latitude/Longitude (subdivision coordinates)
* Flag (subdivsion flag from [`iso3166-flag-icons`](https://github.com/amckenna41/iso3166-flag-icons) repo)

The ISO 3166 standard by the ISO defines codes for the names of countries, dependent territories, special areas of geographical interest, consolidated into the ISO 3166-1 standard [[1]](#references), and their principal subdivisions (e.g., provinces, states, departments, regions), which comprise the ISO 3166-2 standard [[2]](#references). The ISO 3166-1 was first published in 1974 and currently comprises 249 countries, 193 of which are sovereign states that are members of the United Nations [[1]](#references). 

API
---
The main API endpoint is:

> [https://iso3166-2-api.vercel.app/api](https://iso3166-2-api.vercel.app/api)

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha/<input_alpha>
* https://iso3166-2-api.vercel.app/api/country_name/<input_country_name>
* https://iso3166-2-api.vercel.app/api/subdivision/<input_subdivision>
* https://iso3166-2-api.vercel.app/api/name/<input_subdivision_name>

Five paths/endpoints are available in the API - `/api/all`, `/api/alpha`, `/api/country_name`, `/api/subdivision` and `/api/name`.

* The `/api/all` path/endpoint returns all of the ISO 3166 subdivision data for all countries.

* The `/api/alpha` endpoint accepts the 2 letter alpha-2, 3 letter alpha-3 and or numeric ISO 3166-1 country codes appended to the path/endpoint e.g. `/api/alpha/JP`. A single alpha-2, alpha-3 or numeric code or list of them can be passed to the API e.g. `/api/alpha/FR,DE,HU,ID,MA`, `/api/alpha/FRA,DEU,HUN,IDN,MAR` and `/api/alpha/428,504,638`. If an invalid country code is input then an error will be returned.

* The `/api/country_name` endpoint accepts the country/territory name as it is most commonly known in english, according to the ISO 3166-1 e.g. `/api/country_name/Denmark`. A single country name or list of them can be passed into the API e.g. `/api/country_name/France,Moldova,Benin`. A closeness function is utilised so the most approximate name from the input will be used e.g. Sweden will be used if input is `/api/country_name/Swede`. If no country is found from the closeness function or an invalid name is input then an error will be returned.

* The `/api/subdivision` endpoint accepts the ISO 3166-2 subdivision codes, e.g `/api/subdivision/GB-ABD`. You can also input a list of subdivision codes from the same and or different countries and the data for each will be returned e.g `/api/subdivision/IE-MO,FI-17,RO-AG`. If the input subdivision code is not in the correct format then an error will be raised. Similarly if an invalid subdivision code that doesn't exist is input then an error will be raised.

* The `/api/name/` endpoint accepts the ISO 3166-2 subdivision names, e.g `/api/name/Derry`. You can also input a list of subdivision name from the same or different countries and the data for each will be returned e.g `/api/name/Paris,Frankfurt,Rimini`. A closeness function is utilised to find the matching subdivision name, if no exact name match found then the most approximate subdivisions will be returned. Some subdivisions may have the same name, in this case eahc subdivision and its data will be returned e.g `/api/name/Saint George,Sucre`. This endpoint also has the likeness score (`?likeness=`) query string parameter that can be appended to the URL. This can be set between 1 - 100, representing a % of likeness to the input name the return subdivisions should be, e.g: a likeness score of 90 will return fewer potential matches whose name only match to a high degree compared to a score of 10 which will create a larger search space, thus returning more potential subdivision matches. A default likeness of 100 (exact match) is used, if no match found then this is reduced to 90. If an invalid subdivision name that doesn't match any is input then an error will be raised.

* The main API endpoint (`/` or `/api`) will return the homepage and API documentation.

The API documentation and usage with all useful commands and examples to the API is available on the [API.md][api_md] file.

> A demo of the software and API is available [here][demo].

Staying up to date
------------------
An important thing to note about the ISO 3166-2 and its subdivision codes/names is that changes are made consistently to it, from a small subdivision name change to an addition/deletion of a whole subdivision. These changes can happen due to a variety of geopolitical and administrative reasons. Therefore, it's important that the [`iso3166-2`](https://github.com/amckenna41/iso3166-2) library and its dataset have the most up-to-date, accurate and reliable data. To achieve this, the custom-built [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo was created.

The [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates) repo is another open-source software package and accompanying API that pulls the latest updates and changes for any and all countries in the ISO 3166 from a variety of data sources including the ISO website itself. A script is called every few months to check for any updates/changes to the subdivisions, which are communicated via the ISO's Online Browsing Platform [[4]](#references), and will then be manually incorporated into the [`iso3166-2`](https://github.com/amckenna41/iso3166-2) and dataset. Please visit the repository home page for more info about the purpose and process of the software and API - [`iso3166-updates`](https://github.com/amckenna41/iso3166-updates).

The list of ISO 3166 updates was last updated on <strong>Nov 2023</strong>. A log of the latest ISO 3166 updates can be seen in the [UPDATES.md][updates_md].

Requirements
------------
* [python][python] >= 3.8
* [flask][flask] >= 2.3.2
* [requests][requests] >= 2.28.1
* [iso3166][iso3166] >= 2.1.1
* [iso3166-2][iso3166_2] >= 1.5.0
* [unidecode][unidecode] >= 1.3.8
* [thefuzz][thefuzz] >= 0.22.1

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
[iso3166_2]: https://github.com/amckenna41/iso3166-2
[unidecode]: https://pypi.org/project/Unidecode/
[thefuzz]: https://github.com/seatgeek/thefuzz/tree/master
[google-auth]: https://cloud.google.com/python/docs/reference
[google-cloud-storage]: https://cloud.google.com/python/docs/reference
[google-api-python-client]: https://cloud.google.com/python/docs/reference
[Issues]: https://github.com/amckenna41/iso3166-2-api/issues
[vercel]: https://vercel.com/
[attributes]: https://github.com/amckenna41/iso3166-2-api/ATTRIBUTES.md 
[api_md]: https://github.com/amckenna41/iso3166-2-api/API.md 
[updates_md]: https://github.com/amckenna41/iso3166-2/blob/main/UPDATES.md
[medium]: https://ajmckenna69.medium.com/iso3166-2-71a13d9157f7