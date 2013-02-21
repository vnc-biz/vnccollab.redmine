from pyactiveresource.activeresource import ActiveResource

from zope.interface import implements
from Products.CMFPlone.utils import safe_unicode as su
from plone.memoize.instance import memoize

from plone import api

from vnccollab.redmine.interfaces import IRedmineUtil
from vnccollab.redmine.content import Issue


class RedmineUtil:
    '''Redmine Utility.'''
    implements(IRedmineUtil)

    def _get_server_url(self):
        url = api.portal.get_registry_record('vnccollab.zimbra.server_url')
        return url

    def _get_credentials(self):
        member = api.user.get_current()
        username = member.getProperty('redmine_username', '')
        password = member.getProperty('redmine_password', '')
        # password could contain non-ascii chars, ensure it's properly encoded
        return username, su(password).encode('utf-8')

    @memoize
    def _get_user(self, url, username, password):
        attrs = {'_site': url, '_user': username, '_password': password}
        User = type("User", (ActiveResource,), attrs.copy())
        user = User.find('current')
        return user

    def _get_current_user(self):
        url = self._get_server_url()
        username, password = self._get_credentials()
        return self._get_user(url, username, password)

    @memoize
    def _get_issue(self, url, username, password):
        attrs = {'_site': url, '_user': username, '_password': password}
        issue = type("Issue", (ActiveResource,), attrs.copy())
        return issue

    def searchIssues(self, **query):
        user = self._get_current_user()
        issue = self._get_issue()
        result = issue.find(assigned_to_id=user.id, **query)
        result = [Issue(x) for x in result]
        return result


redmineUtilInstance = RedmineUtil()
