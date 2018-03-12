
# I configured the URL based on https://api.nasa.gov/api.html#Images.

import urllib.request
import time
import requests
import json
from urllib.request import urlopen
from pprint import pprint
import csv

# specify the URL of NASA
nasa_url = "https://images-api.nasa.gov/search?q=ilan%20ramon&media_type=image"



def get_images():
    myID = []
    url_array=[]
    url_array=set_url_array()
    count=set_count()
    for i in range(len(url_array)):
        my_json = urlopen(url_array[i])
        string = my_json.read().decode('utf-8')
        data = json.loads(string)
        if count < 100:
            range1=count
        else:
            range1=100
            count=count-100
        for num in range(range1):
            myID.append(data['collection']['items'][num]['data'][0]['nasa_id'])
    return myID

def set_count():
    count=0
    my_json = urlopen(nasa_url)
    string = my_json.read().decode('utf-8')
    data = json.loads(string)
    return (data['collection']['metadata']['total_hits'])

def set_url_array():
    myURL = []
    my_json = ""
    nasa_url_next = "NULL"
    nasa_url_next = nasa_url
    while (nasa_url_next != "NULL"):
        myURL.append(nasa_url_next)
        my_json = urlopen(nasa_url_next)
        string = my_json.read().decode('utf-8')
        data = json.loads(string)
        nasa_url_next = "NULL"
        temp = len(data['collection']['links'])
        for n in range(temp):
            if data['collection']['links'][n]['prompt'] == "Next":
                nasa_url_next = data['collection']['links'][n]['href']
    return myURL

def set_limit(my_arr,lim):
    empty_arr=[]
    for i in range(len(my_arr)):
        size=get_size(my_arr[i])
        if float(size)>float(lim):
            result_str=my_arr[i]+","+str(size)
            pprint (result_str)
            empty_arr.append(result_str)
    pprint (empty_arr)
    with open('result.csv', 'w') as myfile:
        #wr = csv.writer(myfile, delimiter=',',quoting=csv.QUOTE_ALL)
        wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)

        wr.writerow(empty_arr)

def get_size(key):
    url="https://images-assets.nasa.gov/image/" + key + "/metadata.json"
    my_json = urlopen(url)
    string = my_json.read().decode('utf-8')
    data = json.loads(string)
    if 'File:FileSize' in data:
        size = data['File:FileSize']
        size = size.lower()
        size_arr=size.split()
        if size_arr[1] == "mb":
            size_arr[0]=float(float(size_arr[0])*1000)
        return size_arr[0]
    else:
        return 100000



'''
 

#KSC-02pp0490
https://images-assets.nasa.gov/image/KSC-02pp0490/metadata.json
#https://images-assets.nasa.gov/image/{nasa_id}/metadata.json
#File:FileSize: "2 MB" , "1695 KB"
'''
if __name__ == "__main__":
    images_array=[]
    # getting all the nasa_id for images of Ilan Ramon
    images_array = get_images()
    set_limit(images_array,1000)


