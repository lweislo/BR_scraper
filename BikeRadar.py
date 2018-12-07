import requests
import os
import html5lib
import urllib
import time
from bs4 import BeautifulSoup
#import re
# -*- coding: utf-8 -*-
#This script extracts image gallery files
#filenames and caption, and image credit data from a BikeRadar article

#First ask the user for the URL
try:
    start_url = input("Enter URL (with http...): ")
#get the page
    page = requests.get(start_url)
#add some logic here to sort out bad links

    if "bikeradar" not in start_url:
        print("That isn't a BikeRadar link, so this will not work...")
        exit(0)
    #did the file download OK?
    status = page.status_code
    if status == 200:
        print("Success!")
    else:
        print("Something went wrong with that download!")
        exit(0)
#Get the HTML from the page and parse with BeautifulSoup
    content = page.content
    soup = BeautifulSoup(content, "html5lib")


#get a time stamp for the files we create
    timestr = time.strftime("%Y%m%d-%H%M%S.txt")
#Create a file for the captions.
    cap_file = "captions_" + timestr
    print("Creating a new captions file named: ", cap_file)
#Grab the caption credits in a separate file.

    my_credits = soup.find_all(class_="gallery-credit")
    cred_file = "credits_" + timestr
    print("Creating a new credits file named: ", cred_file)
except:
    if "http" not in start_url:
        print("That is not a valid URL, you need to include http://")
    else:
        print("Goodbye!")
        exit(0)
#Count the number of images, and prompt to continue

my_items = soup.find_all(class_="gallery-item-image")
print("There are:", len(my_items), "items in the gallery")
choice = input("Do you wish to proceed with the download? (Y/N): ")
choice = choice.upper()
if "Y" not in choice:
    print("Quitting! Goodbye")
    exit(0)

for div in soup.find_all(class_="gallery-credit"):
    with open(cred_file, 'a') as credits_file:
        credits_file.write(f"{div.text}\n")
#Iterate over the list of gallery items, get the filename, caption
# and download each image to the current directory

for div in soup.find(class_="gallery-thumbnails"):
    for img in div.find_all('img', alt=True):
        image_link = img['data-full-src'].replace('-630-80.jpg', '-1440-810.jpg')
        trim_image = image_link.split("/")[-1]
        #replace dashes and spaces in image names with underscores like the CN CMS will.
        trim_image = trim_image.replace("-","_")
        trim_image = trim_image.replace(" ","_")
        #The standard gallery image is too small, grabbing the bigger one,
        #also, when writing a captions file only take the file name not URL
        caption = img['alt']
        with open(cap_file, 'a') as caption_file:
            caption_file.write(f"{trim_image}\t {caption}\n")
        #Finally, download the actual image file
        print("Downloading images, this might take a while, be patient.")
        urllib.request.urlretrieve(image_link, os.path.basename(image_link))

caption_file.close()
credits_file.close()
