from StringIO import StringIO
import unittest2 as unittest
from lxml import etree
from zope.component import getUtility
from plone.supermodel.interfaces import XML_NAMESPACE
from plone.supermodel.utils import noNS
from ..interfaces import IModelSerializer
from ..testing import FORMBUILDER_INTEGRATION


def parse(xml):
    parser = etree.XMLParser()
    tree = etree.parse(StringIO(xml), parser)
    return tree


class TestSerializer(unittest.TestCase):
    layer = FORMBUILDER_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def test_baseserializer(self):
        serializer = getUtility(IModelSerializer)
        json_template = '{"fields":[]}'
        model = serializer(self.portal, json_template)
        root = parse(model).getroot()
        self.assertEqual(noNS(root.tag), 'model')
        self.assertEqual(len([i for i in root.iterchildren()]), 0)

    def test_dummy(self):
        self.assertTrue(1+1, 2)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSerializer))
    return suite
