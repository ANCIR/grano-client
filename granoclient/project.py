from granoclient.base import GranoObject, GranoCollection

class Project(GranoObject):
    """ A project within grano. This type serves as a namespace for use 
    cases of the application. Each project has its own schemata, entities and 
    relations. """
    pass


class ProjectCollection(GranoCollection):
    """ Represents all the :class:`Project` currently available in this instance
    of grano. Provides functionality to search for, filter and create elements.
    """

    clazz = Project

    def __init__(self, client, data):
        super(ProjectCollection).__init__(self, client, data)

    @classmethod
    def by_slug()
