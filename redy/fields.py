RECURSIVE_RELATIONSHIP_CONSTANT = 'self'

__all__ = ['Field', 'AttributeField', 'CounterField', 'ListField', \
            'SetField', 'ReferenceField', 'CounterField']

class Field(object):
    def __init__(self, indexed=False, required=False, default=None):
        self.indexed = indexed
        self.required = required
        self.default = default

    def __contribute__(self, cls, name):
        cls._meta.fields[name] = self

        if self.indexed:
            if name not in cls._meta.indexes:
                cls._meta.indexes.append(name)

class AttributeField(Field):
    pass

class CounterField(AttributeField):
    pass

class ListField(Field):
    pass

class SetField(Field):
    pass

class ReferenceField(Field):
    pass

class CollectionField(Field):
    pass
