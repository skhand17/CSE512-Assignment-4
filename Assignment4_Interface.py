#
# Assignment4 Interface
# Name: Shreyansh Khandelwal
#
from pymongo import MongoClient
import os
import sys
import json
import itertools
import math
def FindBusinessBasedOnCity(cityToSearch, minReviewCount, saveLocation1, collection):

    mydoc = collection.find({"city" : cityToSearch,
                 "review_count" : {"$gte" : minReviewCount}},{"city": 1,"full_address" : 1,
                                                         "state": 1, "name": 1, "stars" : 1, "_id": 0})
    full_address = []
    city = []
    state = []
    name = []
    stars = []
    star_strings = []
    for x in mydoc:
        state.append(x['state'])
        full_address.append(x['full_address'])
        name.append(x['name'])
        stars.append(x['stars'])
        city.append(x['city'])

    for elements in stars:
        star_strings.append(str(elements))

    with open(saveLocation1, 'w') as fp:
        for (n,f,c,st,sta) in zip(name,full_address,city,state,star_strings):
            fp.write(n+'$'+f+'$'+c+'$'+st+'$'+sta+'\n')
    print("Done writing to a file")

def calculateDistance(myLocation, longitude, latitude):
    R = 3959
    d = []
    for (i,j) in zip(longitude,latitude):
        ph1 = math.radians(myLocation[0])
        ph2 = math.radians(j)
        delta = math.radians(j - myLocation[0])
        lambdas = math.radians(i - myLocation[1])
        a = math.sin(delta/2) * math.sin(delta/2) + math.cos(ph1)\
            * math.cos(ph2) * math.sin(lambdas/2) * math.sin(lambdas/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist = R * c
        d.append(dist)

    return d;

def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, minDistance, maxDistance, saveLocation2, collection):
    longitude = []
    latitude  = []
    businessName = []
    distanceList = []
    businessNameList = []
    mydoc = collection.find({"categories" : {"$in" : categoriesToSearch}})
    for x in mydoc:
        longitude.append(x['longitude'])
        latitude.append(x['latitude'])
        businessName.append(x['name'])


    myLocationFloat = [float(i) for i in myLocation]
    distanceList =  calculateDistance(myLocationFloat,longitude,latitude)
    count = 0
    for (bus,distlist) in zip(businessName,distanceList):
        if distlist >= minDistance and distlist <=maxDistance:
            businessNameList.append(bus)
            count = count + 1

    print(count)

    with open(saveLocation2, 'w') as fp:
        for b in businessNameList:
            fp.write(b+'\n')
        print("Done writing to 2nd file")




