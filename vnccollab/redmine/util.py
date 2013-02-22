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
        url = api.portal.get_registry_record('vnccollab.redmine.server_url')
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
        IssueClass = type("Issue", (ActiveResource,), attrs.copy())
        return IssueClass

    def _get_current_issue(self):
        url = self._get_server_url()
        username, password = self._get_credentials()
        return self._get_issue(url, username, password)

    def searchIssues(self, **query):
        '''Returns a list of issues that satisfy query.

        ARGS:
            query: Dictionary specifying the query.
                offset:
                limit:
                sort:
                project_id:
                subproject_id:
                tracker_id:
                assigned_to_id:
        '''
        user = self._get_current_user()
        IssueClass = self._get_current_issue()
        result = IssueClass.find(assigned_to_id=user.id, **query)
        result = [Issue(x) for x in result]
        return result

    def getIssue(self, id, **args):
        '''Gets the issue identified by id.

        ARGS:
            id: The id of the Issue to fetch.
            args: Specifies associated data to the issue. Possible values are:
                include: Comma separated string with the fields to include.
                    It could be any of:
                        journals
                        children
                        attachments
                        relations
                        changeset
                        watchers
        '''
        IssueClass = self._get_current_issue()
        return IssueClass.get(id, **args)


redmineUtilInstance = RedmineUtil()
