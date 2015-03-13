
from zope.component import adapter
from zope.interface import implementer, implementer_only
from zope.schema.interfaces import ITextLine, IField
from zope.schema._field import TextLine
from plone.supermodel.exportimport import BaseHandler
from z3c.form.interfaces import IFormLayer, IFieldWidget, ITextWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser import text


class ISectionBreak(ITextLine):
    """ """


class ISectionBreakWidget(ITextWidget):
    """ """


@implementer(ISectionBreak)
class SectionBreak(TextLine):

    def __init__(self, *args, **kw):
        kw['readonly'] = False  # BBB: ...
        kw['required'] = False
        super(SectionBreak, self).__init__(*args, **kw)


# plone.supermodel export/import handler
SectionBreakHandler = BaseHandler(SectionBreak)


@implementer_only(ISectionBreakWidget)
class SectionBreakWidget(text.TextWidget):
    """Input type sectionbreak widget implementation."""
    klass = u'text-widget'
    css = u'text'
    value = u''


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def SectionBreakFieldWidget(field, request):
    """IFieldWidget factory for SectionBreak."""
    if not field.title:
        field.title = u''
    return FieldWidget(field, SectionBreakWidget(request))
