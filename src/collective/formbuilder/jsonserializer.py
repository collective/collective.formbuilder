import json
from StringIO import StringIO
from lxml import etree


class JSONSerializer(object):

    def _parse(self, xml):
        parser = etree.XMLParser()
        tree = etree.parse(StringIO(xml), parser)
        return tree

    def __call__(self, context, xml):
        tree = self._parse(xml)
        root = tree.getroot()
        fields = []

        # TODO: parse fields
        for field in root.iterchildren():
            fields.append('1')

        model = {
            'fields': fields
        }

        return json.dumps(model)
