import os
import mimetypes


class GranoObject(object):
    """ Base class for objects to layer over the grano REST API. """

    def __init__(self, client, data):
        self.client = client
        self._data = data

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name != '_data' and self._data and name in self._data:
                return self._data[name]
            raise

    def __setattr__(self, name, value):
        if hasattr(self, '_data') and self._data is not None \
                and name in self._data.keys():
            self._data[name] = value
        else:
            return object.__setattr__(self, name, value)

    def __getitem__(self, name):
        return self._data[name]

    def get(self, name, default=None):
        return self._data.get(name, default)

    def __setitem__(self, name, value):
        self._data[name] = value


class GranoResource(GranoObject):
    """ A specific resource that is part of the grano API. """

    resource_key = 'id'

    def __init__(self, *args, **kwargs):
        super(GranoResource, self).__init__(*args, **kwargs)
        self._files = {}

    def reload(self):
        """ Reload the resource from the server. This is useful when the
        resource is a shortened index representation which needs to be
        traded in for a complete representation of the resource."""
        s, self._data = self.client.get(self.endpoint)

    def save(self):
        """ Update the server with any local changes, then update the
        local version with the returned value from the server. """
        s, self._data = self.client.post(self.endpoint, self._data,
                                         files=self._files)
        # clear files so that they aren't re-uploaded
        self._files = {}

    def set_file_property(self, name, file, source_url):
        self.properties[name] = {
            'name': name,
            'source_url': source_url,
            'active': True
        }
        self._files[name] = (os.path.basename(file.name), file,
                             mimetypes.guess_type(file.name, strict=False)[0],
                             {'Expires': '0'})

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self[self.resource_key])


class Query(GranoObject):
    """ A query is a mechanism to store query state and paginate
    through result sets returned by the server. """

    def __init__(self, client, clazz, endpoint, params=None):
        super(Query, self).__init__(client, None)
        self.clazz = clazz
        self.endpoint = endpoint
        self.params = params or {}

    def reload(self):
        """ Reload the results of the query. """
        s, self._data = self.client.get(self.endpoint, params=self.params)

    @property
    def data(self):
        if self._data is None:
            self.reload()
        return self._data

    def filter(self, name, value):
        """ Apply a filter to the query and return a modified version.

        :param name: the name of the query argument to add.
        :param value: the value of the query argument to add.
        """
        params = self.params.copy()
        params[name] = value
        return self.__class__(self.client, self.clazz, self.endpoint,
                              params=params)

    @property
    def results(self):
        """ The current page's results. """
        for res in self.data.get('results'):
            yield self.clazz(self.client, res)

    def __iter__(self):
        return self.results

    def limit(self, n):
        """ Define a limit for this query. """
        return self.filter('limit', n)

    def offset(self, n):
        """ Define an offset for this query. """
        return self.filter('offset', n)

    @property
    def total(self):
        """ The total number of results available (across all pages). """
        return self.data.get('total')

    @property
    def has_next(self):
        """ Check to see if a next page is available. """
        return self.data.get('next_url') is not None

    @property
    def has_prev(self):
        """ Check to see if a previous page is available. """
        return self.data.get('prev_url') is not None

    @property
    def next(self):
        """ Return a derived query for the next page of elements. """
        return self.__class__(self.client, self.clazz,
                              self.data.get('next_url'))

    @property
    def prev(self):
        """ Return a derived query for the previous page of elements. """
        return self.__class__(self.client, self.clazz,
                              self.data.get('next_url'))

    def __len__(self):
        return self.total


class GranoCollection(GranoObject):
    """ A REST collection provided by the grano API. """

    query_clazz = Query

    def __init__(self, client, params={}):
        super(GranoCollection, self).__init__(client, None)
        self.params = params

    def query(self, params=None):
        """ Begin querying the collection. The query can further be refined
        using the methods of the returned :class:`granoclient.Query`."""
        if params is None:
            params = {}
        params.update(self.params)
        return self.query_clazz(self.client, self.clazz, self.endpoint, params=params)

    def all(self):
        """ Iterate over all available resources in the collection.
        This can also be done by just iterating over the collection::

            for resource in collection:
                ...
        """
        query = self.query()
        while True:
            for resource in query.results:
                yield resource

            if not query.has_next:
                break
            query = query.next

    def _create(self, data):
        if 'files' in data:
            data = data.copy()
            files = data.pop('files')
        else:
            files = {}

        s, data = self.client.post(self.endpoint, data=data, files=files)
        return self.clazz(self.client, data)

    def __iter__(self):
        return self.all()

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.endpoint)
