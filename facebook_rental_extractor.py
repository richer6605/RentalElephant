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

def firstFilter():
