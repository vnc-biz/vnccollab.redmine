#from Products.CMFCore.utils import getToolByName
from plone.app.upgrade.utils import installOrReinstallProduct
from plone import api

from vnccollab.redmine.config import PROJECTNAME
from vnccollab.redmine.upgrades.replaceportlets import replace_all_portlets


DEFAULT_PROFILE = 'profile-%s:default' % PROJECTNAME


def upgrade_1000_1001(context):
    '''Installs vnccollab.common.'''
    portal = api.portal.get()
    installOrReinstallProduct(portal, 'vnccollab.common')


def upgrade_1000_1001_replace_portlets(context):
    '''Replace Theme portlets.'''
    replace_all_portlets()
