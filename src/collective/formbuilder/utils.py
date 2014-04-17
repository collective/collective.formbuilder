from zope.component import getUtilitiesFor
from plone.supermodel.interfaces import ISchemaMetadataHandler
from plone.supermodel.interfaces import IFieldMetadataHandler


def get_nsmap():
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
    return nsmap
