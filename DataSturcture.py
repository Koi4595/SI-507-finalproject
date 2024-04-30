import flickrapi
import json
import requests

api_key = ''
api_secret = ''
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

keywords = ['food', 'recipe', 'cooking', 'cuisine','yogurt'
            'breakfast', 'dinner', 'lunch', 'meal', 'restaurant',
            'pizza', 'sushi', 'steak', 'salad', 'burger', 'pasta', 'tacos',
            'grilled', 'roasted', 'fried', 'baked', 'stir-fried', 'steamed',
            'coffee', 'tea', 'juice', 'cocktail', 'smoothie', 'milkshake',
            'crispy', 'spicy', 'sweet', 'savory', 'creamy', 'crunchy',
            'vegan', 'keto', 'gluten-free', 'organic', 'healthy', 'gourmet',
            'brunch', 'picnic', 'barbecue', 'dinner party', 'buffet', 'potluck']

def get_region(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    response = requests.get(url).json()
    if 'address' in response:
        if 'country' in response['address']:
            return response['address']['country']
    return 'Unknown'

comments_data = []
photo_data = []

for keyword in keywords:
    photos = flickr.photos.search(text=keyword, per_page=50)
    for photo in photos['photos']['photo']:
        photo_id = photo['id']
        photo_title = photo['title']
        photo_description = flickr.photos.getInfo(photo_id=photo_id)['photo']['description']['_content']

        try:
            location = flickr.photos.geo.getLocation(photo_id=photo_id)
            lat = location['photo']['location']['latitude']
            lon = location['photo']['location']['longitude']
            region = get_region(lat, lon)
        except flickrapi.exceptions.FlickrError:
            region = 'Unknown'

        photo_info = {
            'photo_id': photo_id,
            'photo_title': photo_title,
            'description': photo_description,
            'region': region
        }
        photo_data.append(photo_info)

with open('food_photo_descriptions.json', 'w') as file:
    json.dump(photo_data, file, indent=4)

print("Photo data saved to food_photo_descriptions.json")
