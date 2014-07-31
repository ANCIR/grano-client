from ConfigParser import SafeConfigParser
import json
import os

import requests


class GranoException(Exception):
    """ An exception produced by the grano client library, possibly as part 
    of it's interaction with the server. """
    
    def __init__(self, message):
        self.message = message 

    def __unicode__(self):
        return unicode(self.message)

    def __str__(self):
        return unicode(self).encode('ascii', 'replace')

    def __repr__(self):
        return '<GranoException("%s")>' % self.message


class GranoServerException(GranoException):
    """ An exception produced by the grano server. The most common types of 
    errors include:

    * Missing objects (404), i.e. the client requested data that does not 
      exist on the server. 
    * Invalid inputs (400), i.e. the data submitted by the client did not 
      pass validation - it may be incomplete.
    """ 

    def __init__(self, response):
        self.status = response.get('status')
        self.name = response.get('name')
        self.message = response.get('message', response.get('description'))
        self.description = response.get('description')
        self.data = response

    def __repr__(self):
        return '<GranoServerException(%s, "%s")>' % (self.status, self.message)


class InvalidRequest(GranoServerException): pass
class NotFound(GranoServerException): pass


class Client(object):
    """ Grano client class; handles configuration and network
    settings. Do not instantiate directly, use ``Grano`` instead. """

    def __init__(self, api_host, api_key, api_prefix='/api/1/'):
        config = SafeConfigParser()
        config.read([os.path.expanduser('~/.grano.ini')])
        if config.has_section('client'):
            config = dict(config.items('client'))
        else:
            config = {}

        if not api_host:
            api_host = os.environ.get('GRANO_HOST',
                config.get('host', 'http://localhost:5000'))

        if not api_key:
            api_key = os.environ.get('GRANO_APIKEY',
                config.get('api_key'))

        if api_host.endswith('/') and api_prefix.startswith('/'):
            api_prefix = api_prefix[1:]
        self.api_host = api_host
        self.api_key = api_key
        self.api_prefix = api_prefix

    @property
    def session(self):
        if not hasattr(self, '_session'):
            headers = {'Accept': 'application/json'}
            if self.api_key:
                headers['X-Grano-API-Key'] = self.api_key
            self._session = requests.Session()
            self._session.headers.update(headers)
        return self._session

    def path(self, endpoint):
        if endpoint.startswith(self.api_host + self.api_prefix):
            return endpoint
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        return self.api_host + self.api_prefix + endpoint

    def evaluate(self, response):
        try:
            data = response.json()
        except ValueError:
            raise GranoException('Server did not respond with JSON data.')
        if response.status_code == 400:
            raise InvalidRequest(data)
        if response.status_code == 404:
            raise NotFound(data)
        if (not response.ok) and 'status' in data and 'message' in data:
            raise GranoServerException(data)
        return response.status_code, data

    def get(self, endpoint, params={}):
        response = self.session.get(self.path(endpoint), params=params)
        return self.evaluate(response)

    def post(self, endpoint, data={}, files={}):
        data = {'data': json.dumps(data)}
        response = self.session.post(self.path(endpoint),
            allow_redirects=True, data=data, files=files)
        return self.evaluate(response)
