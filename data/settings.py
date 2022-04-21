from data.config import API_TOKEN


headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': API_TOKEN
}

url = "https://hotels4.p.rapidapi.com/locations/search"

querystring_pattern = {
    "destinationId": "",
    "pageNumber": "1",
    "pageSize": "25",
    "checkIn": "",
    "checkOut": "",
    "adults1": "1",
    "priceMin": "",
    "priceMax": "",
    "sortOrder": "",
    "currency": "USD"
}

