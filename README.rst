grano client
============

This library provides a Python client for the [grano API](http://grano.pudo.org/rest_api.html). ``grano`` is a web-based framework for the storage, analysis and presentation of social network information. The tool provides building blocks for custom, data-driven investigative solutions.


Usage
-----

The Python client library can be used to edit projects, data schemata, entities and their relations remotely:

.. code-block:: python

    import granoclient
    
    project = granoclient.Project("germany")
    entity = dataset.match("Angela Merkel")
    print entity


### Installation

The easiest way to install the client is via the Python package index and pip/easy_install:

.. code-block:: bash

    pip install grano-client

If you want to develop the client library's code, check out the [repository](http://github.com/pudo/grani-client) and set up dependencies etc. with the command:

.. code-block:: bash

    python setup.py develop

``grano-client`` depends on [requests](http://requests.readthedocs.org/en/latest/) newer than 2.2.


Configuration
-------------

Several aspects of ``grano-client`` can be configured, including the host name of the ``grano`` server and the API key that is to be used for authentication. To determine these settings, the library will evaluate the following configuration sources in the listed order:

1. Read the ``~/.grano.ini`` file in the user's home directory. The file is a simple .ini configuration as detailed below.
2. Check the contents of the following environment variables: ``GRANO_HOST``, ``GRANO_APIKEY``.
3. Evaluate the keyword arguments passed into the constructor of ``grano.Project``.

A simple configuration file for ``grano-client`` might look like this:

.. code-block:: ini

    [client]
    host = http://api.grano.io
    api_key = xxxxxxxxxxxxxxx (see user profile in grano)


License
-------

Copyright (c) 2014, Friedrich Lindenberg

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
