from DateTime import DateTime

from zope.interface import implements
from Products.CMFPlone.utils import safe_unicode as su

from vnccollab.redmine.interfaces import IUser, IIssue


class User:
    implements(IUser)

    def __init__(self, user):
        self.raw = user
        self.id = user.id
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.mail = user.mail


class Issue:
    implements(IIssue)

    def __init__(self, issue, assigned_to=None):
        self.raw = issue
        self.id = issue.id
        self.author = issue.author
        self.assigned_to = self._assigned_to(issue, assigned_to)
        self.subject = su(issue.subject)
        self.description = su(issue.description)
        self.priority = su(issue.priority)
        self.status = su(issue.status)
        self.estimated_hours = float(issue.estimated_hours)
        self.done_ratio = su(issue.done_ratio)
        self.start_date = DateTime(issue.start_date)
        self.due_date = DateTime(issue.due_date)
        self.created_on = DateTime(issue.created_on)
        self.updated_on = DateTime(issue.updated_on)
        self.project = su(issue.project)
        self.tracker = su(issue.tracker)
        self.fixed_version = su(issue.fixed_version)
        self.parent = su(issue.parent)
        self.custom_fields = issue.custom_fields

    def _assigned_to(self, issue, assigned_to):
        if assigned_to:
            assigned = assigned_to
        else:
            assigned = issue.assigned_to

        return assigned
