from granoclient.base import GranoException, GranoServerException
from granoclient.base import Client
from granoclient.project import Project, ProjectCollection


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

