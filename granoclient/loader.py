import os
import logging
import mimetypes
from threading import RLock

from granoclient.base import InvalidRequest


log = logging.getLogger(__name__)


class ObjectLoader(object):
    # Abstract parent

    def _setup(self, loader, schemata):
        self.loader = loader
        self.schemata = schemata
        self.properties = {}
        self.update_criteria = set()
        self.files = {}

    def unique(self, name, only_active=True):
        """ Define a unique field for this entity or relation. Each unique
        key will be used to decide whether a record already exists and can
        be updated, or whether a new one must be created.

        :param name: The property name of the unique field.
        :param only_active: If set to ``False``, the check will include all
            historic values of the property as well as the current value.
        """
        self.update_criteria.add((name, only_active))

    def set(self, name, value, source_url=None):
        """ Set the value of a given property, optionally by attributing a
        source URL.

        :param name: The property name. This must be defined as part of one
            of the schemata that the entity or relation is associated with.
        :param value: The value to be set for this property. If it is
            ``None``, the property will not be set, but existing values of
            will be marked as inactive.
        :param source_url: A URL which will be set as the origin of this
            information.
        """
        source_url = source_url or self.source_url
        if source_url is None:
            log.warning('No source for property %s.', name)
        self.properties[name] = {
            'name': name,
            'source_url': source_url,
            'active': True
        }
        # add it to files instead if it's a file-like object
        if callable(getattr(value, 'read', None)) and hasattr(value, 'name'):
            self.files[name] = (os.path.basename(value.name), value,
                                mimetypes.guess_type(value.name, strict=False)[0],
                                {'Expires': '0'})
        else:
            self.properties[name]['value'] = value if value is None else unicode(value)

    def lock(self):
        sig = self.signature
        if sig not in self.loader.locks:
            self.loader.locks[sig] = RLock()
        return self.loader.locks[sig]


class EntityLoader(ObjectLoader):
    """ A factory object for entities, used to set the schemata and
    properties for an entity. """

    def __init__(self, loader, schemata, source_url=None):
        self._setup(loader, schemata + ['base'])
        self.unique('name', only_active=False)
        self.source_url = source_url
        self._entity = None

    @property
    def signature(self):
        keys = []
        for p, a in self.update_criteria:
            keys.append(self.properties.get(p, {}).get('value'))
        return tuple(keys)

    @property
    def entity(self):
        if self._entity is None:
            self.save()
        return self._entity

    def save(self):
        """ Save the entity to the database. Do this only once, after all
        properties have been set. """

        with self.lock():
            q = self.loader.project.entities.query()
            for name, only_active in self.update_criteria:
                value = self.properties.get(name).get('value')
                key = 'property-'
                if not only_active:
                    key = key + 'aliases-'
                q = q.filter(key + name, value)

            try:
                entities = list(q.results)
                if len(entities) == 0:
                    data = {
                        'schemata': self.schemata,
                        'properties': self.properties,
                        'files': self.files
                    }
                    self._entity = self.loader.project.entities.create(data)
                else:
                    if len(entities) > 1:
                        log.warn("Ambiguous update: %r" % entities)
                    self._entity = entities[0]
                    self._entity._data['schemata'].extend(self.schemata)
                    self._entity._data['properties'].update(self.properties)
                    self._entity._files.update(self.files)
                    self._entity.save()
            except InvalidRequest, inv:
                log.warning("Validation error: %r", inv)


class RelationLoader(ObjectLoader):
    """ A factory object for relations, used to construct a relation by setting
    its schema, source entity, target entity and a set of properties. """

    def __init__(self, loader, schema, source, target, source_url=None):
        self._setup(loader, [schema])
        self.source_url = source_url
        self.source = source
        self.target = target

    @property
    def signature(self):
        keys = [self.source.signature, self.target.signature]
        for p, a in self.update_criteria:
            keys.append(self.properties.get(p, {}).get('value'))
        return tuple(keys)

    def save(self):
        """ Save the relation to the database. Do this only once, after all
        properties have been set. """

        with self.lock():
            q = self.loader.project.relations.query()
            q = q.filter('source', self.source.entity.id)
            q = q.filter('target', self.target.entity.id)

            for name, only_active in self.update_criteria:
                value = self.properties.get(name).get('value')
                key = 'property-'
                if not only_active:
                    key = key + 'aliases-'
                q = q.filter(key + name, value)

            try:
                relations = list(q.results)
                if len(relations) == 0:
                    data = {
                        'schema': self.schemata.pop(),
                        'source': self.source.entity.id,
                        'target': self.target.entity.id,
                        'properties': self.properties,
                        'files': self.files
                    }
                    self.loader.project.relations.create(data)
                else:
                    if len(relations) > 1:
                        log.warn("Ambiguous update: %r" % relations)
                    rel = relations[0]
                    rel._data['schema'] = self.schemata.pop()
                    rel._data['source'] = self.source.entity.id
                    rel._data['target'] = self.target.entity.id
                    rel._data['properties'].update(self.properties)
                    rel._files.update(self.files)
                    rel.save()
            except InvalidRequest, inv:
                log.warning("Validation error: %r", inv)


class Loader(object):
    """ A loader is a factory object that can be used to make entities and
    relations in the database. It will perform some validation and handle
    database transactions. """

    def __init__(self, project, source_url=None):
        self.source_url = source_url
        self.project = project
        self.locks = {}

    def make_entity(self, schemata, source_url=None):
        """ Create an entity loader, i.e. a construction helper for entities.

        :param schemata: A list of schema names for all the schemata that the
            entity should be associated with.
        :param source_url: A URL which will be made the default source for all
            properties defined on this entity.

        :returns: :py:class:`EntityLoader <grano.logic.loader.EntityLoader>`
        """
        entity = EntityLoader(self, schemata,
                              source_url=source_url or self.source_url)
        return entity

    def make_relation(self, schema, source, target, source_url=None):
        """ Create a relation loader, i.e. a construction helper for relations.

        :param schema: A schema name for the relation.
        :param source: An :py:class:`EntityLoader <grano.logic.loader.EntityLoader>`
            which has been used to construct the source entity.
        :param target: A second :py:class:`EntityLoader <grano.logic.loader.EntityLoader>`
            which has been used to construct the target entity. Cannot be identical to
            the source.
        :param source_url: A URL which will be made the default source for all
            properties defined on this entity.

        :returns: :py:class:`RelationLoader <grano.logic.loader.RelationLoader>`
        """

        relation = RelationLoader(self, schema, source, target,
                                  source_url=source_url or self.source_url)
        return relation

    def persist(self):
        """ No-op on the web. """
