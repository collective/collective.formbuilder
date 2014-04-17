import json
import unittest2 as unittest

from zope.component import getUtility
from ..interfaces import IJSONSerializer
from ..testing import FORMBUILDER_INTEGRATION


class TestSerializer(unittest.TestCase):
    layer = FORMBUILDER_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_baseserializer(self):
        serializer = getUtility(IJSONSerializer)
        model = """<model
            xmlns="http://namespaces.plone.org/supermodel/schema">
        </model>"""

        data = json.loads(serializer(self.portal, model))
        self.assertTrue('fields' in data)
        self.assertEqual(data.get('fields'), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSerializer))
    return suite
