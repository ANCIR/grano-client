import yaml
import logging
from granoclient.common import GranoResource, GranoCollection
from granoclient.base import NotFound

log = logging.getLogger()


class Schema(GranoResource):
    """ A schema within grano. Schemata define the types of entities and
    relations that are stored within a grano project. See also
    :ref:`schema`."""

    resource_key = 'name'

    def __init__(self, client, base_endpoint, data):
        self.base_endpoint = base_endpoint
        super(Schema, self).__init__(client, data)

    @property
    def endpoint(self):
        return '%s/%s' % (self.base_endpoint, self['name'])


class SchemaCollection(GranoCollection):
    """ Represents all the :class:`granoclient.Schema` currently available
    in a given project. Provides functionality to search for, filter
    and create elements.
    """

    clazz = Schema

    @property
    def endpoint(self):
        return '/projects/%s/schemata' % self.project_slug

    def query(self, params=None):
        """ Begin querying the collection. The query can further be refined
        using the methods of the returned :class:`granoclient.Query`."""
        clazz = lambda client, data: self.clazz(client, self.endpoint, data)
        return self.query_clazz(self.client, clazz, self.endpoint,
                                params=params)

    def __init__(self, client, project_slug):
        self.project_slug = project_slug
        super(SchemaCollection, self).__init__(client)

    def by_name(self, name):
        """ Load a schema based on its name, i.e. its unique designation.

        :param name: the name of the project to be retrieved.

        """
        status, data = self.client.get(self.endpoint + '/%s' % name)
        return self.clazz(self.client, self.endpoint, data)

    def create(self, data):
        """ Create a new schema.

        :param data: A dictionary with the schemas attributes, ``name``
            and ``label`` are required, but several ``attributes`` should
            be given. See :ref:`schema` for details.
        """
        if isinstance(data, Schema):
            data = data._data
        s, data = self.client.post(self.endpoint, data=data)
        return self.clazz(self.client, self.endpoint, data)

    def upsert(self, data):
        """ Import a schema from an object. This attempts to either create or
        update schemata based on the specification given. """
        name = data.get('name')
        try:
            schema = self.by_name(name)
            schema._data = data
            schema.save()
            log.info('Updated schema: %s', schema.label)
        except NotFound:
            schema = self.create(data)
            log.info('Created schema: %s', schema.label)


    def upsert_from_file(self, file_name):
        """ Same as ``from_list``, but works on a file name. """
        # TODO: should this be a file object?
        with open(file_name, 'rb') as fh:
            data = yaml.load(fh)
            if not isinstance(data, (list, tuple)):
                data = [data]
            for schema in data:
                self.upsert(schema)
