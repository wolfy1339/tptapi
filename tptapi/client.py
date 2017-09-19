import requests
import six
import hashlib
from . import errors


def md5(data):
    return hashlib.md5(data.encode("utf-8")).hexdigest()


class Client(object):
    def __init__(self):
        self.base_url = "http://powdertoy.co.uk"
        self.session = requests.Session()
        self.loginData = {}

    def _get(self, url, params=None):
        headers = self._headers()
        return self.session.get(url, params=params, headers=headers)

    def _post(self, url, params=None, data=None):
        return self.session.post(url,
                                 params=params,
                                 data=data,
                                 headers=self._headers())

    _get.__doc__ = requests.get.__doc__
    _post.__doc__ = requests.post.__doc__

    def _headers(self):
        headers = {
            "X-Auth-User-Id": "0",
            "X-Auth-Session-Key": "0"
        }
        if len(self.loginData):
            headers["X-Auth-User-Id"] = self.loginData["UserID"]
            headers["X-Auth-Session-Key"] = self.loginData["SessionKey"]
        return headers

    def login(self, user, password):
        """Client.login(user, password)
        Initiates a login with the website. Returns a boolean"""
        form = {
            "Username": user,
            "Hash": md5("{0}-{1}".format(user, md5(password)))
        }
        r = self._post(self.base_url + "/Login.json", data=form)
        if r.json()['Status'] == 1:
            self.loginData.update(r.json())
            j = r.json()
            self.loginData["UserID"] = str(j["UserID"])
            self.loginData["SessionKey"] = str(j["SessionKey"])
            if len(j["Notifications"]):
                notif = ", ".join(j["Notifications"])
                six.print_("User has a new notifications: {0!s}".format(notif))
            del self.loginData["Status"]
            del self.loginData["Notifications"]
        else:
            raise errors.InvalidLogin("There was a problem logging you in.")
        return r.json()['Status'] == 1

    def check_login(self):
        """Checks if your login is valid"""
        r = self._get(self.base_url + "/Login.json").json()
        return r["Status"] == 1

    def vote(self, ID, action):
        """Used to cast a vote on a save, you need to do Client.vote(id, type)
        where type is a negative or positive number that defines if it's
        an upvote or a downvote.
        Returns a boolean."""
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Action": "Up" if action > 0 else "Down"
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def comment(self, ID, content):
        """Posts a comment on specified save ID.
        Returns a boolean"""
        r = self._post(self.base_url + "/Browse/Comments.json",
                       data={"Comment": content},
                       params={"ID": ID})
        if r.json["Status"] == 0:
            raise errors.InvalidLogin("You are not logged in.")
        return r.json['Status'] == 1

    def add_tag(self, ID, tag):
        """Adds a tag to a specified save ID.
        Returns a boolean"""
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "add",
            "Key": self.loginData['SessionKey']
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status_code == requests.codes.ok

    def delete_tag(self, ID, tag):
        """Removes a tag from a specified save ID
        Returns a boolean"""
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "delete",
            "Key": self.loginData['SessionKey']
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status

    def delete_save(self, ID):
        """Deletes a specified save ID
        Returns a boolean"""
        qs = {
            "ID": ID,
            "Mode": "Delete",
            "Key": self.loginData['SessionKey']
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def unpublish_save(self, ID):
        """Unpublishes a specified save ID
        Returns a boolean"""
        qs = {
            "ID": ID,
            "Mode": "Unpublish",
            "Key": self.loginData['SessionKey']
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def publish_save(self, ID):
        """Makes a specified save public
        Returns a boolean"""
        r = self._post(self.base_url + "/Browse/View.json",
                       data={"ActionPublish": 1},
                       params={"ID": ID, "Key": self.loginData["SessionKey"]})
        return r.text() == "1"

    def set_profile(self, p):
        """Updates your profile
        {
            "location": <string>,
            "biography": <string>,
            "DOB": <date in the format DD-MM-YYY>,
            "Email:" <email>,
            "ConfirmPassword": <password if changing email>,
            "Website": <URL string>,
            "BetaEnroll": <1 for yes, 0 for no>,
            "WYSIWYG": <1 for yes, 0 for no>,
            "EditUser": "Save"
        }"""
        # action can be -1 or +1
        r = self._post(self.base_url + "/Profile.json", data=p)
        return r.text() == "OK"

    def browse(self, query, count, start):
        """Browse saves with given query"""
        qs = {
            "Start": start,
            "Count": count,
            "Search_Query": query
        }
        r = self._get(self.base_url + "/Browse.json", params=qs)
        return r.json()

    def list_tags(self, c, s):
        """Returns a list of tags"""
        qs = {
            "Start": s,
            "Count": c
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.json()["Tags"]

    def add_fav(self, ID):
        """Favourite a save"""
        qs = {
            "ID": ID,
            "Key": self.loginData["SessionKey"]
        }
        r = self._get(self.base_url + "/Browse/Favourite.json", params=qs)
        return r.status_code == requests.codes.ok

    def remove_fav(self, ID):
        """Remove a save from your favourites"""
        qs = {
            "ID": ID,
            "Key": self.loginData["SessionKey"],
            "Mode": "Remove"
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.status_code == requests.codes.ok

    def save(self, name, desc, data):
        """Upload a save to the website"""
        # action can be -1 or +1
        form = {
            "Name": name,
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Save.api", data=form).text()
        if r.split(" ")[0] == "OK":
            return r.split(" ")[1]

    def update_save(self, ID, data, desc):
        """Update a save's metadata"""
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Save.api", data=form)
        return r.text() == "OK"

    def save_data(self, ID):
        """Get JSON data on a specified save"""
        r = self._get(self.base_url + "/Browse/View.json", params={"ID": ID})
        return r.json()

    def startup(self):
        """Get startup.json contents"""
        return self._get(self.base_url + "/Startup.json").json()

    def comments(self, ID, count, start):
        """Get comments on a particular save"""
        qs = {
            "Start": start,
            "Count": count,
            "ID": ID
        }
        r = self._get(self.base_url + "/Browse/Comments.json", params=qs)
        return r.json()
