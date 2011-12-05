import unittest, redis, redy, datetime

client = redis.Redis(host='localhost', port=6379, db=9)

class Company(redy.Model):
    name = redy.AttributeField()
    email = redy.AttributeField(indexed=True)
    ctime = redy.DateTimeField(default=datetime.datetime.now)
    is_active = redy.BooleanField(default=True)

    class Meta:
        db = client

class Organization(Company):
    class Meta(Company.Meta):
        key = 'group'

class Person(Company):
    age = redy.AttributeField(indexed=True, required=False)

class Message(redy.Model):
    mhash = redy.Field(primary_key=True)

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        client.flushdb()

    def tearDown(Self):
        client.flushdb()
        client.connection_pool.disconnect()

    def test_meta(self):
        for model in [Company, Organization, Person]:
            self.assertIsNotNone(model._meta)

    def test_db(self):
        for model in [Company, Organization, Person]:
            self.assertEqual(model.db, client)

    def test_key(self):
        for model in [Company, Person]:
            self.assertEqual(str(model._key), model.__name__.lower())

        self.assertEqual(str(Organization._key), 'group')

    def test_key_client(self):
        for model_cls in [Company, Organization, Person]:
            self.assertTrue(model_cls._key.has_client())

    def test_create_instance(self):
        comp = Company()
        comp.name = 'Pixelcloud Inc.'
        comp.email = 'andrew@pixelcloud.com'
        comp.is_active = True
        comp.save()

        self.assertEqual(comp.id, 1)
        self.assertEqual(comp.pk, 1)
        self.assertEqual(comp.name, 'Pixelcloud Inc.')

        comp2 = Company(
            name='Acme Corporation',
            email='beepbeep@acme.comp',
            is_active=True
        )

        self.assertIsNone(comp2.id)
        self.assertEqual(comp2.name, 'Acme Corporation')

        comp2.save()

        self.assertEqual(comp2.id, 2)
        self.assertEqual(comp2.pk, 2)
        self.assertEqual(comp2.name, 'Acme Corporation')

        with self.assertRaises(Company.FieldError):
            Company(
                name='Umbrella Corporation',
                hazardous=True
            )

    def test_field_defaults(self):
        comp = Company(
            name='Acme Corporation',
            email='beepbeep@acme.comp'
        )

        self.assertEqual(comp.is_active, True)
        self.assertIsNotNone(comp.ctime)

        comp.save()

        self.assertEqual(comp.is_active, True)
        self.assertEqual(type(comp.ctime), datetime.datetime)

    def test_fields(self):
        self.assertEqual(
            sorted(Company._meta.fields.keys()),
            sorted(['id', 'name', 'email', 'ctime', 'is_active']))
        self.assertEqual(
            sorted(Organization._meta.fields.keys()),
            sorted(Company._meta.fields.keys()))
        self.assertEqual(
            sorted(Person._meta.fields.keys()),
            sorted(Company._meta.fields.keys() + ['age']))
        self.assertNotEqual(
            sorted(Company._meta.fields.values()),
            sorted(Organization._meta.fields.values()))
        self.assertNotEqual(
            sorted(Company._meta.fields.values()),
            sorted(Person._meta.fields.values()))

    def test_indexes(self):
        self.assertEqual(Company._meta.indexes, ['email'])

    def test_primary_key(self):
        self.assertEqual(Message._meta.primary_key, 'mhash')
        self.assertEqual(Message._meta.fields.keys(), 
            sorted(['mhash']))
        with self.assertRaises(Message.FieldError):
            class BadMessage(redy.Model):
                id = redy.Field(primary_key=True)
                mhash = redy.Field(primary_key=True)

    def test_default_manager(self):
        for model in [Company, Organization]:
            self.assertIsNotNone(model.objects)

    def test_instance_default_manager(self):
        comp = Company.objects.create(
            name='Acme Corporation',
            email='beepbeep@acme.comp'
        )

        self.assertRaises(Exception, comp, 'objects')
