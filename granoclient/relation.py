from granoclient.common import GranoResource, GranoCollection
from granoclient.schema import Schema


class Relation(GranoResource):
    """ A relation within grano. This type serves as a connection between
    two entities, it can also be used to store data (in the form of properties). """
    
    resource_key = 'id'

    @property
    def endpoint(self):
        return '/relations/%s' % self['id']

    @property
    def project(self):
        """ The :class:`granoclient.Project` to which this relation belongs. """
        from granoclient.project import Project
        return Project(self.client, self['project'])

    @property
    def schema(self):
        """ The :class:`granoclient.Schema`. """
        return Schema(self.client, self.endpoint, self['schema'])

    @schema.setter
    def set_schema(self, schema):
        self['schema'] = schema

    @property
    def source(self):
        """ The source :class:`granoclient.Entity`. """
        from granoclient.entity import Entity
        return Entity(self.client, self['source'])

    @source.setter
    def set_source(self, source):
        self['source'] = source

    @property
    def target(self):
        """ The target :class:`granoclient.Entity`. """
        from granoclient.entity import Entity
        return Entity(self.client, self['target'])
    
    @source.setter
    def set_target(self, target):
        self['target'] = target


class RelationCollection(GranoCollection):
    """ Represents all the :class:`granoclient.Relation` currently available
    in this instance of grano. Provides functionality to search for, filter
    and create elements.
    """

    clazz = Relation
    endpoint = '/relations'

    def by_id(self, id):
        """ Load a relation based on its id, i.e. its unique designation.

        :param id: the id of the relation to be retrieved.

        """
        status, data = self.client.get(self.endpoint + '/%s' % id)
        return self.clazz(self.client, data)

    def create(self, data):
        """ Create a new relation. 

        :param data: A dictionary with the relation attributes, ``schema`` 
            ``source``, ``target`` and ``properties`` are required.
        """
        from granoclient.schema import Schema
        from granoclient.entity import Entity

        if 'project' in self.params and not 'project' in data:
            data['project'] = self.params.get('project')

        if isinstance(data, Relation):
            data = data._data
        if isinstance(data.get('schema'), Schema):
            data['schema'] = data.get('schema').name
        if isinstance(data.get('source'), Entity):
            data['source'] = data.get('source').id
        if isinstance(data.get('target'), Entity):
            data['target'] = data.get('target').id
        return self._create(data)
