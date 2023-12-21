import requests, json, os
from dotenv import load_dotenv

load_dotenv()

headers = {
    'Content-Type': 'application/json',
    "X-Goog-Api-Key": os.getenv('GOOGLE_API_KEY'),
    "X-Goog-FieldMask": "places.id,places.displayName,places.location,places.googleMapsUri,places.rating,places.userRatingCount," \
    "places.internationalPhoneNumber,places.priceLevel,places.regularOpeningHours,places.reviews,places.photos,places.editorialSummary"
}

data = json.dumps({
    "includedTypes": ["restaurant"],
    "maxResultCount": 1,
    "locationRestriction": {
        "circle": {
        "center": {
            "latitude": os.getenv('LAT'),
            "longitude": os.getenv('LONG')},
        "radius": 16093.4
        }
    }
})

r = requests.post('https://places.googleapis.com/v1/places:searchNearby', data=data, headers=headers)

print(json.loads(r.content))

with open('out.json', 'w') as f:
    f.write(json.dumps(json.loads(r.content), indent=4))