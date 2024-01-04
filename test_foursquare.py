import requests, json, os
from dotenv import load_dotenv

load_dotenv()

#api parameters
category = 13065 #restaurants
key = os.getenv('FOURSQUARE_API_KEY')
limit = 2
lat = os.getenv('LAT')
lon = os.getenv('LONG')
radius = 16093
fields = [
    'fsq_id',
    'name',
    'location',
    'distance',
    'description',
    'tel',
    'hours',
    'rating',
    'price',
    'menu',
    'photos'
]
photo_size = '400x400'


url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius={radius}&categories={category}&limit={limit}&fields={','.join(fields)}"
headers = {"accept": "application/json", "Authorization": key}

#get places data from api
req = requests.get(url, headers=headers)
res = json.loads(req.content)['results']
