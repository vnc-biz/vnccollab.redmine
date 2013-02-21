from zope.interface import Interface, Attribute


class IRedmineUtil(Interface):
    '''Interface for Redmine Utility.'''

    def searchIssues(**query):
        ''' '''


class IUser(Interface):
    id = Attribute('')
    firstname = Attribute('')
    lastname = Attribute('')
    mail = Attribute('')


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
    custom_fields = Attribute('')
