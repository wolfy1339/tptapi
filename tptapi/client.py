import requests
import six
import hashlib
from . import errors

def md5(d):
    if six.PY3:
        d = bytes(d)
    return haslib.md5().update(d).hexdigest()

class Client(object):
    def __init__(self)
       self.base_url = "http://powdertoy.co.uk/"
       self.session = requests.Session()

       def login(self, user, password){
            hash = md5("{0}-{1}".format(user, md5(password)))
            form = {
                'Username': user,
                'Hash': hash
            }
            r = self.session.post(self.opts['url'] + 'Login.json', data=form)
            if r.status_code == requests.codes.ok:
                 if(j.Status) {
                   self.loginData = j
                   if(j.Notifications.length > 0) {
                        six.print_("User has a new notifications: "+j.Notifications.join(", "))
                   }
                   delete(self.loginData.Status)
                   delete(self.loginData.Notifications)
            else:
                raise LoginError("Bad login.")

    def checkLogin(self){
        return rp(self.optionSkeleton("Login.json","GET")).then(a=>Boolean(a.Status))

    def vote(self, id, type):
        # type can be -1 or +1
        o = self.optionSkeleton("Vote.api","POST")
        o.form = {
            "ID": Number(id),
            "Action": (type>0):"Up":"Down"
       }
       o.json = false
       return rp(o).then(a=>(a=="OK"))

    def comment(self, id, content) {
        o = self.optionSkeleton("Browse/Comments.json","POST")
        o.form = {
            "Comment": content
        }
        o.qs = {"ID": id}
        return rp(o).then(a=>Boolean(a.Status))

    def addTag(self, id, tag){
        o = self.optionSkeleton("Browse/EditTag.json","GET")
        o.qs = {
            "ID": id,
            "Tag": tag,
            "Op": "add",
            "Key": self.loginData.SessionKey
        }
        return rp(o).then(a=>Boolean(a.Status))

    def delTag(self, id, tag):
       o = self.optionSkeleton("Browse/EditTag.json","GET")
        o.qs = {
            "ID": id,
            "Tag": tag,
            "Op": "delete",
            "Key": self.loginData.SessionKey
       }
       return rp(o).then(a=>Boolean(a.Status))

    def delSave(self, id):
        o = self.optionSkeleton("Browse/Delete.json","GET")
        o.qs = {
            "ID": id,
            "Mode": "Delete",
            "Key": self.loginData.SessionKey
       }
        return rp(o).then(a=>Boolean(a.Status))

    def unpublishSave(self, id):
        o = self.optionSkeleton("Browse/Delete.json","GET")
        o.qs = {
            "ID": id,
            "Mode": "Unpublish",
            "Key": self.loginData.SessionKey
        }
        return rp(o).then(a=>Boolean(a.Status))

    def publishSave(self, id, content):
        o = self.optionSkeleton("Browse/View.json","POST")
        o.form = {
            "ActionPublish": 1
        }
        o.qs = {
            "ID": id,
            "Key": self.loginData.SessionKey
        }
        return rp(o).then(a=>Boolean(1))

    def setProfile(self, p):
        # type can be -1 or +1
        o = self.optionSkeleton("Profile.json","POST")
        o.form = p
        return rp(o).then(a=>(a=="OK"))

    def browse(self, query, count,start):
        o = self.optionSkeleton("Browse.json","GET")
        o.qs = {
            Start: start,
            Count: count,
            Search_Query: query
        }
        return rp(o)

    def listTags(self, c, s){
        o = self.optionSkeleton("Browse/Tags.json","GET")
        o.qs = {
             Start: s,
             Count: c
        }
        return rp(o)

    def fav(self, id){
        o = self.optionSkeleton("Browse/Favouritejson","GET")
        o.qs = {
             "ID": id,
             "Key": self.loginData.SessionKey
        }
        return rp(o).then(a=>Boolean(a.Status))

    def remfav(self, id){
        o = self.optionSkeleton("Browse/Favouritejson","GET")
        o.qs = {
              "ID": id,
              "Key": self.loginData.SessionKey,
              "Mode": "Remove"
        }
        return rp(o).then(a=>Boolean(a.Status))

    def save(self, name, desc, data):
        # type can be -1 or +1
        o = self.optionSkeleton("Save.api","POST")
        o.form = {
            "Name": name,
            "Description": desc,
            "Data": data
        }
        o.json = false
        return rp(o).then(a=>{
            if(a.split(" ")[0]=="OK") return a.split(" ")[1]
        })

    def updateSave(self, id, data, desc):
        # type can be -1 or +1
        o = self.optionSkeleton("Vote.api","POST")
        o.form = {
            "ID": Number(id),
            "Description": desc,
            "Data": data
        }
        o.json = false
        return rp(o).then(a=>(a=="OK"))

    def saveData(self, id) {
        o1 = self.optionSkeleton("Browse/View.json","GET")
        o1.qs = {"ID":id}
        return rp(o)

    def _startup(self){
        return rp(self.optionSkeleton("Startup.json","GET"))

    def comments(self, id, c, s):
        o = self.optionSkeleton("Browse/Comments.json","GET")
        o.qs = {
            Start: s,
            Count: c,
            ID: id
        }
        return rp(o)
