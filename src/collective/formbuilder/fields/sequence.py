from zope.interface import implementer
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IList
from zope.schema import Choice
from zope.schema import List
from zope.schema.interfaces import IFromUnicode
from plone.supermodel.exportimport import ChoiceHandler
from plone.supermodel.exportimport import BaseHandler


class IRadiobutton(IChoice):
    pass


@implementer(IRadiobutton, IFromUnicode)
class Radiobutton(Choice):
    pass


class ICheckbox(IList):
    pass


@implementer(ICheckbox, IFromUnicode)
class Checkbox(List):
    pass

# plone.supermodel export/import handler
RadiobuttonHandler = ChoiceHandler(Radiobutton)
CheckboxHandler = BaseHandler(Checkbox)
