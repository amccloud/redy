RECURSIVE_RELATIONSHIP_CONSTANT = 'self'

__all__ = ['Field', 'AttributeField', 'CounterField', 'ListField', \
            'SetField', 'ReferenceField', 'CounterField']

class Field(object):
    def __init__(self, indexed=False, required=False, \
            default=None, primary_key=False):
        self.name = None
        self.indexed = indexed
        self.required = required
        self.default = default
        self.primary_key = primary_key

    def __contribute__(self, cls, name):
        self.model = cls
        self.model._meta.fields[name] = self

        self.name = name

        if self.primary_key:
            if self.model._meta.primary_key:
                raise self.IntegrityError, \
                    u"Primary key field '%s' already defined." % (
                    self.model._meta.primary_key,
                )

            self.model._meta.primary_key = name

        if self.indexed:
            if name not in self.model._meta.indexes:
                self.model._meta.indexes.append(name)

        setattr(self.model, name, self)

    def __set__(self, instance, value):
        setattr(instance, self.instance_attr, value)

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.instance_attr)
        except AttributeError:
            value = self.default

            if not self.primary_key and instance.pk:
                value = self.to_python(self.get_value(instance))

            self.__set__(instance, value)

            return value

    class IntegrityError(Exception):
        pass

    class ValidationError(Exception):
        pass

    @property
    def instance_attr(self):
        return '_' + self.name

    def pre_save(self, instance):
        pass

    def post_save(self, instance):
        pass

    def to_redis(self, value):
        return value

    def to_python(self, value):
        return value

    def get_value(self, instance):
        return instance.get_key(self.name).get()

    def set_value(self, instance, value):
        instance.get_key(self.name).set(value)

class AttributeField(Field):
    def __contribute__(self, cls, name):
        super(AttributeField, self).__contribute__(cls, name)

        if not hasattr(cls._meta, '_attribute_fields'):
            cls._meta._attribute_fields = {}

        cls._meta._attribute_fields[name] = self

    def get_value(self, instance):
        return instance.key.hget(self.name)

    def set_value(self, instance, value):
        if not hasattr(instance, '_attribute_store'):
            instance._attribute_store = {}

        instance._attribute_store[self.name] = value

        if (len(instance._attribute_store.keys()) == \
            len(instance._meta._attribute_fields.keys())):
            instance.key.hmset(instance._attribute_store)
            instance._attribute_store = {}

class CounterField(AttributeField):
    pass

class AutoCounterField(CounterField):
    INCR = 1
    DECR = -1

    def __init__(self, amount=1, direction=INCR, *args, **kwargs):
        super(AutoCounterField, self).__init__(*args, **kwargs)
        self.amount = amount * direction

    def pre_save(self, instance):
        value = getattr(instance, self.name)

        if value:
            return

        key = instance.get_key(self.name)
        setattr(instance, self.name, key.incr(self.amount))

class ListField(Field):
    pass

class SetField(Field):
    pass

class ReferenceField(Field):
    pass

class CollectionField(Field):
    pass
