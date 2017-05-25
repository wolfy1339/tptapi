import requests
import six
import hashlib
from . import errors

def md5(data):
    return hashlib.md5().update(bytes(data)).hexdigest()

class Client(object):
    def __init__(self):
       self.base_url = "http://powdertoy.co.uk"

    def _get(url, params=None):
        headers = {
            "X-Auth-User-Id": 0,
            "X-Auth-Session-Key": 0
        }
        if hasattr(self, 'loginData'):
            headers["X-Auth-User-Id"] = self.loginData["UserID"]
            headers["X-Auth-Session-Key"] = self.loginData["SessionKey"]
        return requests.get(url, params=params, headers=headers)

    def _post(url, params=None, data=None):
        headers = {
            "X-Auth-User-Id": 0,
            "X-Auth-Session-Key": 0
        }
        if hasattr(self, 'loginData'):
            headers["X-Auth-User-Id"] = self.loginData["UserID"]
            headers["X-Auth-Session-Key"] = self.loginData["SessionKey"]
        return requests.post(url, params=params, data=data, headers=headers)

    def login(self, user, password){
        hash = md5("{0}-{1}".format(user, md5(password)))
        form = {
            "Username": user,
            "Hash": hash
        }
        r = self._post(self.opts["url"] + "Login.json", data=form)
        if r.status_code == requests.codes.ok:
            self.loginData = r.json()
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

    def vote(self, id, type):
        # type can be -1 or +1
        form = {
            "ID": Number(id),
            "Action": (type>0):"Up":"Down"
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def comment(self, id, content) {
        form = {
            "Comment": content
        }
        qs = {"ID": id}
        r = self._post(self.base_url + "/Vote.api", data=form, params=qs)
        return r.status

    def addTag(self, id, tag){
        qs = {
            "ID": id,
            "Tag": tag,
            "Op": "add",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status

    def delTag(self, id, tag):
        qs = {
            "ID": id,
            "Tag": tag,
            "Op": "delete",
            "Key": self.loginData.SessionKey
       }
       r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
       return r.status

    def delSave(self, id):
        qs = {
            "ID": id,
            "Mode": "Delete",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status

    def unpublishSave(self, id):
        qs = {
            "ID": id,
            "Mode": "Unpublish",
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status

    def publishSave(self, id, content):
        form = {
            "ActionPublish": 1
        }
        qs = {
            "ID": id,
            "Key": self.loginData.SessionKey
        }
        r = self._post(self.base_url + "/Browse/View.json", data=form, params=qs)
        return r.text() == "1"

    def setProfile(self, p):
        # type can be -1 or +1
        r = self._post(self.base_url + "/Profile.json", data=p)
        return r.text() == "OK"

    def browse(self, query, count,start):
        qs = {
            Start: start,
            Count: count,
            Search_Query: query
        }
        r = self._get(self.base_url + "/Browse.json", params=qs)
        return r

    def listTags(self, c, s){
        qs = {
            Start: s,
            Count: c
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return rp(o)

    def fav(self, id){
        qs = {
            "ID": id,
            "Key": self.loginData.SessionKey
        }
        r = self._get(self.base_url + "/Browse/Favourite.json", params=qs)
        return r.status

    def remfav(self, id){
        qs = {
              "ID": id,
              "Key": self.loginData.SessionKey,
              "Mode": "Remove"
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.status

    def save(self, name, desc, data):
        # type can be -1 or +1
        form = {
            "Name": name,
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Save.api", data=form)
        if r.text().split(" ")[0] == "OK":
            return r.text().split(" ")[1]

    def updateSave(self, id, data, desc):
        # type can be -1 or +1
        form = {
            "ID": Number(id),
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def saveData(self, id) {
        qs = {"ID":id}
        r = self._get(self.base_url + "/Browse/View.json", params=qs)
        return rp(o)

    def startup(self){
        return self._get(self.base_url + "/Startup.json").json()

    def comments(self, id, count, start):
        qs = {
            "Start": start,
            "Count": count,
            "ID": id
        }
        r = self._get(self.base_url + "/Browse/Comments.json", params=qs)
        return rp(o)
