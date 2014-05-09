import json
from StringIO import StringIO
from lxml import etree
from zope.component import queryUtility
from zope.component import getUtility
from zope.interface import implementer
from plone.supermodel.utils import noNS
from .interfaces import IJSONSerializer
from .interfaces import IJSONFieldSerializer


@implementer(IJSONSerializer)
class JSONSerializer(object):

    def _parse(self, xml):
        parser = etree.XMLParser()
        tree = etree.parse(StringIO(xml), parser)
        return tree

    def __call__(self, xml):
        tree = self._parse(xml)
        root = tree.getroot()
        data_fields = root.xpath(
            '//*[local-name()="schema"]/*[local-name()="field"]'
        )

        fields = []
        for field in data_fields:
            serializer = queryUtility(
                IJSONFieldSerializer,
                name=field.attrib['type']
            )
            if not serializer:
                serializer = queryUtility(IJSONFieldSerializer)
            fields.append(serializer(field))

        model = {
            'fields': fields
        }
        return json.dumps(model)


def _no_transform(value):
    return value


def _bool_transform(value):
    if value == 'True':
        return True
    return False


@implementer(IJSONFieldSerializer)
class BaseHandler(object):

    name_attr = 'cid'
    type_attr = 'field_type'
    options_attr = 'field_options'

    field_attributes = {
        'required': ('required', _bool_transform),
        'title': ('label', _no_transform),

    }

    field_options = {
        'description': ('description', _no_transform)
    }

    def __init__(self, field_type='text'):
        self.field_type = field_type

    def __call__(self, field):
        """Create and return a new element representing the given field
        """
        data = {
            self.name_attr: field.attrib['name'],
            self.type_attr: self.field_type
        }

        for el in field:
            attr, transform = self.field_attributes.get(
                noNS(el.tag),
                (None, None)
            )
            if not attr:
                continue
            data[attr] = transform(el.text)

        field_options = {}
        for el in field:
            attr, transform = self.field_options.get(
                noNS(el.tag),
                (None, None)
            )
            if not attr:
                continue
            field_options[attr] = transform(el.text)

        data['field_options'] = field_options
        return data


TextLineHandler = BaseHandler()
TextHandler = BaseHandler('paragraph')
DateHandler = BaseHandler('date')
