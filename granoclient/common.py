#from granoclient.base import Client

class GranoObject(object):
    """ Base class for objects to layer over the grano REST API. """

    def __init__(self, client, data):
        self.client = client
        self._data = data

    def __getattr__(self, name):
        if not name in self._data:
            raise AttributeError
        return self._data[name]

    def __getitem__(self, name):
        return self.__getattr__(name)


class GranoResource(object):
    """ A specific resource that is part of the grano API. """

    resource_key = 'id'

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

    @property
    def results(self):
        """ The current page's results. """
        for res in self.data.get('results'):
            yield self.clazz(self.client, res)

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
        return Query(self.client, self.clazzz, self.data.get('next_url'))

    @property
    def prev(self):
        """ Return a derived query for the previous page of elements. """
        return Query(self.client, self.clazzz, self.data.get('next_url'))

    def __len__(self):
        return self.total


class GranoCollection(GranoObject):
    """ A REST collection provided by the grano API. """

    def query(self, params=None):
        """ Begin querying the collection. The query can further be refined
        using the methods of the returned :class:`granoclient.Query`."""
        return Query(self.client, self.clazz, self.endpoint, params=params)

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
        s, data = self.client.post(self.endpoint, data=data)
        print s, data
        return self.clazz(self.client, data)

    def __iter__(self):
        return self.all()

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.endpoint)
