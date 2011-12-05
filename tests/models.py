import unittest, redis, redy

client = redis.Redis(host='localhost', port=6379, db=9)

class Company(redy.Model):
    name = redy.Field()
    email = redy.Field(indexed=True)
    is_active = redy.Field(default=True)

    class Meta:
        db = client

class Organization(Company):
    class Meta(Company.Meta):
        key = 'group'

class Person(Company):
    age = redy.Field(indexed=True, required=False)

class Message(redy.Model):
    mhash = redy.Field(primary_key=True)

class ModelTestCase(unittest.TestCase):
    def test_meta(self):
        self.assertNotEqual(Company._meta, None)
        self.assertNotEqual(Organization._meta, None)
        self.assertNotEqual(Person._meta, None)

    def test_db(self):
        self.assertEqual(Company.db, client)
        self.assertEqual(Organization.db, client)
        self.assertEqual(Person.db, client)

    def test_key(self):
        self.assertEqual(str(Company._key), 'company')
        self.assertEqual(str(Organization._key), 'group')
        self.assertEqual(str(Person._key), 'person')

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
            is_active=True,
        )

        self.assertEqual(comp2.id, None)
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

    def test_fields(self):
        self.assertEqual(
            sorted(Company._meta.fields.keys()),
            sorted(['id', 'name', 'email', 'is_active']))
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
        with self.assertRaises(redy.Field.IntegrityError):
            class BadMessage(redy.Model):
                id = redy.Field(primary_key=True)
                mhash = redy.Field(primary_key=True)
