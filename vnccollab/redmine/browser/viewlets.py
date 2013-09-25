import logging
from pyactiveresource.activeresource import ActiveResource

from zope.interface import providedBy
from zope.component import getUtility

from plone.app.layout.viewlets import common
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from vnccollab.redmine import messageFactory as _
from vnccollab.redmine.util import RedmineUtil, logException


logger = logging.getLogger('vnccollab.redmine.RelatedRedmineTicketsViewlet')
util = RedmineUtil()


class RelatedRedmineTicketsViewlet(common.ViewletBase):
    """Lists redmine tickets assigned to current object"""

    def update_new(self):
        # TODO: remove update and replace it by this.
        # But before that we need, to change searchIssues and add searchMyIssues
        # and update cloudstream
        if IPloneSiteRoot in providedBy(self.context):
            return

        uuid = self.context.UID()
        field_key = self._get_field_key()
        url = util._get_server_url()

        try:
            issues = util.searchIssues(**{field_key: uuid,
                                          'status_id': 'o',
                                          'sort': 'updated_on:desc'})
        except:
            logException(logger=logger, context=self.context,
                         msg=_(u"Error during fetching redmine tickets %s"
                               % url))
            issues = []

        # TODO: convert to dic
        self.tickets = [self._ticket_from_issue(x, url) for x in issues]

    def _ticket_from_issue(self, issue, url):
        ticket = {
            'id': issue.id,
            'title': issue.subject,
            'body': issue.description,
            'url': '%s/issues/%s' % (url, issue.id)
        }
        return ticket

    def _get_field_key(self):
        '''Returns the name of the Remine key that is used to store plone
        UUIDs.'''
        registry = getUtility(IRegistry)
        field_id = registry.get('vnccollab.redmine.plone_uid_field_id')
        field_key = 'cf_%d' % field_id
        return field_key

    def update(self):
        self.tickets = ()

        if IPloneSiteRoot in providedBy(self.context):
            return

        tickets = []
        # check if settings are configured
        # check user redmine credentials and redmine url/field id
        registry = getUtility(IRegistry)
        url = registry.get('vnccollab.redmine.server_url')
        field_id = registry.get('vnccollab.redmine.plone_uid_field_id')
        username, password = self.getAuthCredentials()
        if username and password and url and field_id:
            Issue = type("Issue", (ActiveResource,), {'_site': url, '_user':
                         username, '_password': password})
            # do actual calls to redmine
            try:
                # fetch opened issues belonging to authenticated user
                uuid = self.context.UID()
                data = Issue.find(**{'cf_%d' % field_id: uuid,
                                     'status_id': 'o',
                                     'sort': 'updated_on:desc'})
            except Exception:
                logException(logger=logger, context=self.context,
                             msg=_(u"Error during fetching redmine tickets %s"
                                   % url))
                return

            for item in data:
                info = item.to_dict()

                # skip invalid entries
                if not info.get('id') or not info.get('subject'):
                    continue

                tickets.append({
                    'id': info['id'],
                    'title': safe_unicode(info['subject']),
                    'body': safe_unicode(info.get('description', '')),
                    'url': '%s/issues/%s' % (url, info['id'])
                })

        self.tickets = tuple(tickets)

    @memoize
    def getAuthCredentials(self):
        """Returns username and password for redmine user."""
        # take username and password from authenticated user Zimbra creds
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        username = member.getProperty('redmine_username') or ''
        password = member.getProperty('redmine_password') or ''
        # password could contain non-ascii chars, ensure it's properly encoded
        return username, safe_unicode(password).encode('utf-8')

