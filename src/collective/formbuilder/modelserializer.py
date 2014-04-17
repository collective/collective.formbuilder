import json
from lxml import etree
from zope.component import getUtilitiesFor
from plone.supermodel.interfaces import XML_NAMESPACE
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.utils import prettyXML
from plone.supermodel.interfaces import IFieldExportImportHandler
from plone.supermodel.interfaces import ISchemaMetadataHandler
from plone.supermodel.interfaces import IFieldMetadataHandler


class ModelSerializer(object):

    def __call__(self, context, json_template):
        data = json.loads(json_template)
        if 'fields' not in data:
            raise AttributeError('Missing fields attribute')

        handlers = {}
        schema_metadata_handlers = tuple(
            getUtilitiesFor(ISchemaMetadataHandler)
        )
        field_metadata_handlers = tuple(
            getUtilitiesFor(IFieldMetadataHandler)
        )

        nsmap = {}
        metadata_handlers = schema_metadata_handlers + field_metadata_handlers
        for name, handler in metadata_handlers:
            namespace, prefix = handler.namespace, handler.prefix
            if namespace is not None and prefix is not None:
                nsmap[prefix] = namespace

        xml = etree.Element('model', nsmap=nsmap)
        xml.set('xmlns', XML_NAMESPACE)
        return prettyXML(xml)
