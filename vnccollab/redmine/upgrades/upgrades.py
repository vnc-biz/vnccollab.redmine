#from Products.CMFCore.utils import getToolByName
from plone.app.upgrade.utils import installOrReinstallProduct
from plone import api

from vnccollab.redmine.config import PROJECTNAME


DEFAULT_PROFILE = 'profile-%s:default' % PROJECTNAME


def upgrade_1000_1001(context):
    '''Installs vnccollab.common.'''
    portal = api.portal.get()
    installOrReinstallProduct(portal, 'vnccollab.common')
