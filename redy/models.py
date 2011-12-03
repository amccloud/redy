import copy

from .key import Key
from .utils import DeclarativeDescriptor

class ModelBase(DeclarativeDescriptor):
    def __prepare__(cls, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, ModelBase)]

        if not parents:
            return cls

        meta_cls = attrs.get('Meta', getattr(cls, 'Meta', None))
        meta_base = getattr(cls, '_meta', None)

        cls._add_to_class('_meta', cls._MetaOptions(meta_cls, meta_base))
        cls._add_to_class('_db', cls._meta.db)
        cls._add_to_class('_key', Key(cls._meta.key, client=cls.db))

        for base_cls in parents:
            if not hasattr(base_cls, '_meta'):
                continue

            for name, field in base_cls._meta.fields.iteritems():
                cls._add_to_class(name, copy.deepcopy(field))

        return cls

    class _MetaOptions(object):
        def __init__(self, meta_cls, base_cls=None):
            self._meta_cls = meta_cls
            self._base_cls = base_cls
            self.db = None
            self.key = None
            self.fields = {}
            self.indexes = []

        def __contribute__(self, cls, name):
            self.key = getattr(self._meta_cls, 'key', cls.__name__.lower())
            self.db = getattr(self._meta_cls, 'db', \
                        getattr(self._base_cls, 'db', None))

            setattr(cls, name, self)

    @property
    def db(cls):
        return cls._db

    @property
    def key(cls):
        return cls._key

class Model(object):
    __metaclass__ = ModelBase
