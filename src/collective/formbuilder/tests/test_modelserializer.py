import json
from StringIO import StringIO
import unittest2 as unittest
from lxml import etree
from zope.component import getUtility
from plone.supermodel.interfaces import XML_NAMESPACE
from plone.supermodel.utils import noNS, ns
from ..interfaces import IModelSerializer
from ..interfaces import IModelFieldSerializer
from ..testing import FORMBUILDER_INTEGRATION


def parse(xml):
    parser = etree.XMLParser()
    tree = etree.parse(StringIO(xml), parser)
    return tree


class TestSerializer(unittest.TestCase):
    layer = FORMBUILDER_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def _check_field(self, field, data, field_type):
        attrs = field.attrib

        self.assertEqual(attrs['name'], data['cid'])
        self.assertEqual(attrs['type'], field_type)

        title = field.xpath('./*[local-name()="title"]')[0]
        self.assertEqual(title.text, data['label'])

        description = field.xpath('./*[local-name()="description"]')[0]
        self.assertEqual(
            description.text,
            data['field_options']['description']
        )

        required = field.xpath('./*[local-name()="required"]')[0]
        self.assertEqual(required.text, str(data['required']))

    def test_baseserializer(self):
        serializer = getUtility(IModelSerializer)

        fields = {
            "fields": []
        }

        model = serializer(json.dumps(fields))

        root = parse(model).getroot()
        self.assertEqual(noNS(root.tag), 'model')
        childrens = [i for i in root.iterchildren()]
        self.assertEqual(len(childrens), 1)

        schema = childrens[0]
        self.assertEqual(noNS(schema.tag), 'schema')
        schema_childrens = [i for i in schema.iterchildren()]
        self.assertEqual(len(schema_childrens), 0)

    def test_fields(self):
        serializer = getUtility(IModelSerializer)
        data = {
            "fields": [
                {
                    "label": "Simple field",
                    "field_type": "text",
                    "required": True,
                    "field_options": {
                        "description": "Field description",
                    },
                    "cid":"c22"
                },

                {
                    "label": "Other field",
                    "field_type": "paragraph",
                    "required": False,
                    "field_options": {
                        "description": "A short description",
                    },
                    "cid":"c23"
                }

            ]
        }

        model = serializer(json.dumps(data))
        tree = parse(model)
        fields = tree.xpath(
            '//*[local-name()="schema"]/*[local-name()="field"]'
        )
        self.assertEqual(len(fields), 2)

        i = 0
        field_type = [
            'zope.schema.TextLine',
            'zope.schema.Text'
        ]

        for field in fields:
            data_field = data['fields'][i]
            self._check_field(field, data_field, field_type[i])
            i += 1

    def test_datefield(self):
        serializer = getUtility(IModelFieldSerializer, name="date")
        data = {
            "label": "Date field",
            "field_type": "date",
            "required": False,
            "field_options": {
                "description": "A short description",
            },
            "cid": "c01"
        }

        element = serializer(data)
        self._check_field(element, data, 'zope.schema.Date')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSerializer))
    return suite
