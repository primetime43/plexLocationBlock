import json
import logging
import urllib.request
import os
from datetime import datetime

# can not have the same location in both arrays
locationsToBlock = ["Florida", "Pennsylvania", "Los Angeles", "Houston"]
locationsToAllow = ["New York"]
usersToAllow = ['test1', 'userNameEx']  # used to override locations

curStreamsDic = {}

# environment variables
TAUTULLI_URL = ''
TAUTULLI_APIKEY = ''
TAUTULLI_URL = os.getenv('TAUTULLI_URL', TAUTULLI_URL)
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY', TAUTULLI_APIKEY)


def getActivity():
    curStreamsDic.clear()  # clear stream array
    endPoint = TAUTULLI_URL + '/api/v2?apikey='+TAUTULLI_APIKEY+'&cmd=get_activity'

    response = urllib.request.urlopen(endPoint)
    data = json.loads(response.read())

    # loop for the number of current sessions
    for stream in range(len(data['response']['data']['sessions'])):
        curStreamsDic[stream] = data['response']['data']['sessions'][stream]
        #print("\n" + json.dumps(data['response']['data']['sessions'][stream], indent=2))
        #print("\n--------------- Stream %s above ---------------" % (stream))

    # loop through all of the streams in the dict created in the loop above
    for index in range(len(curStreamsDic)):
        #print("\n" + curStreamsDic[index]['user'])
        #print("\n" + curStreamsDic[index]['machine_id'])
        #print("\n" + curStreamsDic[index]['ip_address_public'])
        #print("\n" + curStreamsDic[index]['session_key'])
        #print("\n" + curStreamsDic[index]['session_id'])
        #print("\n" + curStreamsDic[index]['location'])
        getLocationInfo(ipAddress=curStreamsDic[index]['ip_address_public'], streamIndex=index, user=curStreamsDic[index]
                        ['user'], sessionKey=curStreamsDic[index]['session_key'], sessionID=curStreamsDic[index]['session_id'])
        # print("\n------------------------------------------------------------------------------")


def getLocationInfo(**kwargs):
    geoLocation = TAUTULLI_URL+'/api/v2?apikey='+TAUTULLI_APIKEY + \
        '&cmd=get_geoip_lookup&ip_address=' + kwargs.get('ipAddress')
    user = kwargs.get('user')

    response = urllib.request.urlopen(geoLocation)
    locationData = json.loads(response.read())
    # print("\n------------------------------------------------------------------------------")
    print("\n" + kwargs.get('user') + " Location Data Below")
    print("\n" + locationData['response']['data']['city'] + " " + locationData['response']['data']['postal_code'] +
          ", " + locationData['response']['data']['region'] + ", " + locationData['response']['data']['country'])
    print("\n" + json.dumps(locationData, indent=2))
    print("\n" + "--------------- %s Location Data Above ---------------" % user)

    location = locationData['response']['data']['region']
    cityLocation = locationData['response']['data']['city']
    # the location is not in the allowed list and is present in the blocked list and user isn't in allowed list
    if location not in locationsToAllow and cityLocation not in locationsToAllow and location in locationsToBlock or cityLocation in locationsToBlock and user not in usersToAllow:
        #logFileStream.write("\n" + location + " not in allowed locations and is present in locations to block! user: " + user)
        print("\n" + location +
              " not in allowed locations and is present in locations to block! user: " + user)
        urllib.request.urlopen(TAUTULLI_URL+'/api/v2?apikey='+TAUTULLI_APIKEY +
                               '&cmd=terminate_session&session_key='+kwargs.get('sessionKey')+'&session_id='+kwargs.get('sessionID'))
    else:
        #logFileStream.write("\n" + user + " is allowed at the current location of " + location)
        print("\n" + user + " is allowed at the current location of " +
              cityLocation + ", " + location)


def timeStamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time


getActivity()
print("\nLog End: " + timeStamp())