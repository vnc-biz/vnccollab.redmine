from zope.interface import Interface, Attribute


class IAddOnInstalled(Interface):
    '''Layer specific intrface for this add-on.'''


class IRedmineUtil(Interface):
    '''Interface for Redmine Utility.'''

    def searchIssues(**query):
        '''Returns a list of issues that satify the query.'''

    def searchMyIssues(**query):
        '''Returns a list of issues for the current user that satify the
        query.'''

    def getIssue(id, **query):
        '''Returns an issue given its id.'''

    def getUser(id):
        '''Returns an user given its id.'''


class IReference(Interface):
    id = Attribute('')
    name = Attribute('')


class IUser(Interface):
    id = Attribute('')
    firstname = Attribute('')
    lastname = Attribute('')
    mail = Attribute('')


class IJournal(Interface):
    id = Attribute('')
    user = Attribute('')
    notes = Attribute('')
    created_on = Attribute('')


class IIssue(Interface):
    id = Attribute('Issue Id')
    author = Attribute('Author')
    assigned_to = Attribute('')
    subject = Attribute('')
    description = Attribute('')
    priority = Attribute('')
    status = Attribute('')
    estimated_hours = Attribute('')
    done_ratio = Attribute('')
    start_date = Attribute('')
    due_date = Attribute('')
    created_on = Attribute('')
    updated_on = Attribute('')
    project = Attribute('')
    tracker = Attribute('')
    fixed_version = Attribute('')
    parent = Attribute('')
    journals = Attribute('')
