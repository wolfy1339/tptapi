import requests
import six
import hashlib
from . import errors

def md5(data):
    return hashlib.md5().update(bytes(data)).hexdigest()

class Client(object):
    def __init__(self):
       self.base_url = "http://powdertoy.co.uk"

    def _get(self, url, params=None):
        headers = {
            "X-Auth-User-Id": 0,
            "X-Auth-Session-Key": 0
        }
        if hasattr(self, 'loginData'):
            headers["X-Auth-User-Id"] = self.loginData["UserID"]
            headers["X-Auth-Session-Key"] = self.loginData["SessionKey"]
        return requests.get(url, params=params, headers=headers)

    def _post(self, url, params=None, data=None):
        headers = {
            "X-Auth-User-Id": 0,
            "X-Auth-Session-Key": 0
        }
        if hasattr(self, 'loginData'):
            headers["X-Auth-User-Id"] = self.loginData["UserID"]
            headers["X-Auth-Session-Key"] = self.loginData["SessionKey"]
        return requests.post(url, params=params, data=data, headers=headers)

    def login(self, user, password):
        form = {
            "Username": user,
            "Hash": md5("{0}-{1}".format(user, md5(password)))
        }
        r = self._post(self.opts["url"] + "Login.json", data=form)
        if r.status_code == requests.codes.ok:
            self.loginData = j = r.json()
            if len(j["Notifications"]):
                six.print_("User has a new notifications: "+", ".join(j["Notifications"]))
            del self.loginData["Status"]
            del self.loginData["Notifications"]
        else:
            raise errors.InvalidLogin()
        return r.status_code == requests.codes.ok

    def checkLogin(self):
        r = self._get(self.base_url + "/Login.json").json()
        return r["Status"] == 1

    def vote(self, ID, action):
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Action": "Up" if action > 0 else "Down"
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def comment(self, ID, content):
        form = {
            "Comment": content
        }
        qs = {"ID": ID}
        r = self._post(self.base_url + "/Browse/Comments.json", data=form, params=qs)
        return r.status_code == requests.codes.ok

    def addTag(self, ID, tag):
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "add",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status_code == requests.codes.ok

    def delTag(self, ID, tag):
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "delete",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status

    def delSave(self, ID):
        qs = {
            "ID": ID,
            "Mode": "Delete",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def unpublishSave(self, ID):
        qs = {
            "ID": ID,
            "Mode": "Unpublish",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def publishSave(self, ID, content):
        form = {
            "ActionPublish": 1
        }
        qs = {
            "ID": ID,
            "Key": self.loginData.SessionKey
        }
        r = self._post(self.base_url + "/Browse/View.json", data=form, params=qs)
        return r.text() == "1"

    def setProfile(self, p):
        # action can be -1 or +1
        r = self._post(self.base_url + "/Profile.json", data=p)
        return r.text() == "OK"

    def browse(self, query, count,start):
        qs = {
            Start: start,
            Count: count,
            Search_Query: query
        }
        r = self._get(self.base_url + "/Browse.json", params=qs)
        return r.json()

    def listTags(self, c, s):
        qs = {
            Start: s,
            Count: c
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.json()["Tags"]

    def fav(self, ID):
        qs = {
            "ID": ID,
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Favourite.json", params=qs)
        return r.status_code == requests.codes.ok

    def remfav(self, ID):
        qs = {
              "ID": ID,
              "Key": self.loginData.SessionKey,
              "Mode": "Remove"
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.status_code == requests.codes.ok

    def save(self, name, desc, data):
        # action can be -1 or +1
        form = {
            "Name": name,
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Save.api", data=form)
        if r.text().split(" ")[0] == "OK":
            return r.text().split(" ")[1]

    def updateSave(self, ID, data, desc):
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def saveData(self, ID):
        qs = {"ID": ID}
        r = self._get(self.base_url + "/Browse/View.json", params=qs)
        return r.json()

    def startup(self):
        return self._get(self.base_url + "/Startup.json").json()

    def comments(self, ID, count, start):
        qs = {
            "Start": start,
            "Count": count,
            "ID": ID
        }
        r = self._get(self.base_url + "/Browse/Comments.json", params=qs)
        return r.json()
