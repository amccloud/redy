class ValueSet(object):
    def __init__(self, model, index):
        self.model = model
        self._index = index
        self._filters = {}
        self._zfilters = {}
        self._excludes = {}
        self._limit = None
        self._offset = None
        self._order_by = []

    @property
    def key(self):
        return self.model.key[self._index]

    @property
    def ordered(self):
        return bool(self._order_by)

    def _clone(self):
        clone = self.__class__(self.model, self._index)
        clone._filters = self._filters
        clone._zfilters = self._zfilters
        clone._excludes = self._excludes
        clone._limit = self._limit
        clone._offset = self._offset
        clone._order_by = self._order_by

        return clone

    def all(self):
        return self._clone()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        return instance if instance.save() else None

    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        instance = self.filter(**kwargs).first()
        created = False

        if not instance:
            instance = self.create(**defaults)
            created = True

        return (instance, created)

    def filter(self, **kwargs):
        clone = self._clone()
        clone._filters.update(**kwargs)

        return clone

    def zfilter(self, **kwargs):
        clone = self._clone()
        clone._zfilters.update(**kwargs)

        return clone

    def exclude(self, **kwargs):
        clone = self._clone()
        clone._excludes.update(**kwargs)

        return clone

    def limit(self, limit, offset=0):
        clone = self._clone()
        clone._limit = limit
        clone._offset = offset

        return clone

    def order_by(self, *fields):
        clone = self._clone()
        clone._order_by = []

        for field in fields:
            name = field.lstrip('-')

            if name not in self.model._meta.indexes:
                raise self.model.FieldError, \
                    u"Field '%s' must be indexed to be ordered by." % (
                        name,
                    )

            clone._order_by.append(field)

        return clone
