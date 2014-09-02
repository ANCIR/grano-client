.. grano-client documentation master file, created by
   sphinx-quickstart on Tue Sep  2 15:25:17 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

grano-client: Python API client
===============================

`grano <http://granoproject.org>`_ is extended by a comprehensive Python client library that can be used to edit projects, data schemata, entities and their relations remotely:

.. code-block:: python

    import granoclient
    
    client = granoclient.Grano()
    for project in client.projects:
        print project.label

    project = client.get('my-project')
    project.label = 'New title'
    project.save()

    data = {'schemata': ['base'], 'properties': {'name': {'value': 'Alice'}}}
    alice = project.entities.create(data)

    data = {'schemata': ['base'], 'properties': {'name': {'value': 'Bob'}}}
    bob = project.entities.create(data)

    rel = {'schema': 'my-schema', 'source': alice, 'target': bob, 'properties': {}}
    project.relations.create(rel)

    query = project.entities.query().filter('properties-name', 'Alice')
    for entity in query:
        print entity.properties.get('name').get('value')


Installation
++++++++++++

The easiest way to install the client is via the Python package index and pip/easy_install:

.. code-block:: bash

    pip install grano-client

If you want to develop the client library's code, check out the `repository <http://github.com/granoproject/grano-client>`_ and set up dependencies etc. with the command:

.. code-block:: bash

    python setup.py develop

grano-client depends on `requests <http://requests.readthedocs.org/en/latest/>`_ newer than 2.2.


Configuration
+++++++++++++

Several aspects of grano-client can be configured, including the host name of the grano server and the API key that is to be used for authentication. To determine these settings, the library will evaluate the following configuration sources in given order:

1. Read the ``~/.grano.ini`` file in the user's home directory. The file is a simple .ini configuration as detailed below.
2. Check the contents of the following environment variables: ``GRANO_HOST``, ``GRANO_APIKEY``.
3. Evaluate the keyword arguments passed into the constructor of ``granoclient.Grano``.

A simple configuration file for grano-client might look like this:

.. code-block:: ini

    [client]
    host = http://beta.grano.cc

    # see user profile in grano:
    api_key = xxxxxxxxxxxxxxx


API
+++

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

