from .valueset import ValueSet

class ManagerDescriptor(object):
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, type=None):
        if instance:
            raise Exception, \
                u"Manager isn't accessible via %s instances." % (
                    type.__name__,
                )

        return self.manager

class Manager(object):
    def __contribute__(self, cls, name):
        self.model = cls
        self.name = name

        self.model._meta.managers[self.name] = self

        if not hasattr(self.model, '_default_manager'):
            self.model._meta._default_manager = self

        setattr(self.model, self.name, ManagerDescriptor(self))

    def get_value_set(self):
        return ValueSet(self.model, self.name)

    def all(self):
        return self.get_value_set().all()

    def create(self, **kwargs):
        return self.get_value_set().create(**kwargs)

    def get_or_create(self, **kwargs):
        return self.get_value_set().get_or_create(**kwargs)

    def filter(self, **kwargs):
        return self.get_value_set().filter(**kwargs)

    def zfilter(self, **kwargs):
        return self.get_value_set().zfilter(**kwargs)

    def exclude(self, **kwargs):
        return self.get_value_set().exclude(**kwargs)

    def order(self, *fields):
        return self.get_value_set().order(*fields)
