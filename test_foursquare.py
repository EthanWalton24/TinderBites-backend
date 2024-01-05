import requests, json, os
from dotenv import load_dotenv

load_dotenv()

#api parameters
category = 13065 #restaurants
key = os.getenv('FOURSQUARE_API_KEY')
limit = 50
lat = os.getenv('LAT')
lon = os.getenv('LONG')
radius = 16093
fields = [
    'fsq_id',
    'name',
    'geocodes',
    'location',
    'distance',
    'description',
    'tel',
    'hours',
    'rating',
    'price',
    'menu',
    'tips',
    'photos'
]
photo_size = '400x400'


url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius={radius}&categories={category}&limit={limit}&fields={','.join(fields)}&sort=DISTANCE"
headers = {"accept": "application/json", "Authorization": key}

#get places data from api
req = requests.get(url, headers=headers)
res = json.loads(req.content)['results']

#remove duplicate restaurants (multiple McDonald's etc.)
data = []
for place in res:
    if not any([place['name'] == d['name'] for d in data]):
        data.append(place)

[print(place['name']) for place in data]

# place_id = res[0]['fsq_id']
# print(place_id)

# req = requests.get(f"https://api.foursquare.com/v3/places/{place_id}/tips", headers=headers)
# res = json.loads(req.content)
# print(res)
# print(len(res))