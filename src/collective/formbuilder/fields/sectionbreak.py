from zope.interface import implementer
from zope.schema.interfaces import ITextLine
from zope.schema._field import TextLine
from plone.supermodel.exportimport import BaseHandler

# TODO: definire un widget specifico


class ISectionBreak(ITextLine):
    pass


@implementer(ISectionBreak)
class SectionBreak(TextLine):

    def __init__(self, *args, **kw):
        kw['readonly'] = False  # BBB: ...
        kw['required'] = False
        super(SectionBreak, self).__init__(*args, **kw)


# plone.supermodel export/import handler
SectionBreakHandler = BaseHandler(SectionBreak)
