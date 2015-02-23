# -*- encoding: utf-8 -*-
import json

from lxml import etree
from plone.supermodel.interfaces import XML_NAMESPACE
from plone.supermodel.utils import prettyXML
from zope.component import queryUtility
from zope.interface import implementer

from .utils import get_nsmap
from .interfaces import IModelFieldSerializer
from .interfaces import IModelSerializer


@implementer(IModelSerializer)
class ModelSerializer(object):

    def __call__(self, json_template):
        data = json.loads(json_template)
        if 'fields' not in data:
            raise AttributeError('Missing fields attribute')

        nsmap = get_nsmap()
        xml = etree.Element('model', nsmap=nsmap)
        xml.set('xmlns', XML_NAMESPACE)

        schema_element = etree.Element('schema')
        for f in data.get('fields'):
            serializer = queryUtility(
                IModelFieldSerializer, name=f['field_type']
            )
            if not serializer:
                serializer = queryUtility(IModelFieldSerializer)
            field = serializer(f)
            schema_element.append(field)

        xml.append(schema_element)
        return prettyXML(xml)


@implementer(IModelFieldSerializer)
class BaseHandler(object):

    name_attr = 'cid'
    options_attr = 'field_options'

    field_attributes = {
        'required': 'required',
        'title': 'label'
    }

    field_options = {
        'description': 'description'
    }

    def __init__(self, field_type='zope.schema.TextLine'):
        self.field_type = field_type

    def set_children(self, element, field, attributes):
        for name, attr in attributes.items():
            value = field.get(attr)
            child = None
            if value is not None:
                child = etree.Element(name)
                if not isinstance(value, basestring):
                    value = str(value)
                child.text = value
                element.append(child)

    def set_field_options(self, element, field):
        self.set_children(
            element,
            field[self.options_attr],
            self.field_options
        )

    def __call__(self, field):
        """Create and return a new element representing the given field
        """

        element = etree.Element('field')
        element.set('name', field.get(self.name_attr))
        element.set('type', self.field_type)

        self.set_children(
            element,
            field,
            self.field_attributes
        )

        self.set_field_options(element, field)
        return element


class ChoiceHandler(BaseHandler):

    def set_field_options(self, element, field):
        super(ChoiceHandler, self).set_field_options(element, field)

        # {u'options': [
        #   {u'checked': False, u'label': u'uno'},
        #   {u'checked': False, u'label': u'due'},
        #   {u'checked': False, u'label': u'tre'}
        # ]},
        # u'label': u'Senza titolo'}

        #   <values>
        #     <element>uno</element>
        #     <element>due</element>
        #     <element>tre</element>
        #   </values>
        field_values = etree.Element('values')

        default = None

        values = []
        for opt in field[self.options_attr]['options']:
            value = opt["label"].strip()
            if not value:
                # TODO: logging
                continue
            if value in values:
                # TODO: logging
                continue
            values.append(value)
            if opt['checked']:
                default = value
            child = etree.Element('element')
            child.text = value
            field_values.append(child)
        element.append(field_values)
        if default:
            child = etree.Element('default')
            child.text = default
            element.append(child)


class ListHandler(BaseHandler):

    field_value_type = 'zope.schema.Choice'

    def set_field_options(self, element, field):
        super(ListHandler, self).set_field_options(element, field)

        # <value_type type="zope.schema.Choice">
        #   <values>
        #     <element>a</element>
        #     <element>b</element>
        #   </values>
        # </value_type>
        value_type = etree.Element('value_type')
        value_type.set('type', self.field_value_type)

        field_values = etree.Element('values')
        default = []

        values = []
        for opt in field[self.options_attr]['options']:
            value = opt["label"].strip()
            if not value:
                # TODO: logging
                continue
            if value in values:
                # TODO: logging
                continue
            values.append(value)
            if opt['checked']:
                default.append(value)
            child = etree.Element('element')
            child.text = value
            field_values.append(child)

        value_type.append(field_values)
        element.append(value_type)

        # XXX: default doesn't work properly with multichoice
        # if default:
        #     child = etree.Element('default')
        #     child.text = default
        #     element.append(child)


TextLineHandler = BaseHandler()
TextHandler = BaseHandler('zope.schema.Text')
DateHandler = BaseHandler('zope.schema.Date')
NamedBlobFileHandler = BaseHandler('plone.namedfile.field.NamedBlobFile')
DropdownHandler = ChoiceHandler('zope.schema.Choice')

SectionBreakHandler = BaseHandler('collective.formbuilder.fields.SectionBreak')
EmailHandler = BaseHandler('collective.formbuilder.fields.Email')
RadioButtonHandler = ChoiceHandler('collective.formbuilder.fields.Radiobutton')
CheckboxHandler = ListHandler('collective.formbuilder.fields.Checkbox')
