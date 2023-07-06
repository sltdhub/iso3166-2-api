# ISO3166-2 API

As well as the Python software package, this API is also available to access a plethora of the latest data for all countries included in the ISO 3166-1. You can search for a particular country via it's name or its 2 letter alpha 2 code (e.g EG, FR, DE) via the 'name' and 'alpha2' query parameters appended to the API URL. The full list of fields/attributes available for each country is in the [ATTRIBUTES.md][attributes] file.

The main API endpoint is:

> https://iso3166-2-api.vercel.app/api

The other endpoints available in the API are:
* https://iso3166-2-api.vercel.app/api/all
* https://iso3166-2-api.vercel.app/api/alpha2/<input_alpha2>
* https://iso3166-2-api.vercel.app/api/name/<input_name>

Get All ISO 3166-2 updates for all countries
-------------------------------------------
### Request
`GET /`

    curl -i https://iso3166-2-api.vercel.app/api/all

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:29:39 GMT
    server: Google Frontend
    content-length: 202273

    {"AD":..., "AE":...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api/all"

all_request = requests.get(base_url)
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = await fetch('https://iso3166-2-api.vercel.app/api/all')
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```

Get all country and ISO 3166-2 data for a specific country e.g France, Germany, Hondurus, using alpha-2 code
------------------------------------------------------------------------------------------------------------

### Request
`GET /alpha2/FR`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=FR
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/FR

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:30:27 GMT
    server: Google Frontend
    content-length: 4513

    {"FR":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /alpha2/DE`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=DE
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/DE

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:19 GMT
    server: Google Frontend
    content-length: 10

    {"DE":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /alpha2/HN`

    curl -i https://iso3166-2-api.vercel.app/api?alpha2=HN
    curl -i https://iso3166-2-api.vercel.app/api/alpha2/HN

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:31:53 GMT
    server: Google Frontend
    content-length: 479

    {"HN":[{"altSpellings":"", "area": "", "borders": ""...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api"

all_request = requests.get(base_url, params={"alpha2": "FR"})
# all_request = requests.get(base_url, params={"alpha2": "DE"})
# all_request = requests.get(base_url, params={"alpha2": "HN"})
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch('https://iso3166-2-api.vercel.app/api?' + 
        new URLSearchParams({
            alpha2: 'FR'
  }));
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```
Get all country and ISO 3166-2 data for a specific country, using country name, e.g. Tajikistan, Seychelles, Uganda
-------------------------------------------------------------------------------------------------------------------

### Request
`GET /name/Tajikistan`

    curl -i https://iso3166-2-api.vercel.app/api?name=Tajikistan
    curl -i https://iso3166-2-api.vercel.app/api/name/Tajikistan

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:40:19 GMT
    server: Google Frontend
    content-length: 10

    {"TJ":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /name/Seychelles`

    curl -i https://iso3166-2-api.vercel.app/api?name=Seychelles
    curl -i https://iso3166-2-api.vercel.app/api/name/Seychelles

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 20 Dec 2022 17:41:53 GMT
    server: Google Frontend
    content-length: 479

    {"SC":[{"altSpellings":"", "area": "", "borders": ""...}

### Request
`GET /name/Uganda`

    curl -i https://iso3166-2-api.vercel.app/api?name=Ugandda
    curl -i https://iso3166-2-api.vercel.app/api/name/Uganda

### Response
    HTTP/2 200 
    content-type: application/json
    date: Tue, 21 Dec 2022 19:43:19 GMT
    server: Google Frontend
    content-length: 10

    {"UG":[{"altSpellings":"", "area": "", "borders": ""...}

### Python
```python
import requests

base_url = "https://iso3166-2-api.vercel.app/api"

all_request = requests.get(base_url, params={"name": "Tajikistan"})
# all_request = requests.get(base_url, params={"name": "Seychelles"})
# all_request = requests.get(base_url, params={"name": "Uganda"})
all_request.json() 
```

### Javascript
```javascript
function getData() {
  const response = 
    await fetch('https://iso3166-2-api.vercel.app/api?' + 
        new URLSearchParams({
            name: 'Tajikistan'
  }));
  const data = await response.json()
}

// Begin accessing JSON data here
var data = JSON.parse(this.response)
```