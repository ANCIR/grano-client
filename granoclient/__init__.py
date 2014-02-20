from granoclient.base import GranoException, GranoServerException
from granoclient.base import NotFound, InvalidRequest
from granoclient.base import Client
from granoclient.common import Query
from granoclient.project import Project, ProjectCollection
from granoclient.schema import Schema, SchemaCollection
from granoclient.entity import Entity, EntityCollection


class Grano(object):
    """ Grano client library. This class provides basic access to many of 
    the core APIs for grano, including projects, and a global view of 
    entities and relations (seldomly useful, consider using the project-filtered
    versions instead.)

    The client library can be configured directly, or through a configuration
    file (``~/.grano.ini``) and a set of environment variables.

    :param api_host: (optional) host name URL to connect to, without any path 
        information (e.g. ``http://grano.io``).
    :param api_key: (optional) API key of the user which is running the
        requests.
    :param api_prefix: (optional) path prefix of the grano API, usually
        ``/api/1/``.
    """

    def __init__(self, api_host=None, api_key=None, api_prefix='/api/1/'):
        self.client = Client(api_host=api_host, api_key=api_key,
            api_prefix=api_prefix)

    @property
    def projects(self):
        """ Returns a :class:`granoclient.ProjectCollection` of all available 
        projects in this instance of grano. """
        if not hasattr(self, '_projects'):
            self._projects = ProjectCollection(self.client)
        return self._projects

    @property
    def entities(self):
        """ Returns a :class:`granoclient.EntityCollection` of all available 
        entities in this instance of grano.

        Consider using the ``entities`` of a specific :class:`granoclient.Project`
        instead.
        """
        if not hasattr(self, '_entities'):
            self._entities = EntityCollection(self.client)
        return self._entities

    def get(self, slug):
        """ Get a project. Shortcut to ``Grano.projects.by_slug()``.

        :param slug: the slug identifying the project to be retrieved.
        """
        return self.projects.by_slug(slug)

    def __repr__(self):
        return '<Grano(%s)>' % self.client.api_host

