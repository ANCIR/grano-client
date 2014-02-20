from granoclient.common import GranoResource, GranoCollection
from granoclient.schema import Schema


class Entity(GranoResource):
    """ An entity within grano. This type serves as a node, which can be
    used to store data (in the form of properties), and can be part of 
    relations.. """
    
    resource_key = 'id'

    @property
    def endpoint(self):
        return '/entities/%s' % self['slug']


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
        if isinstance(data, Entity):
            data = data._data
        schemata = data.get('schemata')
        data['schemata'] = []
        for schema in schemata:
            if isinstance(schema, Schema):
                schema = schema.name
        return self._create(data)
