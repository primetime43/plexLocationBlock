import json, logging, urllib.request, os
from datetime import datetime

curStreamsDic = {}
#use logFileStream to stream when running on the desktop
#logFileStream = open(os.getcwd()+'\\plexLocationBlockLogging.txt',"a+") 

#get the apikey value from settings>web interface>bottom of the page
#apiKeyVal = ' '

#environment variables
TAUTULLI_URL = ''
TAUTULLI_APIKEY = ''
TAUTULLI_URL = os.getenv('TAUTULLI_URL', TAUTULLI_URL)
TAUTULLI_APIKEY = os.getenv('TAUTULLI_APIKEY', TAUTULLI_APIKEY)

def getActivity():
    curStreamsDic.clear()  # clear stream array
    endPoint = TAUTULLI_URL + '/api/v2?apikey='+TAUTULLI_APIKEY+'&cmd=get_activity'

    #logFileStream.write("Log Begin: " + timeStamp())
    response = urllib.request.urlopen(endPoint)
    data = json.loads(response.read())

    # loop for the number of current sessions
    for stream in range(len(data['response']['data']['sessions'])):
        curStreamsDic[stream] = data['response']['data']['sessions'][stream]
        #logFileStream.write("\n" + json.dumps(data['response']['data']['sessions'][stream], indent=2))
        #logFileStream.write("\n--------------- Stream %s above ---------------" % (stream))
        print("\n" + json.dumps(data['response']['data']['sessions'][stream], indent=2))
        print("\n--------------- Stream %s above ---------------" % (stream))

    #loop through all of the streams in the dict created in the loop above
    for index in range(len(curStreamsDic)):
        #logFileStream.write("\n" + curStreamsDic[index]['user'])
        #logFileStream.write("\n" + curStreamsDic[index]['machine_id'])
        #logFileStream.write("\n" + curStreamsDic[index]['ip_address_public'])
        #logFileStream.write("\n" + curStreamsDic[index]['session_key'])
        #logFileStream.write("\n" + curStreamsDic[index]['session_id'])
        #logFileStream.write("\n" + curStreamsDic[index]['location'])
        print("\n" + curStreamsDic[index]['user'])
        print("\n" + curStreamsDic[index]['machine_id'])
        print("\n" + curStreamsDic[index]['ip_address_public'])
        print("\n" + curStreamsDic[index]['session_key'])
        print("\n" + curStreamsDic[index]['session_id'])
        print("\n" + curStreamsDic[index]['location'])
        getLocationInfo(ipAddress=curStreamsDic[index]['ip_address_public'], streamIndex=index, user = curStreamsDic[index]['user'], sessionKey=curStreamsDic[index]['session_key'], sessionID=curStreamsDic[index]['session_id'])
        #logFileStream.write("\n------------------------------------------------------------------------------")
        print("\n------------------------------------------------------------------------------")

def getLocationInfo(**kwargs):
    geoLocation = TAUTULLI_URL+'/api/v2?apikey='+TAUTULLI_APIKEY+'&cmd=get_geoip_lookup&ip_address=' + kwargs.get('ipAddress')
    user = kwargs.get('user')

    # can not have the same location in both arrays
    locationsToBlock = ["Florida", "Pennsylvania"]
    locationsToAllow = ["New York"]
    usersToAllow = ['test1', 'userNameEx']  # used to override locations
    response = urllib.request.urlopen(geoLocation)
    locationData = json.loads(response.read())
    #logFileStream.write("\n------------------------------------------------------------------------------")
    #logFileStream.write("\n" + kwargs.get('user') + " Location Data Below")
    #logFileStream.write("\n" + locationData['response']['data']['city'] + " " + locationData['response']['data']['postal_code'] + ", "  + locationData['response']['data']['region'] + ", " + locationData['response']['data']['country'])
    #logFileStream.write("\n" + json.dumps(locationData, indent=2))
    #logFileStream.write("\n" + "--------------- %s Location Data Above ---------------" % user)
    print("\n------------------------------------------------------------------------------")
    print("\n" + kwargs.get('user') + " Location Data Below")
    print("\n" + locationData['response']['data']['city'] + " " + locationData['response']['data']['postal_code'] + ", "  + locationData['response']['data']['region'] + ", " + locationData['response']['data']['country'])
    print("\n" + json.dumps(locationData, indent=2))
    print("\n" + "--------------- %s Location Data Above ---------------" % user)

    location = locationData['response']['data']['region']
    # the location is not in the allowed list and is present in the blocked list and user isn't in allowed list
    if location not in locationsToAllow and location in locationsToBlock and user not in usersToAllow:
        #logFileStream.write("\n" + location + " not in allowed locations and is present in locations to block! user: " + user)
        print("\n" + location + " not in allowed locations and is present in locations to block! user: " + user)
        urllib.request.urlopen(TAUTULLI_URL+'/api/v2?apikey='+TAUTULLI_APIKEY+'&cmd=terminate_session&session_key='+kwargs.get('sessionKey')+'&session_id='+kwargs.get('sessionID'))
    elif locationsToAllow or usersToAllow:
        #logFileStream.write("\n" + user + " is allowed at the current location of " + location)
        print("\n" + user + " is allowed at the current location of " + location)
        urllib.request.urlopen(TAUTULLI_URL+'/api/v2?apikey='+TAUTULLI_APIKEY+'&cmd=terminate_session&session_key='+kwargs.get('sessionKey')+'&session_id='+kwargs.get('sessionID'))

def timeStamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

getActivity()
print("\nLog End: " + timeStamp())
#logFileStream.write("\nLog End: " + timeStamp())
#logFileStream.close()