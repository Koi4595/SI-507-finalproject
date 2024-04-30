SI507 Final project: Social media food Explorer
*Author: Zhongrui Ning*, SI507 WN 2024
This is a project aims to explore and identify current food trends by analyzing food-related content on reddit/Flickr. 
By integrating publicly available food posts and comments from reddit/Flickr api, build a graphical structure that shows the attitudes and preferences of people on socialmedia (Flickr) towards food. 

Data source:
Flickr Api: - [Flickrapi]（https://www.flickr.com/services/developer/api/）
I put my api and password in my Datastructure code for ease of reproduction
Flickr's API can be requested through their developer platform very quickly, and once you've passed their online app review, you can see your API and password directly on the Flickr platform.

Data format：
All the data through the Flickr API real-time crawling, through the introduction of Python in the Flickr package to achieve (detailed code see Datastructure.py) and through the json package will crawl the Cache stored in the local JSON file, named food_photo_description.json, and then Clean.py to clean the crawled JSON data (remove /www and other information that may interfere with the judgment), named cleaned_food_descriptio.json, this file is the data source we use in the application.

Summary of data: 
This dataset is the information uploaded and shared by users through Flickr real-time crawling, in crawling by introducing the keywords related to food (e.g., food, meal, dinner, etc.), to retrieve the latest information of the platform, and for each keyword, we select the relevant 50 pieces of information on each page as the data source, which includes the variables of photo_id, photo_title ,photo_title, photo_description, and the Region information calculated by the latitude and longitude information.
