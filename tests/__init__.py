import unittest

from .key import KeyTestCase
from .declarative import DeclarativeDescriptorTestCase
from .models import ModelTestCase

def test_all():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(ModelTestCase))
    suite.addTest(unittest.makeSuite(DeclarativeDescriptorTestCase))
    suite.addTest(unittest.makeSuite(KeyTestCase))

    return suite
    