import copy

from .key import Key
from .utils import DeclarativeDescriptor
from .fields import AutoCounterField

class ModelBase(DeclarativeDescriptor):
    def __pre_contribute__(cls, name, bases, attrs):
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

    def __post_contribute__(cls, name, bases, attrs):
        if not hasattr(cls, '_meta'):
            return cls

        if not cls._meta.primary_key and 'id' not in cls._meta.fields:
            cls._add_to_class('id', AutoCounterField(primary_key=True))

        return cls

    class _MetaOptions(object):
        def __init__(self, meta_cls, base_cls=None):
            self._meta_cls = meta_cls
            self._base_cls = base_cls
            self.db = None
            self.key = None
            self.fields = {}
            self.indexes = []
            self.primary_key = None

        def __contribute__(self, cls, name):
            self.key = getattr(self._meta_cls, 'key', cls.__name__.lower())
            self.db = getattr(self._meta_cls, 'db', \
                        getattr(self._base_cls, 'db', None))

            setattr(cls, name, self)

    @property
    def db(cls):
        return cls._db

class Model(object):
    __metaclass__ = ModelBase

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args)

        for key, value in kwargs.iteritems():
            if key not in self._meta.fields:
                raise self.FieldError, \
                    u"Cannot resolve field '%s' in %s. Choices are %s." % (
                        key,
                        self.__class__.__name__,
                        ', '.join(self._meta.fields.keys()),
                    )

            setattr(self, key, value)

    class FieldError(Exception):
        pass

    @property
    def pk(self):
        return getattr(self, self._meta.primary_key)

    @property
    def key(self):
        if not self.pk:
            return self._key

        return self._key[self.pk]

    def validate(self):
        pass

    def save(self):
        fields = self._meta.fields.values()

        for field in fields:
            field.pre_save(self)

            value = field.to_redis(getattr(self, field.name))
            field.set_value(self, value)

            field.post_save(self)

    def delete(self):
        pass

    def create(self, **kwargs):
        pass
