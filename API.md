# ISO3166-2 API

Two query string parameters are available in the API - `alpha2` and `name`. The 2 letter alpha-2 country code can be appeneded to the url as a query string parameter to the main endpoint - "?alpha2=JP" - or added to the alpha2 endpoint - "/alpha2/JP". A single alpha-2 or list of them can be passed to the API (e.g "FR", "DE", "HU, ID, MA"). The name parameter can be a country name in english as it is most commonly known. The name can similarly be added as a query string parameter to the main endpoint - "?name="Denmark" - or added to the name endpoint - "/name/Denmark". A closeness function is utilised so the most approximate name from the input will be used e.g Sweden will be used if "?name=Swede". 

The API documentation and usage with all useful commands and examples to the API is available on the [API.md](https://github.com/amckenna41/iso3166-2-api/API.md) file. The full list of attributes/fields available in `iso3166-2` can be viewed in the [ATTRIBUTES.md][attributes] file.

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

Get all country and ISO 3166-2 data for a specific country, using its 2 letter alpha-2 code e.g FR, DE, HN
----------------------------------------------------------------------------------------------------------

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

[attributes]: https://github.com/amckenna41/iso3166-2-api/ATTRIBUTES.md 