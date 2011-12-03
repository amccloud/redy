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
        self.assertEqual(str(Company.key), 'company')
        self.assertEqual(str(Organization.key), 'group')
        self.assertEqual(str(Person.key), 'person')

        for model_cls in [Company, Organization, Person]:
            self.assertTrue(model_cls.key.has_client())

    def test_fields(self):
        self.assertEqual(
            sorted(Company._meta.fields.keys()),
            sorted(['name', 'email', 'is_active']))
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
