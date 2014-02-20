from granoclient.common import GranoResource, GranoCollection

class Project(GranoResource):
    """ A project within grano. This type serves as a namespace for use 
    cases of the application. Each project has its own schemata, entities and 
    relations. """
    
    resource_key = 'slug'

    @property
    def endpoint(self):
        return '/projects/%s' % self['slug']


class ProjectCollection(GranoCollection):
    """ Represents all the :class:`granoclient.Project` currently available
    in this instance of grano. Provides functionality to search for, filter
    and create elements.
    """

    clazz = Project
    endpoint = '/projects'

    def __init__(self, client, data):
        super(ProjectCollection, self).__init__(client, data)

    def by_slug(self, slug):
        """ Load a project based on its slug, i.e. its unique designation.

        :param slug: the slug of the project to be retrieved.

        """
        status, data = self.client.get(self.endpoint + '/%s' % slug)
        return self.clazz(self.client, data)

    def create(self, data):
        """ Create a new project. 

        :param data: A dictionary with the projects attributes, ``slug`` 
            and ``label`` are required.
        """
        if isinstance(data, Project):
            data = data._data
        return self._create(data)
