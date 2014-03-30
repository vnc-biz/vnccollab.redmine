from zope.component import getUtility, getMultiAdapter

from Products.GenericSetup.utils import _getDottedName

from plone.app.portlets.storage import PortletAssignmentMapping

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletManager

from vnccollab.redmine.tests.base import FunctionalTestCase
from vnccollab.redmine.tests._mock import initialize as initialize_mock
from vnccollab.redmine.portlets import redmine_tickets


class PortletTest(FunctionalTestCase):
    def setUp(self):
        super(PortletTest, self).setUp()
        self.setRoles(('Manager', ))

    def test_PortletTypeRegistered(self):
        portlet = getUtility(IPortletType,
            name='vnccollab.redmine.portlets.RedmineTicketsPortlet')
        self.assertEquals(portlet.addview,
            'vnccollab.redmine.portlets.RedmineTicketsPortlet')

    def test_RegisteredInterfaces(self):
        portlet = getUtility(IPortletType,
            name='vnccollab.redmine.portlets.RedmineTicketsPortlet')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
            'plone.app.portlets.interfaces.IDashboard'],
            registered_interfaces)

    def test_Interfaces(self):
        portlet = redmine_tickets.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_InvokeAddview(self):
        portlet = getUtility(IPortletType,
            name='vnccollab.redmine.portlets.RedmineTicketsPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')

        for m in mapping.keys():
            del mapping[m]

        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   redmine_tickets.Assignment))

    def test_InvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = redmine_tickets.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, redmine_tickets.EditForm))

    def test_Renderer(self):
        initialize_mock()
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.leftcolumn',
                             context=self.portal)
        assignment = redmine_tickets.Assignment()

        renderer = getMultiAdapter((context, request, view, manager,
                                    assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, redmine_tickets.Renderer))

        renderer.refresh()
        tickets = renderer.getTickets()

        self.assertTrue(len(tickets) == 2)
        for ticket in tickets:
            self.assertTrue(ticket['body'] in
                            (u'\t<p>some description 1</p>',
                             u'\t<p>some description 2</p>'))
            self.assertTrue(ticket['title'] in
                            (u'Some subject 1', u'Some subject 2'))

        self.assertEquals(renderer.getTicketsURL(), 'https:///issues')
        self.assertEqual(renderer.title, '')
