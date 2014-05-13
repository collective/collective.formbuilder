from zope.interface import implementer
from zope.schema.interfaces import IChoice
from zope.schema import Choice
from zope.schema.interfaces import IFromUnicode
from plone.supermodel.exportimport import ChoiceHandler


class IRadiobutton(IChoice):
    pass


@implementer(IRadiobutton, IFromUnicode)
class Radiobutton(Choice):
    pass


class ICheckbox(IChoice):
    pass


@implementer(ICheckbox, IFromUnicode)
class Checkbox(Choice):
    pass

# plone.supermodel export/import handler
RadiobuttonHandler = ChoiceHandler(Radiobutton)
CheckboxHandler = ChoiceHandler(Checkbox)
