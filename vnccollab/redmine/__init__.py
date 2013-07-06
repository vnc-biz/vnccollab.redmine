# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

messageFactory = MessageFactory('vnccollab.redmine')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
