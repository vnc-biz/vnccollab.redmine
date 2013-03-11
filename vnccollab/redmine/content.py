from DateTime import DateTime

from zope.interface import implements
from Products.CMFPlone.utils import safe_unicode

from vnccollab.redmine.interfaces import IUser, IIssue, IReference, IJournal


class BaseRemine:
    def __init__(self, raw):
        self.raw = raw
        self.raw_is_dict = isinstance(raw, dict)
        self.id = self._su('id')

    def _getattr(self, key, default=u''):
        '''The raw object could be an object or a dict.'''
        if self.raw_is_dict:
            val = self.raw.get(key, default)
        else:
            val = getattr(self.raw, key, default)

        return val

    def _su(self, key):
        return safe_unicode(self._getattr(key, u''))

    def _float(self, key, default):
        val = self._getattr(key, default)

        if val is None:
            val = default

        return float(val)

    def _date(self, key):
        date = self._getattr(key, None)

        if date is not None:
            date = DateTime(date)

        return date

    def _reference(self, key):
        val = self._getattr(key, None)

        if val is not None:
            val = Reference(val)

        return val


class Reference(BaseRemine):
    implements(IReference)

    def __init__(self, ref):
        BaseRemine.__init__(self, ref)
        self.name = self._su('name')


class User(BaseRemine):
    implements(IUser)

    def __init__(self, user):
        BaseRemine.__init__(self, user)
        self.firstname = self._su('firstname')
        self.lastname = self._su('lastname')
        self.mail = self._su('mail')


class Journal(BaseRemine):
    implements(IJournal)

    def __init__(self, journal):
        BaseRemine.__init__(self, journal)
        self.user = self._reference('user')
        self.notes = self._su('notes') or u''
        self.created_on = self._date('created_on')


class Issue(BaseRemine):
    implements(IIssue)

    def __init__(self, issue):
        BaseRemine.__init__(self, issue)
        self.project = self._reference('project')
        self.tracker = self._reference('tracker')
        self.author = self._reference('author')
        self.status = self._reference('status')
        self.assigned_to = self._reference('assigned_to')
        self.priority = self._reference('priority')
        self.parent = self._reference('parent')
        self.subject = self._su('subject')
        self.description = self._su('description')
        self.estimated_hours = self._float('estimated_hours', -1)
        self.done_ratio = self._float('done_ratio', 0)
        self.start_date = self._date('start_date')
        self.due_date = self._date('due_date')
        self.created_on = self._date('created_on')
        self.updated_on = self._date('updated_on')
        self.fixed_version = self._su('fixed_version')
        self.journals = self._journals(issue)

    def _journals(self, issue):
        journals = self._getattr('journals', [])
        journals = [Journal(x) for x in journals]
        return journals
