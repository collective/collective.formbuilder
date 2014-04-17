from zope.interface import Interface


class IJSONSerializer(Interface):
    """Serialize form's fields from to schema model to JSON"""


class IModelSerializer(Interface):
    """Serialize form's fields from JSON to schema model"""


class IJSONFieldSerializer(Interface):
    """Serialize a field from schema model to JSON"""


class IModelFieldSerializer(Interface):
    """Serialize a field from JSON to schema model"""
