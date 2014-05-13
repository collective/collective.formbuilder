from zope.interface import implementer
from zope.schema.interfaces import ITextLine
from zope.schema._field import TextLine
from Products.CMFDefault.utils import checkEmailAddress
from plone.supermodel.exportimport import BaseHandler


class IEmail(ITextLine):
    pass


@implementer(IEmail)
class Email(TextLine):

    def constraint(self, value):
        checkEmailAddress(value)
        return super(Email, self).constraint(value)


# plone.supermodel export/import handler
EmailHandler = BaseHandler(Email)
