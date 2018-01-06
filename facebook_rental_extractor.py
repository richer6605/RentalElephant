import requests

def getAppAccessToken(app_id, app_secret):
    url = (
           "https://graph.facebook.com/v2.11/oauth/access_token" +
           "?client_id={}&client_secret={}".format(app_id, app_secret) +
           "&grant_type=client_credentials"
          )
    headers = {
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    token = res.json()['access_token']
    return token

def getAllGroupFeeds(group_id, access_token, since):
    url = (
           "https://graph.facebook.com/v2.11/{}".format(group_id) +
           "/feed?access_token={}".format(access_token) +
           "&since={}".format(since)
          )
    headers = {
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    res_json = res.json()
    feeds = []
    while "paging" in res_json:
        url = res_json['paging']['next']
        feed = res_json['data']
        feeds.extend(feed)
        res = requests.get(url, headers=headers)
        res_json = res.json()
    return feeds

def rentTypeFilter(feeds):
    feeds_filtered = {
        "rent-out": [],
        "rent": [],
        "sublet": []
    }
    for feed in feeds:
        message = feed['message']
        message_bytes = message.encode('utf-8')
        if (
            b'\xe6\xb1\x82\xe7\xa7\x9f' in message_bytes or
            b'\xe9\xa0\x90\xe7\xae\x97' in message_bytes
           ):
            feeds_filtered['rent'].append(feed)
        elif b'\xe8\xbd\x89\xe7\xa7\x9f' in message_bytes:
            feeds_filtered['sublet'].append(feed)
        else:
            feeds_filtered['rent-out'].append(feed)
    return feeds_filtered
