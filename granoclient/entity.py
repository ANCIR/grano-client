from granoclient.common import GranoResource, GranoCollection
from granoclient.schema import Schema


class Entity(GranoResource):
    """ An entity within grano. This type serves as a node, which can be
    used to store data (in the form of properties), and can be part of
    relations.. """

    resource_key = 'id'

    @property
    def endpoint(self):
        return '/entities/%s' % self['id']

    @property
    def project(self):
        """ The :class:`granoclient.Project` to which this entity belongs. """
        from granoclient.project import Project
        return Project(self.client, self['project'])

    @property
    def inbound(self):
        """ Inbound relations as a filtered
        :class:`granoclient.RelationCollection`. """
        from granoclient.relation import RelationCollection
        return RelationCollection(self.client, params={'target': self.id})

    @property
    def outbound(self):
        """ Outbound relations as a filtered
        :class:`granoclient.RelationCollection`. """
        from granoclient.relation import RelationCollection
        return RelationCollection(self.client, params={'source': self.id})

    def get_graph(self, depth=2):
        entity_graph = EntityGraph(self.client,
            params={'id': self.id, 'depth': depth})
        return entity_graph.get_data()


class EntityCollection(GranoCollection):
    """ Represents all the :class:`granoclient.Entity` currently available
    in this instance of grano. Provides functionality to search for, filter
    and create elements.
    """

    clazz = Entity
    endpoint = '/entities'

    def by_id(self, id):
        """ Load an entity based on its id, i.e. its unique designation.

        :param id: the id of the entity to be retrieved.

        """
        status, data = self.client.get(self.endpoint + '/%s' % id)
        return self.clazz(self.client, data)

    def create(self, data):
        """ Create a new entity.

        :param data: A dictionary with the entity attributes, ``schemata``
            and ``properties`` are required.
        """

        if 'project' in self.params and not 'project' in data:
            data['project'] = self.params.get('project')

        if isinstance(data, Entity):
            data = data._data
        schemata = data.get('schemata')
        data['schemata'] = []
        for schema in schemata:
            if isinstance(schema, Schema):
                schema = schema.name
            data['schemata'].append(schema)
        return self._create(data)


class EntityGraph(object):
    """ An entity within grano. This type serves as a node, which can be
    used to store data (in the form of properties), and can be part of
    relations.. """

    resource_key = 'id'

    def __init__(self, client, params={}):
        self.client = client
        self.params = params

    @property
    def endpoint(self):
        return '/entities/%(id)s/graph?depth=%(depth)s' % {
            'id': self.params['id'],
            'depth': self.params['depth']
        }

    def get_data(self):
        s, data = self.client.get(self.endpoint)
        return data
