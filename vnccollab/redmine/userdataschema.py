from zope import schema
from zope.component import adapts
from zope.interface import implements, Interface
from zope.publisher.browser import IBrowserRequest

from collective.customizablePersonalizeForm.adapters.interfaces import \
    IExtendedUserDataSchema, IExtendedUserDataPanel

from vnccollab.redmine import messageFactory as _


class UserDataSchemaAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataSchema)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSchema(self):
        return IUserDataSchema


class UserDataSchemaPropertiesAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataPanel)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getProperties(self):
        return [
            'redmine_username', 'redmine_password'
        ]


class IUserDataSchema(Interface):

    redmine_username = schema.ASCIILine(
        title=_("Redmine Username"),
        description=_(u"We need this field in order to display your Redmine "
                      "related information."),
        required=False)

    redmine_password = schema.Password(
        title=_("Redmine Password"),
        description=_(u"We need this field in order to display your Redmine "
                      "related information."),
        required=False)
