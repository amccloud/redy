import unittest
from redy.utils import DeclarativeDescriptor

class Topping(object):
    def __init__(self, amount='normal'):
        self.amount = amount

    def __contribute__(self, cls, name):
        if not hasattr(cls, 'toppings'):
            cls.toppings = {}

        cls.toppings[name] = self

class BestPriceFinder(object):
    pass

class Hotdog(object):
    __metaclass__ = DeclarativeDescriptor

    name = 'plain'
    price = BestPriceFinder()

    chili = Topping()
    cheese = Topping('extra')
    onions = Topping('light')

class DeclarativeDescriptorTestCase(unittest.TestCase):
    def test_attributes(self):
        self.assertEqual(Hotdog.name, 'plain')
        self.assertIsInstance(Hotdog.price, BestPriceFinder)

    def test_contributions(self):
        self.assertRaises(AttributeError, getattr, Hotdog, 'chili')
        self.assertEqual(
            sorted(Hotdog.toppings.keys()),
            sorted(['chili', 'cheese', 'onions']))
        self.assertIsInstance(Hotdog.toppings['chili'], Topping)
        self.assertEqual(Hotdog.toppings['cheese'].amount, 'extra')
