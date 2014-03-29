import logging
import textile

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from vnccollab.redmine import messageFactory as _
from vnccollab.redmine.util import RedmineUtil, logException
from vnccollab.common.portlets import deferred


logger = logging.getLogger('vnccollab.redmine.RedmineTicketsPortlet')
util = RedmineUtil()


class IRedmineTicketsPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the portlet."),
        required=True,
        default=u'Redmine Tickets')

    count = schema.Int(
        title=_(u"Number of items to display"),
        description=_(u"How many items to list."),
        required=True,
        default=5)

    request_timeout = schema.Int(
        title=_(u"Request timeout"),
        description=_(u"How many seconds to wait for hanging Redmine request."),
        required=True,
        default=15)


class Assignment(base.Assignment):
    implements(IRedmineTicketsPortlet)

    header = u''
    count = 5
    request_timeout = 15

    @property
    def title(self):
        """Return portlet header"""
        return self.header

    def __init__(self, header=u'', count=5, request_timeout=15):
        self.header = header
        self.count = count
        self.request_timeout = request_timeout


class Renderer(deferred.DeferredRenderer):

    render_preload = render_full = ZopeTwoPageTemplateFile(
        'templates/redmine_tickets.pt')

    def refresh(self):
        '''Calculates the data needed for deferred_update.'''
        self.getTickets()

    def getTickets(self):
        """Returns list of opened issues for authenticated user"""
        try:
            tickets = util.searchMyIssues(status_id='o', sort='updated_on:desc')
        except:
            logException(msg=_(u"Error during fetching redmine tickets %s" %
                               util._get_server_url),
                         context=self.context, logger=logger)
            return ()

        plone_view = getMultiAdapter((self.context, self.request),
                                     name=u'plone')
        url = util._get_server_url()

        tickets = [x for x in tickets if x.id and x.subject]
        tickets = tickets[:self.data.count]
        result = tuple([self._dct_from_issue(x, plone_view, url) for x in tickets])
        return result

    def _dct_from_issue(self, issue, plone_view, url):
        '''Converts an issue in a dict.'''
        try:
            body = textile.textile(issue.description)
        except:
            body = issue.description
        date = plone_view.toLocalizedTime(issue.updated_on, long_format=1)

        dct = {
            'id': issue.id,
            'title': issue.subject,
            'body': body,
            'date': date,
            'url': '%s/issues/%s' % (url, issue.id)
        }
        return dct

    def getTicketsURL(self):
        """Returns tickets root url"""
        return '%s/issues' % util._get_server_url()

    @property
    def title(self):
        """return title of feed for portlet"""
        return self.data.header


class AddForm(base.AddForm):
    form_fields = form.Fields(IRedmineTicketsPortlet)
    label = _(u"Add Redmine Tickets Portlet")
    description = _(u"Renders list of opened Redmine Tickets for authenticated "
                    "user.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IRedmineTicketsPortlet)
    label = _(u"Edit Redmine Tickets Portlet")
    description = _(u"Renders list of opened Redmine Tickets for authenticated "
                    "user.")
