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
        self.id = _coerce(issue, 'id')
        self.author = _coerce(issue, 'author')
        self.assigned_to = self._assigned_to(issue, assigned_to)
        self.subject = _coerce(issue, 'subject', fn=su)
        self.description = _coerce(issue, 'description', fn=su)
        self.priority = _coerce(issue, 'priority', fn=su)
        self.status = _coerce(issue, 'status', fn=su)
        self.estimated_hours = _coerce(issue, 'estimated_hours', 0, float)
        self.done_ratio = _coerce(issue, 'done_ratio', fn=su)
        self.start_date = _coerce(issue, 'start_date', fn=DateTime)
        self.due_date = _coerce(issue, 'due_date', fn=DateTime)
        self.created_on = _coerce(issue, 'created_on', fn=DateTime)
        self.updated_on = _coerce(issue, 'updated_on', fn=DateTime)
        self.project = _coerce(issue, 'project', fn=su)
        self.tracker = _coerce(issue, 'tracker', fn=su)
        self.fixed_version = _coerce(issue, 'fixed_version', fn=su)
        self.parent = self._parent(issue)
        self.custom_fields = issue.custom_fields

    def _assigned_to(self, issue, assigned_to):
        if assigned_to:
            assigned = assigned_to
        else:
            assigned = issue.assigned_to

        return assigned

    def _parent(self, issue):
        try:
            parent = issue.parent
        except:
            return ''

        if parent is None:
            return ''
        else:
            return parent.id


def _coerce(issue, key, default=u'', fn=None):
    # Issues define all their attributes, some with None
    val = getattr(issue, key)
    if val is None:
        val = default

    if fn is not None:
        try:
            val = fn(val)
        except:
            val = default

    return val
