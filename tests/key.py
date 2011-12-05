import unittest, redis, redy

class KeyTestCase(unittest.TestCase):
    def get_client(self, cls=redis.Redis):
        return cls(host='localhost', port=6379, db=9)

    def setUp(self):
        self.client = self.get_client()
        self.client.flushdb()

    def tearDown(self):
        self.client.flushdb()
        self.client.connection_pool.disconnect()

    def test_key(self):
        user = redy.Key('user')
        self.assertEqual(str(user), 'user')
        self.assertEqual(str(user[0]), 'user:0')
        self.assertEqual(str(user[0]['age']), 'user:0:age')
        self.assertFalse(user.has_client())
        self.assertRaises(redy.Key.NoClient, lambda: user[0]['age'].set(21))

    def test_key_case(self):
        user = redy.Key('USER')
        self.assertEqual(str(user), 'user')
        self.assertEqual(str(user[0]['Age']), 'user:0:age')

    def test_transient_key(self):
        user = redy.Key('user')
        self.assertTrue(user.transient.is_transient())
        self.assertEqual(str(user.transient), '~:user')
        self.assertEqual(str(user[0].transient), '~:user:0')
        self.assertEqual(str(user[0]['age'].transient), '~:user:0:age')

    def test_key_with_client(self):
        user = redy.Key('user', self.client)
        self.assertTrue(user.has_client())
        self.assertIsNone(user[0]['age'].get())
        self.assertTrue(user[0]['age'].set(21))
        self.assertTrue(user[0]['age'].incr())
        self.assertEqual(user[0]['age'].get(), '22')
