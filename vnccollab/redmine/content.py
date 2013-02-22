from DateTime import DateTime

from zope.interface import implements
from Products.CMFPlone.utils import safe_unicode

from vnccollab.redmine.interfaces import IUser, IIssue, IReference, IJournal


class Reference:
    implements(IReference)

    def __init__(self, ref):
        self.raw = ref
        self.id = int(getattr(ref, 'id', -1))
        self.name = _su(ref, 'name')


class User:
    implements(IUser)

    def __init__(self, user):
        self.raw = user
        self.id = _su(user, 'id')
        self.firstname = _su(user, 'firstname')
        self.lastname = _su(user, 'lastname')
        self.mail = _su(user, 'mail')


class BaseRemine:
    def _reference(self, key):
        val = getattr(self.raw, key, None)

        if val is not None:
            val = Reference(val)

        return val


class Journal(BaseRemine):
    implements(IJournal)

    def __init__(self, journal):
        self.raw = journal
        self.id = _su(journal, 'id')
        self.user = self._reference('user')
        self.notes = _su(journal, 'notes')
        self.created_on = _date(journal, 'created_on')


class Issue(BaseRemine):
    implements(IIssue)

    def __init__(self, issue, assigned_to=None):
        self.raw = issue
        self.id = _su(issue, 'id')
        self.project = self._reference('project')
        self.tracker = self._reference('tracker')
        self.author = Reference(issue.author)
        self.status = self._reference('status')
        self.assigned_to = self._reference('assigned_to')
        self.priority = self._reference('priority')
        self.parent = self._reference('parent')
        self.subject = _su(issue, 'subject')
        self.description = _su(issue, 'description')
        self.estimated_hours = _float(issue, 'estimated_hours', -1)
        self.done_ratio = _float(issue, 'done_ratio', 0)
        self.start_date = _date(issue, 'start_date')
        self.due_date = _date(issue, 'due_date')
        self.created_on = _date(issue, 'created_on')
        self.updated_on = _date(issue, 'updated_on')
        self.fixed_version = _su(issue, 'fixed_version')
        self.journals = self._journals(issue)

    def _journals(self, issue):
        journals = getattr(issue, 'journals', [])
        journals = [Journal(x) for x in journals]
        return journals


def _su(item, key):
    return safe_unicode(getattr(item, key, u''))


def _float(item, key, default):
    val = getattr(item, key, default)

    if val is None:
        val = default

    return float(val)


def _date(item, key):
    date = getattr(item, key, None)

    if date is not None:
        date = DateTime(date)

    return date
