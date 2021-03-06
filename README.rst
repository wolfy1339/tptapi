TPTAPI
======
|BCH compliance| |Codacy| |Landscape|


This package interacts with `The Powder Toy <http://powdertoy.co.uk>`__'s API.

Usage:
------

.. code:: python

    import tptapi

    client = tptapi.Client()

Login
~~~~~

Most actions need a session token you can obtain from Login:
``client.login(user, password)`` returns a boolean.

Check Login
~~~~~~~~~~~

To verify that your session is still valid you can run checkLogin:
``client.check_login()`` which will return a boolean.

Vote [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~

To cast a vote, you need to do ``client.vote(id, type)`` where type is a
negative or positive number that defines if it's a upvote or downvote.
Returns a boolean.

Comment [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~

To add a comment, you need to do ``client.comment(id, text)``. Returns a
boolean.

Add Tag [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~

To add a tag, you need to do ``client.add_tag(id, name)``. Returns a
boolean.

Delete Tag [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a tag, you need to do ``client.delete_tag(id, name)``. Returns a
boolean.

Delete Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a save, you need to do ``client.delete_save(id)``. Returns a
boolean.

Unpublish Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To unpublish a save, you need to do ``client.unpublish_tag(id)``. Returns
a boolean.

Publish Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To publish a save, you need to do ``client.publish_save(id)``. Returns a
boolean.

Update Profile [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update your profile, you need to do ``client.set_profile(data)``.
Returns a boolean.

Browse [LOGIN ENHACES OUTPUT]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To browse, you need to do ``client.browse(query, count, offset)``.
Returns results.

List Tags
~~~~~~~~~

To list tags, you need to do ``client.list_tags(start, count)``. Returns
array of tags.

Favourite a Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a save to favutrites, you need to do ``client.add_fav(id)``. Returns
a boolean.

UnFavourite a Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a save from favutrites, you need to do ``client.remove_fav(id)``.
Returns a boolean.

Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~

Saves a CPS file. Data has to be OPS1-encoded save.

.. code:: python

    data = open("save.cps", "br").read()
    client.save(name, description, data)

Returns the save id.

Update Save [LOGIN NEEDED]
~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates a save with new description and content. Data has to be
OPS1-encoded save.

.. code:: python

    data = open("save.cps", "br").read()
    client.updateSave(id, description, data)

Returns a boolean.

Startup Data [LOGIN ENHACES OUTPUT]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns Startup.json data. ``client.startup()``

Save's Comments
~~~~~~~~~~~~~~~

Returns a save's comments. ``client.comments(id, count, offset)``

.. |BCH compliance| image:: https://bettercodehub.com/edge/badge/wolfy1339/tptapi?branch=master
   :target: https://bettercodehub.com/

.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/6fc2b55ae1c14858a0bdf4639ebe69fc
   :target: https://www.codacy.com/app/wolfy1339/tptapi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=wolfy1339/tptapi&amp;utm_campaign=Badge_Grade

.. |Landscape| image:: https://landscape.io/github/wolfy1339/tptapi/master/landscape.svg?style=flat
   :target: https://landscape.io/github/wolfy1339/tptapi/master
   :alt: Code Health
