from Acquisition import aq_parent, Implicit
from OFS.OrderedFolder import OrderedFolder

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.interfaces import IActionProvider

from vnccollab.redmine.tests.base import FunctionalTestCase
from vnccollab.redmine.browser.viewlets import RelatedRedmineTicketsViewlet
from vnccollab.redmine.tests._mock import initialize as initialize_mock



class DummyUser(Implicit):
    def getId(self):
        return 'dummy'

    def getProperty(self, name, value=''):
        return {'redmine_username': 'username',
                'redmine_password': 'password'}[name]


class DummyMembershipTool(OrderedFolder, ActionProviderBase):
    implements(IActionProvider)

    def isAnonymousUser(self):
        return False

    def getAuthenticatedMember(self):
        return DummyUser().__of__(aq_parent(self))


class ViewletsTest(FunctionalTestCase):
    members = (
        ('secret', 'Scott Tiger', 'scott@tiger.com',
            ['Manager'], '2013-09-24'),
        ('secret', 'Johann Sebastian Bach', 'johan@bach.com',
            ['Manager'], '2013-09-24'),)

    def setUp(self):
        super(ViewletsTest, self).setUp()
        self.populateSite()

    def populateSite(self):
        self.setRoles(['Manager'])
        if 'Members' in self.portal:
            self.portal._delObject('Members')
            self.folder = None
        if 'news' in self.portal:
            self.portal._delObject('news')
        if 'events' in self.portal:
            self.portal._delObject('events')
        if 'front-page' in self.portal:
            self.portal._delObject('front-page')
        self.portal.invokeFactory('Document', 'doc1 foo', title='doc1 foo')
        self.portal.invokeFactory('Document', 'doc2 foo', title='doc2 foo')
        self.portal.invokeFactory('Document', 'doc3 foo', title='doc3 foo')
        self.portal.invokeFactory('Folder', 'folder1')
        self.portal.invokeFactory('Link', 'link1')
        self.portal.link1.setRemoteUrl('http://plone.org')
        self.portal.link1.reindexObject()
        folder1 = getattr(self.portal, 'folder1')
        self._login('johan@bach.com')
        folder1.invokeFactory('Document', 'doc11', title='doc11 foo')
        folder1.invokeFactory('Document', 'doc12', title='doc12 foo')
        folder1.invokeFactory('Document', 'doc13', title='doc13 foo')
        self.portal.invokeFactory('Folder', 'folder2')
        folder2 = getattr(self.portal, 'folder2')
        self._login('scott@tiger.com')
        folder2.invokeFactory('Document', 'doc21', title='doc21 foo')
        folder2.invokeFactory('Document', 'doc22', title='doc22 foo')
        folder2.invokeFactory('Document', 'doc23', title='doc23 foo')
        folder2.invokeFactory('File', 'file21')
        folder2.invokeFactory('Folder', 'folder21')
        self.setRoles(['Member'])

    def test_RelatedRedmineTicketsViewlet(self):
        initialize_mock()
        self.portal.portal_membership = DummyMembershipTool()
        request = self.app.REQUEST
        viewlet = RelatedRedmineTicketsViewlet(self.portal.folder1,
            request, None, None)
        viewlet.update()

        self.assertTrue(len(viewlet.tickets) == 2)
        for ticket in viewlet.tickets:
            self.assertTrue(ticket['body'] in (u'some description 1', u'some description 2'))
            self.assertTrue(ticket['title'] in (u'Some subject 1', u'Some subject 2'))

        viewlet.tickets = []
        viewlet.update_new()

        self.assertTrue(len(viewlet.tickets) == 2)
        for ticket in viewlet.tickets:
            self.assertTrue(ticket['body'] in (u'some description 1', u'some description 2'))
            self.assertTrue(ticket['title'] in (u'Some subject 1', u'Some subject 2'))
