import json
import re

def clean_description(description):
    # remove html
    description = re.sub('<.*?>', '', description)
    # remove url
    description = re.sub('https?://\S+|www\.\S+', '', description)
    # remove special characters
    description = re.sub('[^a-zA-Z0-9\s]+', '', description)
    # remove extra blank
    description = re.sub('\s+', ' ', description).strip()
    return description

def clean_data(data):
    cleaned_data = []
    for item in data:
        if 'photo_id' in item and 'photo_title' in item and 'description' in item:
            cleaned_item = {
                'photo_id': item['photo_id'],
                'photo_title': item['photo_title'],
                'description': clean_description(item['description']),
                'region': item['region']
            }
            if cleaned_item['description']:  # 去除空描述
                cleaned_data.append(cleaned_item)
    return cleaned_data

with open('food_photo_descriptions.json', 'r') as file:
    raw_data = json.load(file)

cleaned_data = clean_data(raw_data)

with open('cleaned_food_photo_descriptions.json', 'w') as file:
    json.dump(cleaned_data, file, indent=4)

print("Data cleaning completed. Cleaned data saved to cleaned_food_photo_descriptions.json")