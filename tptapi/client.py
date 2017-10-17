import requests
import six
import hashlib
from . import errors


def md5(data):
    """Returns the string hashed with MD5

    :param data: String that you want hashed with md5
    :return: :class:`str`
    :rtype: str
    """
    return hashlib.md5(data.encode("utf-8")).hexdigest()


class Client(object):
    def __init__(self):
        self.base_url = "http://powdertoy.co.uk"
        self.session = requests.Session()
        self.session.headers.update(self._headers())
        self.SessionID = ''

    def _get(self, url, params=None):
        """Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.session.get(url, params=params)

    def _post(self, url, params=None, data=None):
        """Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary (will be form-encoded), bytes,
            or file-like object to send in the body of the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self.session.post(url, params=params, data=data)

    @staticmethod
    def _headers():
        """Returns common headers for all requests (GET & POST) to the API"""
        headers = {
            "X-Auth-User-Id": "0",
            "X-Auth-Session-Key": "0",
            "User-Agent": "PowderToy/92.2 (WIN32; SSE3; M0) TPTPP/92.2.333R.0"
        }

        return headers

    def login(self, user, password):
        """Initiates a login with the website. Returns a boolean

        :param user: Username used to login to The Powder Toy's website.
        :param password: password used to login to The Powder Toy's website.
        :return: :class:`bool` bool
        :rtype: bool
        """
        form = {
            "Username": user,
            "Hash": md5("{0}-{1}".format(user, md5(password)))
        }
        r = self._post(self.base_url + "/Login.json", data=form)
        j = r.json()
        status_ok = j['Status'] == 1
        if status_ok:
            self.session.headers["X-Auth-User-Id"] = str(j["UserID"])
            self.session.headers["X-Auth-Session-Key"] = str(j["SessionKey"])
            self.SessionID = j['SessionID']
            if len(j["Notifications"]):
                notif = ", ".join(j["Notifications"])
                six.print_("User has a new notifications: {0!s}".format(notif))
        else:
            raise errors.InvalidLogin("There was a problem logging you in.")
        return status_ok

    def check_login(self):
        """Checks if your login is valid

        >>> import tptapi
        >>> client = tptapi.Client()
        >>> client.check_login()

        :return: :class:`bool` bool
        :rtype: bool
        """
        r = self._get(self.base_url + "/Login.json").json()
        return r["Status"] == 1

    def vote(self, ID, action):
        """Used to cast a vote on a save.

        >>> import tptapi
        >>> client = tptapi.Client()
        >>> client.vote(id, action)

        :param action: Integer. Upvote or Downvote a save.
        :return: :class:`bool` bool
        :rtype: bool
        """
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Action": "Up" if action > 0 else "Down"
        }
        r = self._post(self.base_url + "/Vote.api", data=form)
        return r.text() == "OK"

    def comment(self, ID, content):
        """Posts a comment on specified save ID.

        :param ID: Integer. The save number you want to post a comment on.
        :return: :class:`bool` bool
        :rtype: bool
        """
        r = self._post(self.base_url + "/Browse/Comments.json",
                       data={"Comment": content},
                       params={"ID": ID})
        if r.json["Status"] == 0:
            raise errors.InvalidLogin("You are not logged in.")
        return r.json['Status'] == 1

    def add_tag(self, ID, tag):
        """Adds a tag to a specified save ID.

        :param ID: Integer. The save number you wish to add a tag to.
        :param tag: String. The tag you wish to add to the specified save.
        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "add",
            "Key": self.session.headers["X-Auth-Session-Key"]
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status_code == requests.codes.ok

    def delete_tag(self, ID, tag):
        """Removes a tag from a specified save ID

        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Tag": tag,
            "Op": "delete",
            "Key": self.session.headers["X-Auth-Session-Key"]
        }
        r = self._get(self.base_url + "/Browse/EditTag.json", params=qs)
        return r.status

    def delete_save(self, ID):
        """Deletes a specified save ID

        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Mode": "Delete",
            "Key": self.session.headers["X-Auth-Session-Key"]
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def unpublish_save(self, ID):
        """Unpublishes a specified save ID

        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Mode": "Unpublish",
            "Key": self.session.headers["X-Auth-Session-Key"]
        }
        r = self._get(self.base_url + "/Browse/Delete.json", params=qs)
        return r.status_code == requests.codes.ok

    def publish_save(self, ID):
        """Makes a specified save public

        :return: :class:`bool`
        :rtype: bool
        """
        r = self._post(self.base_url + "/Browse/View.json",
                       data={"ActionPublish": 1},
                       params={"ID": ID, "Key": self.session.headers["X-Auth-Session-Key"]})
        return r.text() == "1"

    def set_profile(self, p):
        """Updates your profile

        :return: :class:`bool`
        :rtype: bool
        """
        # action can be -1 or +1
        r = self._post(self.base_url + "/Profile.json", data=p)
        return r.text() == "OK"

    def browse(self, query=None, count=20, start=0):
        """Browse saves with given query.

        :return: :class:`dict`
        :rtype: dict
        """
        qs = {
            "Start": start,
            "Count": count,
            "Search_Query": query
        }
        r = self._get(self.base_url + "/Browse.json", params=qs)
        return r.json()

    def list_tags(self, count=24, start=0):
        """Returns a list of tags.

        :return: :class:`list` object
        :rtype: list
        """
        qs = {
            "Start": start,
            "Count": count
        }
        r = self._get(self.base_url + "/Browse/Tags.json", params=qs)
        return r.json()["Tags"]

    def add_fav(self, ID):
        """Add a save to your favourites.

        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Key": self.session.headers["X-Auth-Session-Key"]
        }
        r = self._get(self.base_url + "/Browse/Favourite.json", params=qs)
        return r.status_code == requests.codes.ok

    def remove_fav(self, ID):
        """Remove a save from your favourites.

        :return: :class:`bool`
        :rtype: bool
        """
        qs = {
            "ID": ID,
            "Key": self.session.headers["X-Auth-Session-Key"],
            "Mode": "Remove"
        }
        r = self._get(self.base_url + "/Browse/Favourite.json", params=qs)
        return r.status_code == requests.codes.ok

    def save(self, name, desc, data):
        """Upload a save to the website.

        :return: :class:`int`
        :rtype: int
        """
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
        """Update a save's metadata.

        :return: :class:`bool`
        :rtype: bool
        """
        # action can be -1 or +1
        form = {
            "ID": int(ID),
            "Description": desc,
            "Data": data
        }
        r = self._post(self.base_url + "/Save.api", data=form)
        return r.text() == "OK"

    def save_data(self, ID):
        """Get JSON data on a specified save.

        :return: :class:`dict`
        :rtype: dict
        """
        r = self._get(self.base_url + "/Browse/View.json", params={"ID": ID})
        return r.json()

    def startup(self):
        """Get startup.json contents.

        :return: :class:`dict`
        :rtype: dict
        """
        return self._get(self.base_url + "/Startup.json").json()

    def comments(self, ID, count, start):
        """Get comments on a particular save

        :return: :class:`dict` object
        :rtype: dict
        """
        qs = {
            "Start": start,
            "Count": count,
            "ID": ID
        }
        r = self._get(self.base_url + "/Browse/Comments.json", params=qs)
        return r.json()
