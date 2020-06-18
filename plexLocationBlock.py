import json, logging, urllib.request, os
from datetime import datetime

curStreamsDic = {}
logFileStream = open(os.getcwd()+'\\plexLocationBlockLogging.txt',"a+") 

#get the apikey value from settings>web interface>bottom of the page
apiKeyVal = ' '

def getActivity():
    curStreamsDic.clear()  # clear stream array
    endPoint = 'http://localhost:8181/api/v2?apikey='+apiKeyVal+'&cmd=get_activity'

    logFileStream.write("Log Begin: " + timeStamp())
    response = urllib.request.urlopen(endPoint)
    data = json.loads(response.read())

    # loop for the number of current sessions
    for stream in range(len(data['response']['data']['sessions'])):
        curStreamsDic[stream] = data['response']['data']['sessions'][stream]
        logFileStream.write("\n" + json.dumps(data['response']['data']['sessions'][stream], indent=2))
        logFileStream.write("\n--------------- Stream %s above ---------------" % (stream))

    #loop through all of the streams in the dict created in the loop above
    for index in range(len(curStreamsDic)):
        logFileStream.write("\n" + curStreamsDic[index]['user'])
        logFileStream.write("\n" + curStreamsDic[index]['machine_id'])
        logFileStream.write("\n" + curStreamsDic[index]['ip_address_public'])
        logFileStream.write("\n" + curStreamsDic[index]['session_key'])
        logFileStream.write("\n" + curStreamsDic[index]['session_id'])
        logFileStream.write("\n" + curStreamsDic[index]['location'])
        getLocationInfo(ipAddress=curStreamsDic[index]['ip_address_public'], streamIndex=index, user = curStreamsDic[index]['user'], sessionKey=curStreamsDic[index]['session_key'], sessionID=curStreamsDic[index]['session_id'])
        logFileStream.write("\n------------------------------------------------------------------------------")

#http://localhost:8181/api/v2?apikey=67359240365f409eb5a5b5fef2ca0cbb&cmd=terminate_session&session_key=170&session_id=1e3d7d1c47c98259-com-plexapp-android
def getLocationInfo(**kwargs):
    geoLocation = 'http://localhost:8181/api/v2?apikey='+apiKeyVal+'&cmd=get_geoip_lookup&ip_address=' + kwargs.get('ipAddress')
    user = kwargs.get('user')

    # can not have the same location in both arrays
    locationsToBlock = ["Florida", "Pennsylvania"]
    locationsToAllow = ["New York"]
    usersToAllow = ['test1', 'userNameEx']  # used to override locations
    response = urllib.request.urlopen(geoLocation)
    locationData = json.loads(response.read())
    logFileStream.write("\n------------------------------------------------------------------------------")
    logFileStream.write("\n" + kwargs.get('user') + " Location Data Below")
    logFileStream.write("\n" + locationData['response']['data']['city'] + " " + locationData['response']['data']['postal_code'] + ", "  + locationData['response']['data']['region'] + ", " + locationData['response']['data']['country'])
    logFileStream.write("\n" + json.dumps(locationData, indent=2))
    logFileStream.write("\n" + "--------------- %s Location Data Above ---------------" % user)

    location = locationData['response']['data']['region']
    # the location is not in the allowed list and is present in the blocked list and user isn't in allowed list
    if location not in locationsToAllow and location in locationsToBlock and user not in usersToAllow:
        logFileStream.write("\n" + location + " not in allowed locations and is present in locations to block! user: " + user)
        urllib.request.urlopen('http://localhost:8181/api/v2?apikey='+apiKeyVal+'&cmd=terminate_session&session_key='+kwargs.get('sessionKey')+'&session_id='+kwargs.get('sessionID'))
    elif locationsToAllow or usersToAllow:
        logFileStream.write("\n" + user + " is allowed at the current location of " + location)
        urllib.request.urlopen('http://localhost:8181/api/v2?apikey='+apiKeyVal+'&cmd=terminate_session&session_key='+kwargs.get('sessionKey')+'&session_id='+kwargs.get('sessionID'))

def timeStamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

getActivity()
logFileStream.write("\nLog End: " + timeStamp())
logFileStream.close()