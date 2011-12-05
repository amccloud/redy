class Key(str):
    class NoClient(Exception):
        pass

    def __new__(cls, key, client=None):
        cls = super(Key, cls).__new__(cls, key.lower())
        cls._client = client

        return cls

    def __getattr__(self, key):
        def _client(*args, **kwargs):
            if not self.has_client():
                raise self.NoClient, u"Key does not have client."

            method = getattr(self._client, key)
            return method(self, *args, **kwargs)

        return _client

    def __getitem__(self, key):
        return self.__class__('%s:%s' % (self, key), self._client)

    def __add__(self, key):
        return self.__class__('%s+%s' % (self, key), self._client)

    def __sub__(self, key):
        return self.__class__('%s-%s' % (self, key), self._client)

    def __contribute__(self, cls, name):
        setattr(cls, name, self)

    @property
    def transient(self):
        if self.is_transient():
            return self

        return self.__class__('~', self._client)[self]

    def has_client(self):
        return self._client != None

    def is_transient(self):
        return self.startswith('~')
