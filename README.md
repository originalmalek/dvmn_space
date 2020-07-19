# dvmn_space
Download photos from hubble api and spaceX api. Upload the photo to instagram use instabot


# Description
The code: 
1. Download photos from hubble collection and from lastest SpaceX launch by API
2. Post the photos to instagram.

The project use:  
[Instagram](https://instagram.com)  
[SpaceX API](https://github.com/r-spacex/SpaceX-API)  
[Hubble telescope API](http://hubblesite.org/api/documentation)  


# Requirements
Python >=3.7

Create file '.env' and add the code
```
USERNAME_INSTA = your_instagram_login
PASS_INSTA = your_instagram_password
```

Modules:  
'requests 2.24.0'   
'python-dotenv 0.14.0'  
'instabot 0.117.0'  

For installing the modules use command
```
pip install -r requirements.txt	
```


# How to use

Install requirements  
Open and run 'main.py'
```
python main.py	
```


# Additional information
For downloading another collection from hubble change variable 'collection_name' in get_ids_hubble_collections() function   
Existing collections: "holiday_cards", "wallpaper", "spacecraft", "news", "printshop", "stsci_gallery"

# Project goal

The code was written for educational purpose on online course for Api developers dvmn.org

