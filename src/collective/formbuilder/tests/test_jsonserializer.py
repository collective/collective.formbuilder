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

        data = json.loads(serializer(model))
        self.assertTrue('fields' in data)
        self.assertEqual(data.get('fields'), [])

    def test_fields(self):
        model = """<model
            xmlns="http://namespaces.plone.org/supermodel/schema">
            <schema>
                <field name="c12" type="zope.schema.TextLine">
                    <title>My field</title>
                    <description>My short description</description>
                    <required>False</required>
                </field>
                <field name="c23" type="zope.schema.Text">
                    <title>Another field</title>
                    <required>True</required>
                </field>
            </schema>
        </model>"""

        results = [
            {
                "label": "My field",
                "field_type": "text",
                "required": False,
                "field_options": {
                    "description": "My short description",
                },
                "cid": "c12"
            },
            {
                "label": "Another field",
                "field_type": "paragraph",
                "required": True,
                "field_options": {},
                "cid": "c23"
            }
        ]

        serializer = getUtility(IJSONSerializer)
        data = json.loads(serializer(model))

        self.assertTrue('fields' in data)

        fields = data.get('fields')
        self.assertEqual(len(fields), 2)

        i = 0
        for el in results:
            check = fields[i]
            for k, v in el.items():
                self.assertEqual(check[k], v)

            i += 1


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSerializer))
    return suite
