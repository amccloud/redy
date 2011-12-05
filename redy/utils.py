class DeclarativeDescriptor(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super(DeclarativeDescriptor, cls).__new__(cls, name, bases, {
            '__module__': attrs.pop('__module__'),
        })

        if hasattr(cls, '__pre_contribute__'):
            new_cls = cls.__pre_contribute__(new_cls, name, bases, attrs)

        for obj_name, obj in attrs.items():
            new_cls._add_to_class(obj_name, obj)

        if hasattr(cls, '__post_contribute__'):
            new_cls = cls.__post_contribute__(new_cls, name, bases, attrs)

        return new_cls

    def _add_to_class(cls, name, value):
        if hasattr(value, '__contribute__'):
            value.__contribute__(cls, name)
        else:
            setattr(cls, name, value)
